# REST API
## Authentication
| URL                                 | Name                    | Method | Form                                                           |
|-------------------------------------|-------------------------|--------|----------------------------------------------------------------|
| `api/login/`                        | `login`                 | POST   | email, password                                                |
| `api/logout/`                       | `logout`                | POST   |                                                                |
| `api/register/`                     | `register`              | POST   | email, password                                                |
| `api/send-verify-email/`            | `send_verify_email`     | POST   | email, reason=`register`                                       |
| `api/send-verify-email/`            | `send_verify_email`     | POST   | email, new_email, reason=`change_email`                        |
| `api/send-verify-email/`            | `send_verify_email`     | POST   | email, new_password, confirm_password, reason=`reset_password` |
| `api/verify-account/<uid>/<token>/` | `verify_account`        | GET    |                                                                |
| `api/reset-password/<uid>/<token>/` | `verify_reset_password` | GET    |                                                                |
| `api/change-email/<uid>/<token>/`   | `verify_change_email`   | GET    |                                                                |
| `api/change-password/`              | `change_password`       | POST   | old_password, new_password, confirm_password                   |
| `api/profile/`                      | `profile`               | GET    |                                                                |
| `api/profile/`                      | `profile`               | PUT    | bio, display_name, email, receive_emails                       |
