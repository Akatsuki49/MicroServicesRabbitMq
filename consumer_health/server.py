import time
import requests
import threading

# RabbitMQ management plugin details
# rabbitmq_host = 'localhost'
rabbitmq_host = 'rabbitmq'
rabbitmq_port = 15672  # Default management plugin port
rabbitmq_user = 'guest'
rabbitmq_pass = 'guest'

producer_server_url = "http://producer:5000/get_active"


def check_producer_health():
    while True:
        try:
            # Send a GET request to the producer server's health check endpoint
            response = requests.get(producer_server_url)

            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                # The producer server is active
                print("Producer server is active")
            else:
                # The producer server is not active
                print("Producer server is not active")
        except requests.exceptions.RequestException as e:
            # Handle exceptions when sending the request
            print(f"Error checking producer health: {e}")

        # Wait for 5 seconds before checking again
        time.sleep(5)


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


# Start the producer health check thread
producer_health_thread = threading.Thread(target=check_producer_health)
producer_health_thread.start()


if __name__ == '__main__':
    while True:
        check_rabbitmq_connections()
        time.sleep(5)  # Check every 5 seconds
