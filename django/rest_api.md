# REST API
## Authentication
| URL                              | Name                          | Method | Form                                       |
|----------------------------------|-------------------------------|--------|--------------------------------------------|
| `auth/login`                     | `rest_login`                  | POST   | email, password                            |
| `auth/logout`                    | `rest_logout`                 | POST   |                                            |
| `auth/password/reset`            | `rest_password_reset`         | POST   | email                                      |
| `auth/password/reset/confirm`    | `rest_password_reset/confirm` | POST   | uid, token, new_password1, new_password2   |
| `auth/password/change`           | `rest_password_change`        | POST   | new_password1, new_password2, old_password |
| `auth/registration`              | `rest_register`               | POST   | email, password1, password2                |
| `auth/registration/verify-email` | `rest_verify_email`           | POST   | key                                        |
| `auth/registration/resend-email` | `rest_resend_email`           | POST   | email                                      |
