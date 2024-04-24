import time
import requests

# RabbitMQ management plugin details
rabbitmq_host = 'localhost'
rabbitmq_port = 15672  # Default management plugin port
rabbitmq_user = 'guest'
rabbitmq_pass = 'guest'


def check_rabbitmq_connections():
    url = f"http://{rabbitmq_host}:{rabbitmq_port}/api/connections"
    try:
        response = requests.get(url, auth=(rabbitmq_user, rabbitmq_pass))
        if response.status_code == 200:
            connections = response.json()
            # print(connections)
            total_consumers = 0
            for connection in connections:
                total_consumers += connection['channels']
            print(f"Total Consumers: {total_consumers}")
            for connection in connections:
                host = connection.get('host')
                name = connection.get('name')
                print(f"Host: {host}, Name: {name}")
        else:
            print("Failed to fetch RabbitMQ connections")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    while True:
        check_rabbitmq_connections()
        time.sleep(5)  # Check every 5 seconds
