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

## Flight dispatcher
| URL                             | Method | Description                      | Form                                                                                  |
|---------------------------------|--------|----------------------------------|---------------------------------------------------------------------------------------|
| `api/dispatch/charter/`         | POST   | Submit charter flight schedule.  | flight_number, callsign, aircraft, departure_time, departure_airport, arrival_airport |
| `api/dispatch/standard/`        | POST   | Submit standard flight schedule. | flight_number, callsign, departure_time                                               |
| `api/schedules/`                | GET    | Get your flight plans.           |                                                                                       |
| `api/schedule/<flight_number>/` | GET    | Get one specific plan.           |                                                                                       |
| `api/schedule/<flight_number>/` | PUT    | Revise the flight plan.          | callsign, aircraft, departure_time, departure_airport, arrival_airport                |
| `api/schedule/<flight_number>/` | DELETE | Cancel the flight plan.          |                                                                                       |

## Standard route
| URL                          | Method | Description                                                      | Form | Query         |
|------------------------------|--------|------------------------------------------------------------------|------|---------------|
| `api/routes/`                | GET    | Get standard routes. Routes taken come after the available ones. |      | dep, arr, acf |
| `api/route/<flight_number>/` | POST   |                                                                  |      |               |

## Fleet
| URL                               | Method | Description                 | Form                                 |
|-----------------------------------|--------|-----------------------------|--------------------------------------|
| `api/fleet/all/`                  | GET    | Get all aircraft profiles.  |                                      |
| `api/fleet/aircraft/<icao_code>/` | GET    | Get one aircraft profile.   |                                      |
| `api/fleet/aircraft/`             | POST   | Create an aircraft profile. | icao_code, registration, name, image |
| `api/fleet/aircraft/<icao_code>/` | PUT    | Modify an aircraft profile. | registration, name, image            |
| `api/fleet/aircraft/<icao_code>/` | DELETE | Delete an aircraft profile. |                                      |

## Booking
| URL              | Method | Description                      | Form |
|------------------|--------|----------------------------------|------|
| `api/timetable/` | GET    | Get timetable of future flights. |      |
