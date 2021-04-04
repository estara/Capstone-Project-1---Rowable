# Capstone-Project-1---Rowable

https://rowable.herokuapp.com/

App to let rowers know if it will be safe to row when they want to go out.

Site lets users enter a boathouse they want to row from and a day/time and find out if it will be safe to go out on the water. 

Use wind speed limits for primary safety measure as that has one of the greatest impacts upon safety and is the hardest for many rowers to become familiar with. Also provide reminders to bring lights if it's dark (using sunrise/sunset times) and warnings about special weather such as thunderstorms, squalls, tornadoes, etc.

Users are provided with the time of sunrise/sunset, temperature, wind speed, and weather type.

A list of boathouses is also provided so users can see details such as their addresses and safety limits if the boathouse has been activated. This is a handy function for users so they can check assumptions and provide corrections if necessary for data accuracy.

Users can create an account to select their favorite boathouses for easy reference as well as choose whether to get temperature in C or F. Once they have confirmed their email they can activate a boathouse by entering in the boathouse's timezone and safe wind speed limits. The email confirmation is required as a way to discourage people from knowingly entering bad data.

Boathouse activation can be accessed through a boathouse's details page which can be accessed through the boathouse list. The create a new user page can be accessed through the login page.

API used:

OpenWeather:
https://openweathermap.org/api/hourly-forecast

Primary constraint is only having access to 2 days of hourly weather forecast data on the free API account. If funding can be acquired this can be upgraded to provide predictions further in the future.

Made using Python with Flask, SQLAlchemy, and WTForms. Uses PostgreSQL for the database. Front end is HTML with Jinja.
