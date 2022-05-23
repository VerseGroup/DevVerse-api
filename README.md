# DevVerse

DevVerse is a simple and open-source extension for GitHub that allows users to more effectively interact with GitHub. It is a companion to the GitHub Mobile app and provides features such as project boards (intergrated from GitHub), repository access and text message notifications. All authentication is handled by GitHub with OAuth. 

Services that DevVerse provides:
- Oauth integration with GitHub. No passwords needed.
- Automatic notifications from Twilio based off of GitHub API.
- Note storage through progress board
- Repository access

Built with:
- fastAPI in python 
- Postgresql in heroku and psycopg2 
- Heroku Cloud Container Hosting and Heroku Postgres 
- Docker and docker-compose

Connections:
- GitHub API (central to app purpose)
- Twilio API (for notifications)

The code is open-source and documentation is available on the Github page (versegroup.github.io/devverse/).

