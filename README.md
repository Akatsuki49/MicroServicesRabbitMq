# 558_559_587_609_3
Microservices communication using RabbitMQ

* Run Rabbitmq on docker
```docker
docker run --rm -it --hostname my-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management
```
* Create virtualenv and install required modules
```cmd
python -m virtualenv venv
venv/Scripts/activate
pip install -r ./requirements.txt
```
* Run the python frontend
```cmd
python ./server.py
```

* Run docker compose
```cmd
  docker-compose up --build
```

