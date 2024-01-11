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

from src.common.logger import LoggingUtil


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
        self.max_wait_time: int = 400
        self.check_interval_wait: int = 15

        # get the log level and directory from the environment.
        log_level, log_path = LoggingUtil.prep_for_logging()

        # create a logger
        self.logger = LoggingUtil.init_logging("iRODS.Forensics", level=log_level, line_format='medium', log_file_path=log_path)

    def run(self, run_dir: str) -> int:
        """
        Performs the forensics operation.

        The supervisor will mount the /data directory for this component by default.

        :param run_dir: The directory path to use for the forensics operations.

        :return:
        """
        # init the return value
        ret_val: int = 0

        # make sure the directory exists
        if os.path.isdir(run_dir):
            # init the check counter
            count: int = 0

            # init the flag for processing complete
            keep_running: bool = True

            # do work
            while keep_running:
                # is the file there that marks the testing is complete?
                if not os.path.isfile(os.path.join(run_dir, 'PROVIDER_tests.complete')):
                    # have we exceeded the maximum wait time?
                    # 40 tries * 15 seconds
                    if (count * self.check_interval_wait) >= self.max_wait_time:
                        self.logger.error('Max wait time of %s seconds exceeded.', self.max_wait_time)

                        # set the error code
                        ret_val = -98

                        # no need to continue
                        break

                    # increment the counter
                    count += 1

                    # keep waiting for the file that signifies testing complete
                    time.sleep(self.check_interval_wait)
                else:
                    self.logger.debug('End of testing marker found.')

                    # TODO: parse the files
                    # TODO: analyze the results
                    # TODO: do something with the results

                    # end the processing
                    keep_running = False

        # cant work on this unless it exists
        else:
            ret_val = -99

        # return to the caller
        return ret_val
