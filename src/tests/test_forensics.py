# SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.
# SPDX-FileCopyrightText: 2023 Renaissance Computing Institute. All rights reserved.
# SPDX-FileCopyrightText: 2024 Renaissance Computing Institute. All rights reserved.
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-License-Identifier: LicenseRef-RENCI
# SPDX-License-Identifier: MIT

"""
    Job supervisor tests.

    Author: Phil Owen, RENCI.org
"""
import os
import pytest

from src.forensics.forensics import Forensics


@pytest.mark.skip(reason="Local test only")
def test_run():
    """
    tests doing the normal operations for initial and final forensics.

    this test requires that DB connection parameters are set

    :return:
    """
    # init the return value
    ret_val: int = 0

    # create the target class
    forensics = Forensics()

    # set a run ID
    run_id: str = '0'

    # set up the test directory
    run_dir: str = os.path.join(os.getenv('TEST_PATH'), run_id)

    # make the call to do an initial stage
    ret_val = forensics.run(run_dir)

    # ensure we got a failure code
    assert ret_val < 0

    # set a run ID
    run_id: str = '3'

    # set up the test directory
    run_dir: str = os.path.join(os.getenv('TEST_PATH'), run_id)

    # make the call to do an initial stage
    ret_val = forensics.run(run_dir)

    # make sure of a successful return code and a json file
    assert ret_val == 0