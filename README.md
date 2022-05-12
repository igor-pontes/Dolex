# Dolex
Built with Django framework.
This is a personal project for learning purposes only. I learned A LOT messing around with this one. 
WebSocket requests were inevitable so I used Django ASGI (https://channels.readthedocs.io/en/latest/introduction.html) and some Javascript to handle all of those (see lobby.html and consumers.py).
Made this site entirely in portuguese for the solely reason that my target was all the Brazilians players.
(If I really needed to I could easily make something similar for CSGO too)
Since I very familiarizied with MysQL I took use of it in this project. (See https://www.digitalocean.com/community/tutorials/how-to-create-a-django-app-and-connect-it-to-a-database for more info on how to set up mysql+django)
## About
This project was entirely inspired by Ixdl and Faceit. Since the beginning of its creation I was fascinated by the idea that people could create their own Dota2 inhouse leagues all on an unique website. This idea was growing in me since Ixmike88(https://liquipedia.net/dota2/Ixmike88) made his Ixdl platform where anyone could simply host their own league by only paying him a fixed price per month.

## Functionalities
As I said before, this project was entirely inspired by Ixdl so it has almost all functionalities this platform has. For example:

- Individual leagues where each one of them have their own ranking system.
- Steam API Authentication
- Profile page (Unfinished :@)
- Dota 2 bots so we can manage and/or receive events from the matchmaking system.
- Entrance fee system. (Unfinished)
