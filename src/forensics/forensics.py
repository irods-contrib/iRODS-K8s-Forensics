# SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.
# SPDX-FileCopyrightText: 2023 Renaissance Computing Institute. All rights reserved.
# SPDX-FileCopyrightText: 2024 Renaissance Computing Institute. All rights reserved.
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-License-Identifier: LicenseRef-RENCI
# SPDX-License-Identifier: MIT

"""
    Main entry point for the forensics microservice application
"""
import os
import time
import sys
import json

from src.common.logger import LoggingUtil
from src.common.pg_impl import PGImplementation
from src.common.enum_utils import ReturnCodes


class Forensics:
    """
    Class that contains functionality for forensics

    """
    def __init__(self):
        # get the app version
        self.app_version: str = os.getenv('APP_VERSION', 'Version number not set')

        # get the environment this instance is running on
        self.system: str = os.getenv('SYSTEM', 'System name not set')

        # set the time limits (seconds)
        self.max_wait: int = int(os.getenv('FORENSICS_MAX_WAIT', '600'))
        self.check_interval: int = int(os.getenv('FORENSICS_CHECK_INTERVAL', '15'))

        # get the log level and directory from the environment.
        log_level, log_path = LoggingUtil.prep_for_logging()

        # create a logger
        self.logger = LoggingUtil.init_logging("iRODS.Forensics", level=log_level, line_format='medium', log_file_path=log_path)

        # specify the DB to get a connection
        # note the extra comma makes this single item a singleton tuple
        db_names: tuple = ('irods-sv',)

        # create a DB connection object
        self.db_info: PGImplementation = PGImplementation(db_names, _logger=self.logger)

    def run(self, run_id: str, run_dir: str) -> int:
        """
        Performs the forensics operation.

        The supervisor will mount the /data directory for this component by default.

        :param run_id: The id of the run.
        :param run_dir: The directory path to use for the forensics operations.

        :return:
        """
        self.logger.info('Forensics version %s start: run_id: %s, run_dir: %s', self.app_version, run_id, run_dir)

        # init the return value
        ret_val: int = ReturnCodes.EXIT_CODE_SUCCESS

        try:
            # make sure the directory exists
            if os.path.isdir(run_dir):
                # init the check counter
                count: int = 0

                # init the flag for processing complete
                keep_running: bool = True

                if sys.platform == 'win32':
                    # get the run ID
                    run_id: str = run_dir.split('\\')[-1]
                else:
                    # get the run ID
                    run_id: str = run_dir.split('/')[-1]

                # try to make the call for records
                run_data: json = self.db_info.get_run_def(run_id)

                # did getting the data to go ok
                if run_data != ReturnCodes.DB_ERROR:
                    # do work
                    while keep_running:
                        # get the list of tests for this run
                        tests_done: int = self.get_tests_done(run_dir, run_data)

                        # were the tests all completed?
                        if tests_done == ReturnCodes.TEST_FOUND_SUCCESS:
                            self.logger.info('End of testing markers found for: %s', run_dir)

                            # gather the test xml file(s)
                            # gather iRODS server log(s)
                            # analyze the results
                            # do something with the results (notifications, persist in a DB...?)

                            # end the processing
                            keep_running = False
                        elif tests_done == 0:
                            # have we exceeded the maximum wait time? default is 40 tries * 15 seconds
                            if (count * self.check_interval) >= self.max_wait:
                                self.logger.error('Max wait time of %s seconds exceeded for run id: %s, run_dir: %s.', self.max_wait, run_id, run_dir)

                                # set the error code
                                ret_val = ReturnCodes.ERROR_TIMEOUT

                                # no need to continue
                                break

                            # increment the counter
                            count += 1

                            # keep waiting for the file that signifies testing complete
                            time.sleep(self.check_interval)
                        else:
                            self.logger.info('Warning No tests found for run id: %s, run_dir: %s, status %s.', run_id, run_dir, tests_done)

                            # this is not an error per se, so exit normally
                            ret_val = ReturnCodes.EXIT_CODE_SUCCESS

                            # no tests, no need to continue
                            break

                # cant work on this unless run data exists
                else:
                    self.logger.error('Error: Request run data was not found for run id: %s, run_dir: %s', run_id, run_dir)
                    ret_val = ReturnCodes.ERROR_NO_RUN_DIR
            # cant work on this unless it exists
            else:
                self.logger.error('Error: Request run_dir was not found forrun id: %s, run_dir: %s', run_id, run_dir)
                ret_val = ReturnCodes.ERROR_NO_RUN_DIR
        except Exception:
            self.logger.exception('Exception: Error processing request for runrun id: %s, run_dir: %s', run_id, run_dir)
            ret_val = ReturnCodes.EXCEPTION_RUN_PROCESSING

        self.logger.info('Forensics complete: run_id: %s, run_dir: %s, ret_val: %s', run_id, run_dir, ret_val)

        # return to the caller
        return ret_val

    @staticmethod
    def get_tests_done(run_dir: str, run_data: json) -> int:
        """
        Gets the list of run tests requested

        :param run_dir:
        :param run_data:
        :return:
        """
        # init the retval
        ret_val: int = ReturnCodes.TEST_FOUND_FAILURE

        # init the test counter
        count: int = 0

        # get the tests
        tests = run_data['request_data']['tests']

        # if there were no tests for this run
        if len(tests) == 0:
            # set a return code to not look any further
            ret_val = ReturnCodes.ERROR_NO_TESTS
        else:
            # for each test in the request list
            for test in tests:
                # get the dict key/value
                for key, value in test.items():
                    # if the end of test marker found, or a test run was specified with no individual tests requested
                    if os.path.isfile(os.path.join(run_dir, f'{key}_tests.complete')) or len(value) == 0:
                        # increment the found counter
                        count += 1

            # were all the tests discovered?
            if len(tests) == count:
                # set the success return code
                ret_val = ReturnCodes.TEST_FOUND_SUCCESS

        # return to the caller
        return ret_val
