# BSD 3-Clause All rights reserved.
#
# SPDX-License-Identifier: BSD 3-Clause

"""
    Job supervisor tests.

    Author: Phil Owen, RENCI.org
"""
import os
import pytest

from src.forensics.forensics import Forensics
from src.common.enum_utils import ReturnCodes


#@pytest.mark.skip(reason="Local test only")
def test_run():
    """
    tests doing the normal operations for initial and final forensics.

    this test requires that DB connection parameters are set

    :return:
    """
    # init the return value
    ret_val: int = ReturnCodes.EXIT_CODE_SUCCESS

    # create the target class
    forensics = Forensics()

    # set a run ID
    run_id: str = '0'

    # set up the test directory
    run_dir: str = os.path.join(os.getenv('TEST_PATH'))

    # make the call to do forensics
    ret_val = forensics.run(run_id, run_dir)

    # ensure we got a failure code
    assert ret_val == ReturnCodes.ERROR_NO_RUN_DIR

    # set a run ID
    run_id: str = '68'

    # set up the test directory
    run_dir: str = os.path.join(os.getenv('TEST_PATH'))

    # make the call to do forensics
    ret_val = forensics.run(run_id, run_dir)

    # make sure of a successful return code and a .complete file
    assert ret_val == ReturnCodes.EXIT_CODE_SUCCESS


@pytest.mark.skip(reason="Local test only")
def test_parse_test_results():
    """
    tests the parsing of a test results xml file
    :return:
    """
    # init the return value
    ret_val: int = ReturnCodes.EXIT_CODE_SUCCESS

    # create the target class
    forensics = Forensics()

    # set a run ID
    run_id: str = '67'

    # set up the test directory
    run_dir: str = os.path.join(os.getenv('TEST_PATH'), 'PROVIDER')

    # make the call to do parse the test results
    ret_val = forensics.parse_test_reports(run_id, run_dir)

    # make sure of a successful return code and a .complete file
    assert ret_val == ReturnCodes.EXIT_CODE_SUCCESS
