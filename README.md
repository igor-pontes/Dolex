# Dolex
This is a personal project for learning purposes only. I learned A LOT messing around with this one. 
I used Django 2.2.5 so I could learn more about Python and its applications.
WebSocket requests were inevitable so I used Django ASGI (https://channels.readthedocs.io/en/latest/introduction.html) and some Javascript(obviously?) to handle all of those (see lobby.html and consumers.py).
Made this site entirely in portuguese because my target was all the Brazilians players.
(If I really needed to I could easily make something similar for CSGO too)
Since I very familiarizied with MysQL I took use of it in this project too. (See https://www.digitalocean.com/community/tutorials/how-to-create-a-django-app-and-connect-it-to-a-database for more info on how to use mysql+django)
## About
This project was entirely inspired by Ixdl and Faceit. Since the beginning of its creation I was fascinated by the idea that people could create their own Dota2 inhouse leagues all on an unique website. This idea was growing in me since Ixmike88(https://liquipedia.net/dota2/Ixmike88) made his Ixdl platform where anyone could simply host their own league by only paying him a fixed price per month.

## Functionalities
As I said before, this project was entirely inspired by Ixdl so it has almost all functionalities this platform has. For example:

- Create individual leagues where each one of them have their own ranking system.
- Login with your Steam account (used steamauth(https://github.com/blurfx/django-steamauth) package for that).
- Profile page (Unfinished :@)
- Dota 2 bots so we can see all the info we need about the matches(eg. bot can send info if team A lost or not and if so the website can lower points from all players of team A).
- You can set up an entrance fee so players who are interested in joining your league will need to pay you first. (Unfinished :@)


If you intend to use this you can send me an email at igoppop@gmail.com so I can help you. (I do not guarantee I will answer)
