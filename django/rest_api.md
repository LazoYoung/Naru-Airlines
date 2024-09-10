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
| URL                             | Method | Description                     | Form                                                                     |
|---------------------------------|--------|---------------------------------|--------------------------------------------------------------------------|
| `api/dispatch/charter/`         | POST   | Submit charter flight schedule. | aircraft, departure_time, block_time, departure_airport, arrival_airport |
| `api/dispatch/routine/`         | POST   | Submit routine flight schedule. | flight_number, aircraft                                                  |
| `api/schedule/`                 | GET    | Get flight schedules.           | departure_airport, arrival_airport, aircraft, date                       |
| `api/schedule?mine/`            | GET    | Get your flight schedules.      | departure_airport, arrival_airport, aircraft, date                       |
| `api/schedule?available/`       | GET    | Get available flight schedules. | departure_airport, arrival_airport, aircraft, date                       |
| `api/schedule/<flight_number>/` | GET    | Get one schedule.               |                                                                          |
| `api/schedule/<flight_number>/` | DELETE | Cancel the schedule.            |                                                                          |

## Standard route
| URL                          | Method | Description          | Form / Response                                                                                        |
|------------------------------|--------|----------------------|--------------------------------------------------------------------------------------------------------|
| `api/route/`                 | GET    | Get standard routes. | departure_airport, arrival_airport, aircraft                                                           |
| `api/route/`                 | POST   | Create a new route.  | flight_number, aircraft, departure_day, departure_zulu, block_time, departure_airport, arrival_airport |
| `api/route/<flight_number>/` | GET    | Get one route.       |                                                                                                        |
| `api/route/<flight_number>/` | PUT    | Modify the route.    |                                                                                                        |
| `api/route/<flight_number>/` | DELETE | Delete the route.    |                                                                                                        |

## Fleet
| URL                      | Method | Description                | Form                                 |
|--------------------------|--------|----------------------------|--------------------------------------|
| `api/fleet/`             | GET    | Get all aircraft profiles. |                                      |
| `api/fleet/`             | POST   | Create a new profile.      | icao_code, registration, name, image |
| `api/fleet/<icao_code>/` | GET    | Get one profile.           |                                      |
| `api/fleet/<icao_code>/` | PUT    | Modify the profile.        | registration, name, image            |
| `api/fleet/<icao_code>/` | DELETE | Delete the profile.        |                                      |

## Booking
| URL              | Method | Description                      | Form |
|------------------|--------|----------------------------------|------|
| `api/timetable/` | GET    | Get timetable of future flights. |      |
