<!--
BSD 3-Clause All rights reserved.

SPDX-License-Identifier: BSD 3-Clause
-->

[![iRODS](iRODS-Logo.png)](https://irods.org)

# iRODS-K8s Forensics
The iRODS-K8s Forensics workflow step microservice.

#### License.
[![BSD License](https://img.shields.io/badge/License-BSD-orange.svg)](https://github.com/irods-contrib/iRODS-K8s-forensics/blob/main/LICENSE)

#### Components and versions.
[![Python](https://img.shields.io/badge/Python-3.12.5-orange)](https://github.com/python/cpython)
[![Linting Pylint](https://img.shields.io/badge/Pylint-%203.2.6-yellow)](https://github.com/PyCQA/pylint)
[![Pytest](https://img.shields.io/badge/Pytest-%208.3.2-blue)](https://github.com/pytest-dev/pytest)

#### Build status...
[![PyLint the codebase](https://github.com/irods-contrib/iRODS-K8s-forensics/actions/workflows/pylint.yml/badge.svg)](https://github.com/irods-contrib/iRODS-K8s-forensics/actions/workflows/pylint.yml)
[![Build and push the Docker image](https://github.com/irods-contrib/iRODS-K8s-forensics/actions/workflows/image-push.yml/badge.svg)](https://github.com/irods-contrib/iRODS-K8s-forensics/actions/workflows/image-push.yml)

## Description.
The iRODS-K8s Forensics product is a microservice used in an iRODS K8s Supervisor workflow step to analyze and summarize 
the results of tests performed.

### There are GitHub actions to maintain code quality in this repo:
 - Pylint (minimum score of 10/10 to pass),
 - Build/publish a Docker image.

### How to build the Docker image for this product.

The Docker image must be placed in a container image registry and referenced in the Job supervisor configuration database table.

```shell
docker build --build-arg APP_VERSION=<version> -f Dockerfile -t irods-forensics :latest . 
```
