# REST API
## Authentication
| URL                           | Name                     | Method | Form                       |
|-------------------------------|--------------------------|--------|----------------------------|
| `auth/login`                  | `login`                  | POST   | email, password            |
| `auth/logout`                 | `logout`                 | POST   |                            |
| `auth/reset-password`         | `reset_password`         | POST   | email                      |
| `auth/reset-password/confirm` | `reset_password_confirm` | POST   | uid, token, new_password   |
| `auth/change-password`        | `change_password`        | POST   | old_password, new_password |
| `auth/register`               | `register`               | POST   | email, password            |
| `auth/register/send-email`    | `send_register_email`    | POST   | email                      |
| `auth/register/verify-email`  | `verify_register_email`  | POST   | key                        |
