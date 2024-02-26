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
import sys

from argparse import ArgumentParser
from src.forensics.forensics import Forensics

if __name__ == '__main__':
    # Main entry point for the forensics microservice
    #
    # Args expected:
    #    --run_id - The ID of the supervisor run request.
    #    --run_dir - The name of the target directory to use for operations

    # init the return value
    ret_val: int = 0

    # create a forensics object
    forensics_obj = Forensics()

    # create a command line parser
    parser = ArgumentParser()

    parser.add_argument('--run_id', default=None, help='The run identifier.', type=str, required=True)
    parser.add_argument('--run_dir', default=None, help='The name of the run directory to use for the staging operations.', type=str,
                        required=True)

    # collect the params
    args = parser.parse_args()

    # validate the inputs
    if args.run_dir == '':
        # missing 1 or more params
        ret_val: int = -2
    else:
        # do the forensics
        ret_val: int = forensics_obj.run(args.run_id, args.run_dir)

    # exit with the final exit code
    sys.exit(ret_val)
