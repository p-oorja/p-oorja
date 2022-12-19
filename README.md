#To build the docker image run the following command:
docker-compose build

#To run the docker image:
docker-compose up -d

#To see the api logs:
docker-compose logs -f api

#To see the celery worker logs:
docker-compose logs -f celery_worker

#Test end points with curl:
curl http://127.0.0.1:5000/api/v1/test/flask
curl http://127.0.0.1:5000/api/v1/test/test_celery
