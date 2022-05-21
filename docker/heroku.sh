heroku login
heroku container:login

echo "Building image..."
docker buildx build --platform linux/amd64 -t devverse-server .
docker tag devverse-server registry.heroku.com/devverse-server/web
docker push registry.heroku.com/devverse-server/web

echo "Deploying image to heroku..."
heroku container:release web -a devverse-server
