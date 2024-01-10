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

        # get the log level and directory from the environment.
        log_level, log_path = LoggingUtil.prep_for_logging()

        # create a logger
        self.logger = LoggingUtil.init_logging("iRODS.forensics", level=log_level, line_format='medium', log_file_path=log_path)

    @ staticmethod
    def run(run_dir: str) -> int:
        """
        Performs the requested type of forensics operation.

        The supervisor will mount the /data directory for this component by default.

        :param run_dir: The base path of the directory to use for the forensics operations.

        :return:
        """
        # init the return value
        ret_val: int = 0

        # return to the caller
        return ret_val
