# 5GCity-AAA

## Scope

Authentication, Authorization and Accounting module
traversal to any other 5GCity distributed cloud and radio
platform components.

## Architecture

The current module provides an integrated ecosystem between two opensource solutions.
[Keycloak](https://www.keycloak.org/), for Authentication and [Gravitee.io](https://gravitee.io/), for Authorization
enforcement and auditing.

## Usage

The current application provides a management client for 5GCity-AAA allowing to start and stop the environment and
import and export tools.

### Installation

The presented solution uses python3 as environment and Pipenv to manage its environment.

```
$ sudo dnf install pipenv
```

```
$ pipenv install
```

### Configuration

Currently there are two points of configuration for this solution, the docker compose file and the etc/conf.ini. It's
intended to be developed a single point of configuration for all the ecosystem. 

### Execution

To execute the ecosystem the main.py must be used. Currently it accept three commands,
(i) docker, related the ecosystem management, start and stop, (ii) keycloak related to the authentication solution and
 (iii) gravitee to manage the authorization and audit

```
$ python main.py -h

usage: main.py [-h] {docker,keycloak} ...

Script to manage 5G City AAA

positional arguments:
  {docker,keycloak}

optional arguments:
  -h, --help         show this help message and exit

```