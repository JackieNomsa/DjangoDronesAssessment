// README.md
# Drones
### Introduction
Drones is a api for drones to carry and deliver medication from one point to another
with the options to create a new Drone, Load medication to a Drone, View available Drones,
Check medication loaded on a specific Drone, Check the current battery level on a specific Drone
### Getting started
* Clone this repository [here](https://github.com/JackieNomsa/DjangoDronesAssessment).
* Change into the assessment directory
* Run pip install -r requirements.txt to install all dependancies
* Run "python manage.py test drones.tests.test_drones drones.tests.test_validator" to ensure that the project is functional, all tests should pass
### Usage
  * Run python3 manage.py runserver on the terminal to start the applocation
  * navigate to http://127.0.0.1:8000/ using an api tool like postman
### API Endpoints
| HTTP Verbs | Endpoints                           | Action                                          |
|------------|-------------------------------------|-------------------------------------------------|
| POST       | /register_drone                     | To add a new Drone                              |
| GET        | /available_drones                   | To view all available drones                    |
| GET        | /check_medication/{serial_number}   | To view all medication loaded on a drone        |
| POST       | /load_medication/{serial_number}    | To load medication to drone using serial number |
| GET        | /drone_battery/{serial_number}      | To check the current battery level                         |

