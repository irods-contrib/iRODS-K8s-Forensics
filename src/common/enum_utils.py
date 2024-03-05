# BSD 3-Clause License All rights reserved.
#
# SPDX-License-Identifier: BSD 3-Clause License

"""
    Enum utilities.

    Author: Phil Owen, 01/30/2024
"""

from enum import Enum


class ReturnCodes(int, Enum):
    """
    Class enum for error codes
    """
    EXIT_CODE_SUCCESS = 0
    TEST_FOUND_FAILURE = 0
    TEST_FOUND_SUCCESS = 1
    DB_ERROR = -1
    EXCEPTION_RUN_PROCESSING = -99
    ERROR_TIMEOUT = -98
    ERROR_NO_RUN_DIR = -97
    ERROR_NO_RUN_DATA = -96
    ERROR_NO_TESTS = -95
