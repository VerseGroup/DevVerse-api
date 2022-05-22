# DevVerse

DevVerse is a simple and open-source extension for Github that allows users to more effectively interact with Github. It is a companion to the Github Mobile app and provides features such as project boards (intergrated from github), repository access and text message notifications. All authentication is handled by Github with oauth.

Services that DevVerse Provides:
- Oauth integration with Github. No passwords needed.
- Automatic Notifications from Twilio based off of github API.
- Note storage through progress board
- Repository access

Built with:
- fastAPI in python 
- Postgresql in heroku and psycopg2 
- Heroku Cloud Container Hosting and Heroku Postgres 
- Docker and docker-compose

Connections:
- Github API (central to app purpose)
- Twilio API (for notifications)

The app was designed for PantherHacks 2022. The code is open-source and documentation is available on the Github page (versegroup.github.io/devverse/).

