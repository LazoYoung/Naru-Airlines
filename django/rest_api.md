# REST API
## Authentication
| URL                                       | Name                    | Method | Form                       |
|-------------------------------------------|-------------------------|--------|----------------------------|
| `api/auth/login/`                         | `login`                 | POST   | email, password            |
| `api/auth/logout/`                        | `logout`                | POST   |                            |
| `api/auth/reset-password/`                | `reset_password`        | POST   | email                      |
| `api/auth/change-password/`               | `change_password`       | POST   | old_password, new_password |
| `api/auth/register/`                      | `register`              | POST   | email, password            |
| `api/auth/send-register-email/`           | `send_register_email`   | POST   | email                      |
| `api/auth/verify-register/<uid>/<token>/` | `verify_register_email` | GET    |                            |
| `api/auth/profile/`                       | `profile`               | GET    |                            |
| `api/auth/profile/`                       | `profile`               | PUT    | display_name, email        |
