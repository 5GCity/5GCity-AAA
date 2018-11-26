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

The presented solution uses Docker, **Python 3.7** and pipenv to manage the environment.

Please install Python3.7 and Pipenv according to the desired operating system.

Once Python3.7 and Pipenv are installed run the following command within the project folder to install project
dependencies and the activate the Pipenv.

**Note that the following commands must run within the
project's directory**.


```
$ pipenv install
```

This will activate the Pipenv environment with all its dependencies. To run the script contained in this project the
environment must be activated.

```
$ pipenv shell
```

#### Ubuntu Installation

**Python3.7 Installation**:

```
sudo apt-get install -y build-essential
sudo apt-get install -y checkinstall
sudo apt-get install -y libreadline-gplv2-dev
sudo apt-get install -y libncursesw5-dev
sudo apt-get install -y libssl-dev
sudo apt-get install -y libsqlite3-dev
sudo apt-get install -y tk-dev
sudo apt-get install -y libgdbm-dev
sudo apt-get install -y libc6-dev
sudo apt-get install -y libbz2-dev
sudo apt-get install -y zlib1g-dev
sudo apt-get install -y openssl
sudo apt-get install -y libffi-dev
sudo apt-get install -y python3-dev
sudo apt-get install -y python3-setuptools
sudo apt-get install -y wget

mkdir /tmp/Python37
cd /tmp/Python37

wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
tar xvf Python-3.7.0.tar.xz
cd /tmp/Python37/Python-3.7.0
./configure
sudo make altinstall
```


**Pipenv Installation**
```
pip3.7 install --user pipenv
```

### Configuration

Currently the solution uses the following Ports:

8080: Keycloak

9200: Elasticsearch

8000: Gravitee Gateway

27017: MongoDB

8083: Gravitee Management API

80: Gravitee Management UI

To run the solution it's needed to previously run the following command:

```
$ sudo sysctl -w vm.max_map_count=262144
```

The solution uses the following users:

Service: username:password

Keycloack: admin:admin

Gravitee: admin:admin

5GCity: admin:admin

### Execution

To execute the ecosystem the main.py must be used. Currently it accepts three commands,
(i) docker, related the ecosystem management, start and stop, (ii) keycloak related to the authentication solution and
 (iii) gravitee to manage the authorization and audit. Both keycloak and Gravitee commands are used to to import and
 export environments.

Within the project folder activate the python environment, **Note that the following commands must run within the
project's directory**.

```
$ pipenv shell
```

Check script usage

```
$ python main.py -h

usage: main.py [-h] {docker,keycloak} ...

Script to manage 5G City AAA

positional arguments:
  {docker,keycloak}

optional arguments:
  -h, --help         show this help message and exit

```

To start docker environment

```
$ python main.py docker --start
```

Once a message similar to **"Admin console listening on http://127.0.0.1:9990"** means the environment has started.

To import keycloak realm

```
$ python main.py keycloak --import_realm 5gcity
```

Once the keycloack stars the admin console, message similar to **"Admin console listening on http://127.0.0.1:9990" the
realm was imported** and Ctrl+C can be pressed.

To import Gravitee API

```
$ python main.py gravitee --import_api "Slice Manager API"
```

If no message is displayed everything worked as expected.