heroku login
heroku container:login

docker buildx build --platform linux/amd64 -t devverse-server .
docker tag devverse-server registry.heroku.com/devverse-server/web
docker push registry.heroku.com/devverse-server/web

heroku container:release web -a devverse-server
