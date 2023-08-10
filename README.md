# SafePass – A simple password manager!
## Introduction
This repository was submitted as the final project for CS50X 2023 online course offered by Harvard University. It’s a web application built around Flask’s framework and some software development/web programming languages covered by the course, such as Python, JavaScript, SQL, HTML and CSS. The application is designed for storing passwords.

The central component of the application is the **password vault**, where the user can **store**, **retrieve**, **upload** and **delete** their credentials, which encompass domains, usernames, and passwords. To enable these interactions, the main application is **supported by additional files**, that contain **utilities** and **security** functions.

The project files follow the layout guidelines of [Flask](https://flask.palletsprojects.com/en/2.3.x/tutorial/layout/), but in a simplified manner. The root files are `app.py`, `helpers.py`, `security.py` and `schema.sql`, serving as the **backend** of the application. Regarding the **frontend**, it is divided into two folders: `static` and `templates`. These folders host user-interactive functionality scripts, a style sheet and svgs, and HTML content, respectively.

## BackEnd
### [`app.py`](/app.py)
This file is where most of the server logic resides. The first lines of code (1-25) start with the usual import declarations, some server configurations, the definition of the server Fernet key[^1], which is a binary string used for encryption, and a function for closing the database connection when the application context[^2] is popped.
[^1]: For more information about the encryption method, check out [cryptography.fernet](https://cryptography.io/en/latest/fernet/).
[^2]: Application context is defined [here](https://flask.palletsprojects.com/en/2.3.x/appcontext/#the-application-context).

The next lines of code refer to the different routes of the application:
- `register`
- `login`
- `index`
- `import_file`
- `change_password`
- `change_master_password`
- `delete_account`
- `logout`

#### `register`

### `helpers.py`
### `security.py`
### `schema.sql`

## FrontEnd
### `static`
#### JavaScript
#### CSS
### `templates`
#### Layout

## Room for improvement and Vulnerabilities

## Sources
 
