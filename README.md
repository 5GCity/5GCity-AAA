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

#### Fedora

The presented solution uses python3 as environment and Pipenv to manage its environment.

```
$ sudo dnf install pipenv
```

```
$ pipenv install
```

#### Ubuntu 16.04

##### Altinstall

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


##### Pipenv installation
Install pyenv (project requires Python 3.7.1 not available in Xenial)

```
$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
$ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
$ source .bash_profile
```

Use local Python 3.7.1 in 5GCity-AAA directory:

```
5GCity-AAA$ pyenv install 3.7.1
5GCity-AAA$ pyenv local 3.7.1
```

Setup virtual environment:

```
5GCity-AAA$ python -m venv venv
5GCity-AAA$ source venv/bin/activate
(venv) 5GCity-AAA$ pip install --upgrade pip
```

Use virtual environment pip to install pipenv:

```
(venv) 5GCity-AAA$ pip install pipenv
```

Install pipenv dependencies:

```
(venv) 5GCity-AAA$ pipenv install
```

### Configuration

Currently the configuration is hold in two files:
 
 * etc/conf.ini - File that is used by the python script to perform the import and export both realms and APIs.
 * aaa_compose/compose-aaa.yml - File that is used by docker to mount the environment that will run the solution.


#### conf.ini

Within the conf.ini file there is a single configuration section, gravitee.


##### Gravitee

The gravitee section contains Gravitee Management API access information

* username - Gravitee admin username
* password - Gravitee admin password

#### compose-aaa.yml

This file is a regular docker compose file in yml format containing all needed software configurations to run the AAA
environment, containing three sections "Auxiliary Services",  "GRAVITEE Services" and "Keycloak Services".

##### Auxiliary Services

Composed by a POSTGRES, Mongo and Elasticsearch. All services use the default Docker configurations.
Changes in MongoDB and Elasticsearch must be replicated on the Gravitee variables:

* GRAVITEE_MANAGEMENT_MONGODB_URI
* GRAVITEE_REPORTERS_ELASTICSEARCH_ENDPOINTS_0

Changes on the POSTGRES must be replicated on the Keycloak's section

* DB_ADDR
* DB_DATABASE
* DB_USER
* DB_PASSWORD
* DB_PORT

##### GRAVITEE Services

The gravitee is composed by three components, the gateway, the management api which will manage the Gravitee APIs and 
the UI which is a web interface to configure Gravitee.

More configurations can be found on Gravitee's documentation page:
https://docs.gravitee.io/apim_overview_introduction.html

##### Keycloak Services

Information about configuration can be found on keycloak docker page https://hub.docker.com/r/jboss/keycloak/ 

#### Port Mapping

| Service             | Port          | Network
| -------------       | ------------- | ------------- | 
| MongoDB             | 27017         | Docker        |
| MongoDB             | 27017         | Host          |
| ElasticSearch       | 9200          | Docker        |
| ElasticSearch       | 9200          | Host          |
| POSTGRES            | 5432          | Docker        |
| Gravitee GW         | 8000          | Host          |
| Gravitee Management | 8083          | Host          |
| Gravitee UI         | 80            | Docker        |
| Gravitee UI         | 8092          | Host          |
| keycloak            | 8080          | Host          |
| keycloack           | 8080          | Docker        |


#### User Mapping

| Service       | Username      | Password      |
| ------------- | ------------- | ------------- | 
| Gravitee      | admin         | admin         |
| Keycloak      | admin         | admin         |
| 5GCity        | admin         | admin         |


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

usage: main.py [-h] {docker,keycloak,gravitee} ...

Script to manage 5G City AAA

positional arguments:
  {docker,keycloak,gravitee}

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

Once the keycloak stars the admin console, message similar to **"Admin console listening on http://127.0.0.1:9990" the
realm was imported** and Ctrl+C can be pressed.

To import Gravitee API

```
$ python main.py gravitee --import_api "Slice Manager API"
```

If no message is displayed everything worked as expected.


### Add New Users and Tenant to the platform

According to the current implementation a tenant is a SliceManager OpenStack user, the AAA introduces through Keycloak
an abstraction layer that allows the administrator to add multiple users and roles using a single OpenStack user.
In order to create a tenant the administrator must create a new user on the SliceManager API, the generated user id
will be the tenant id in keycloak, while the SliceManager API username will be Keycloak's tenant name.

To add a new user, the administrator must navigate to keycloak and select the 5GCity realm, then on the users menu must
select "add user". The administrator must fill all the user information and set the email verified. Once the user is
created the administrator must edit the user on the section attributes and add the following attributes:

| Key           | Value                                     |
| ------------- | ----------------------------------------- |
| os_id         | The user_id generated by SliceManager API |
| tenant_label  | The username on the SliceManager API      |

The administrator can also set the credentials for the new user.