# BSD 3-Clause All rights reserved.
#
# SPDX-License-Identifier: BSD 3-Clause

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

    TEST_RESULTS_NOT_FOUND = 0
    TEST_RESULTS_FOUND = 1

    DB_ERROR = -1

    EXCEPTION_RUN_PROCESSING = -99

    RESULT_PARSE_SUCCESS = 0

    ERROR_TIMEOUT = -98
    ERROR_NO_RUN_DIR = -97
    ERROR_NO_RUN_DATA = -96
    ERROR_NO_TESTS = -95
    ERROR_RESULT_PARSE_FAILURE = -94
    ERROR_NO_RESULT_DIR = -93
    ERROR_NO_RESULT_DATA = -92
