# Gravitee API Configuration

Gravitee is an API management system, in 5GCity context will serve the of Authorization enforcement and auditing.

Once the system is running a UI system will be loaded by default on http://localhost:80 to configure the Gravitee
platform. To access the platform use the default credentials:

* username: admin
* password: admin

To add APIs in Gravitee there are two approaches, using the UI creating a new API or Importing an API through the
5GCity-AAA.

## Create New API

Navigating to the Administration and then selecting API the user will have a list of all APIs or a Screen to add the
first API. To create a new API the user should have an OpenAPI spec of the API to ease this process. By choosing the
spec file the API will be automatically imported. The user only has to click on deploy, make the API public and start
it.

## Import API

If the API was already created in the 5GCity context and loaded to the 5GCity-AAA the user can import the API by using 
the import command.

```
$ python main.py gravitee --import_api "Slice Manager API"
```

## Configure API

There are five important menus for API management in Gravitee.

* Portal
* Proxy
* Design


### Portal

Contains the main information about an API, in this section can be set the API access plans, if the API is not public
and the applications that can access it, through subscriptions.

### Proxy

The proxy contains the details on how to access an API,

* **context path** is the path to be used to access an API. Let's
suppose an API has the endpoint /user and in Gravitee the contextpath is temp, in order to access it through Gravitee 
the user must use the following path http://localhost:8000/temp/user, where localhost:8000 is the default 5GCity-AAA 
gravity address.

*  **CORS** is the menu where the administrator can manage the API CORS.
* **Endpoints** is the menu where the user can change the API default location, i.e., if the API port or location change
here is the menu to reflect the change.

### Design

The Design menu allow to change how the endpoints are accessed, i.e., if the administrator needs to change the response
from an endpoint can use the design. It also allows to create resources, such oauth or cache.
