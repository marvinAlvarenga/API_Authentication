# API_Authentication

This project tries to show how to implement authentication into an API in a deacoupled way.

You can build one module per authentication service you want to use (Google authentication module is already done) and
integrate it using the created services as interfaces.

## Features

- Provide a module with endpoints and services to authenticate using a Google
  Account.
- Extend [Simple JWT Module](https://github.com/SimpleJWT/django-rest-framework-simplejwt) to support Token tracking in DB. This backend has
  to be used by any authentication module like Google App to provide on
  site tokens.
- Provide services to register and retrive an user.

## Extra

Permission app could be named in a different way (User app could be more appropriate).
