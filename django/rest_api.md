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
| URL                             | Method | Description                      | Form                                                                      |
|---------------------------------|--------|----------------------------------|---------------------------------------------------------------------------|
| `api/dispatch/charter/`         | POST   | Submit charter flight schedule.  | aircraft, flight_time, departure_time, departure_airport, arrival_airport |
| `api/dispatch/standard/`        | POST   | Submit standard flight schedule. | flight_number, aircraft                                                   |
| `api/schedules/`                | GET    | Get your flight schedules.       |                                                                           |
| `api/schedule/<flight_number>/` | GET    | Get one specific schedule.       |                                                                           |
| `api/schedule/<flight_number>/` | DELETE | Cancel the flight schedule.      |                                                                           |

## Standard route
| URL                          | Method | Description              | Form / Response                                             |
|------------------------------|--------|--------------------------|-------------------------------------------------------------|
| `api/routes/`                | GET    | Get all standard routes. |                                                             |
| `api/route/<flight_number>/` | GET    | Get one standard route.  |                                                             |
| `api/route/`                 | POST   | Create a standard route. | flight_number, aircraft, departure_airport, arrival_airport |
| `api/route/<flight_number>/` | PUT    | Modify a standard route. |                                                             |
| `api/route/<flight_number>/` | DELETE | Delete a standard route. |                                                             |

## Fleet
| URL                               | Method | Description                 | Form                                 |
|-----------------------------------|--------|-----------------------------|--------------------------------------|
| `api/fleet/profiles/`             | GET    | Get all aircraft profiles.  |                                      |
| `api/fleet/aircraft/<icao_code>/` | GET    | Get one aircraft profile.   |                                      |
| `api/fleet/aircraft/`             | POST   | Create an aircraft profile. | icao_code, registration, name, image |
| `api/fleet/aircraft/<icao_code>/` | PUT    | Modify an aircraft profile. | registration, name, image            |
| `api/fleet/aircraft/<icao_code>/` | DELETE | Delete an aircraft profile. |                                      |

## Booking
| URL              | Method | Description                      | Form |
|------------------|--------|----------------------------------|------|
| `api/timetable/` | GET    | Get timetable of future flights. |      |
