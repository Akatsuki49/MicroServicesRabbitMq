# 558_559_587_609_3
Microservices communication using RabbitMQ

* Run Rabbitmq on docker
```docker
docker run --rm -it --hostname my-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management
```
* Run the python frontend
```cmd
python ./server.py
```

