# BSD 3-Clause All rights reserved.
#
# SPDX-License-Identifier: BSD 3-Clause

"""
    Main entry point for the forensics microservice application
"""
import os
import time
import json

import xml.etree.ElementTree as ElTree

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
                # get the run request record
                run_data: json = self.db_info.get_run_def(run_id)

                # did getting the data to go ok
                if run_data != ReturnCodes.DB_ERROR:
                    # get the test executor run location
                    executor = next(iter(run_data['request_data']['tests']))

                    # get the tests
                    tests_requested = run_data['request_data']['tests'][executor]

                    # if there were tests requested
                    if len(tests_requested) > 0:
                        # init the check counter
                        count: int = 0

                        # init the flag for processing complete
                        keep_running: bool = True

                        # get the full run directory
                        full_run_dir: str = os.path.join(run_dir, run_id)

                        # do work
                        while keep_running:
                            # get the list of tests for this run
                            testing_complete: int = self.get_tests_done(full_run_dir, executor)

                            # were the tests all completed?
                            if testing_complete == ReturnCodes.TEST_RESULTS_FOUND:
                                self.logger.info('End of testing marker found for: %s', full_run_dir)

                                # parse the test reports found in <full_run_dir>\<test executor>\test-reports\
                                ret_val = self.parse_test_reports(run_id, os.path.join(full_run_dir, executor))

                                # no need to continue
                                keep_running = False
                            elif testing_complete == ReturnCodes.TEST_RESULTS_NOT_FOUND:
                                self.logger.info('End of testing marker NOT found for: %s', full_run_dir)

                                # have we exceeded the maximum wait time? default is 40 tries * 15 seconds
                                if (count * self.check_interval) >= self.max_wait:
                                    self.logger.error('Results max wait time of %s seconds exceeded for run id: %s, run_dir: %s.', self.max_wait,
                                                      run_id, run_dir)

                                    # set the error code
                                    ret_val = ReturnCodes.ERROR_TIMEOUT

                                    # no need to continue
                                    break

                                # increment the counter
                                count += 1

                                # keep waiting for the file that signifies testing complete
                                time.sleep(self.check_interval)
                    else:
                        self.logger.error('Error: No tests found for run id: %s, run_dir: %s.', run_id, run_dir)
                        ret_val = ReturnCodes.ERROR_NO_TESTS
                # cant work on this unless run data exists
                else:
                    self.logger.error('Error: Request run data was not found for run id: %s, run_dir: %s', run_id, run_dir)
                    ret_val = ReturnCodes.ERROR_NO_RUN_DIR
            # cant work on this unless it exists
            else:
                self.logger.error('Error: Run data directory was not found for run id: %s, run_dir: %s', run_id, run_dir)
                ret_val = ReturnCodes.ERROR_NO_RUN_DIR
        except Exception:
            self.logger.exception('Exception: Error processing request for run id: %s, run_dir: %s', run_id, run_dir)
            ret_val = ReturnCodes.EXCEPTION_RUN_PROCESSING

        self.logger.info('Forensics complete: run_id: %s, run_dir: %s, ret_val: %s', run_id, run_dir, ret_val)

        # return to the caller
        return ret_val

    @staticmethod
    def get_tests_done(full_run_dir, executor: str) -> ReturnCodes:
        """
        Gets the list of run tests requested

        :param full_run_dir:
        :param executor:
        :return:
        """
        # init the retval
        ret_val: ReturnCodes = ReturnCodes.TEST_RESULTS_NOT_FOUND

        # if the end of test marker found
        if os.path.isfile(os.path.join(full_run_dir, f'{executor}_tests.complete')):
            # set the success return code
            ret_val = ReturnCodes.TEST_RESULTS_FOUND

        # return to the caller
        return ret_val

    def parse_test_reports(self, run_id: str, full_run_dir: str) -> ReturnCodes:
        """
        Parses the test reports

        :param run_id:
        :param full_run_dir:
        :return:
        """
        # init the return
        ret_val: ReturnCodes = ReturnCodes.ERROR_RESULT_PARSE_FAILURE

        # append the test reports directory to the path
        test_reports_dir = os.path.join(full_run_dir, 'test-reports/')

        # check if the directory exists
        if os.path.isdir(test_reports_dir):
            # get the files to parse
            files: list = [file for file in os.listdir(test_reports_dir) if file.endswith('.xml')]

            # were there any xml files?
            if len(files):
                # init the summary data variable
                run_summary: dict = {}

                # for each file in the test results directory
                for file in files:
                    # parse the xml file
                    tree = ElTree.parse(os.path.join(test_reports_dir, file))

                    # get root element of the XML
                    root = tree.getroot()

                    # capture the summary data on the root element in the XML
                    run_summary[root.attrib['name']] = root.attrib

                    # capture the data at these tags if it exists
                    for tag in ['error', 'failure']:
                        # get the data and save it if it exists
                        self.get_tag_data(root, run_summary, tag)

                # persist the summary to the DB
                ret_val = self.db_info.update_run_results(run_id, run_summary)
            else:
                # set the return code
                ret_val = ReturnCodes.ERROR_NO_RESULT_DATA
        else:
            # set the return code
            ret_val = ReturnCodes.ERROR_NO_RESULT_DIR

        # return to the caller
        return ret_val

    @staticmethod
    def get_tag_data(root: ElTree.Element, run_summary: dict, tag: str):
        """
        gets the data at the tag specified

        :param root:
        :param run_summary:
        :param tag:
        :return:
        """
        # get a list of the errors
        data = root.findall(f"./testcase/{tag}")

        # if there were any found
        if data:
            # add on a list for the entries
            run_summary[root.attrib['name']].update({f'{tag}_details': []})

            # for each entry
            for item in data:
                # flatten out the elements
                item.attrib.update({'text': item.text})

                # add the entry into the list
                run_summary[root.attrib['name']][f'{tag}_details'].extend([item.attrib])
