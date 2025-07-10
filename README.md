This is a personal project built with the Django framework for learning purposes. It was a significant learning experience, particularly in experimenting with various technologies. To handle real-time interactions, I implemented WebSocket functionality using Django Channels (ASGI) alongside JavaScript (refer to lobby.html and consumers.py). The site is entirely in Portuguese, targeting Brazilian players, as this was my primary audience. Given my familiarity with MySQL, I used it as the database for this project. For guidance on setting up MySQL with Django, see this DigitalOcean tutorial.

## About

This project draws inspiration from IXDL and FACEIT. From its inception, I was captivated by the idea of enabling users to create their own Dota 2 in-house leagues on a single platform. The concept took root after learning about Ixmike88's IXDL platform , which allowed anyone to host their own league for a fixed monthly fee.

## Functionalities

Inspired by IXDL, this project incorporates many of its core features, including:

Individual Leagues: Each league has its own ranking system.
Steam API Authentication: For secure user login and integration.
Profile Page: Currently under development.
Dota 2 Bots: Used to manage and receive events from the matchmaking system.
Entrance Fee System: In progress, not yet completed.
