# Microservices communication using RabbitMQ

# Introduction:
In large-scale businesses like Amazon, Flipkart, and Zepto, inventory management systems are crucial for ensuring efficient stock levels, order processing, and overall inventory control. Key considerations for such systems include:
* Scalability: Handle millions of transactions seamlessly, up to 10000 DB reads/s and up to 2000 DB writes/s
* High Availability: Ensure minimal downtime.
* Consistency: Maintain accurate stock levels across multiple locations, multiple caches, and maybe in multiple DBs.
* Performance: Fast response times for stock queries and updates.
* Failure Tolerance/Recovery: Recover gracefully from failures.
* Security: Protect inventory data and ensure authorized access for certain operations such as updating inventory levels/ adding new items.

# Key Features of Large-Scale Inventory Management Systems(Part of Amazon, Flipkart, Zepto, etc):
* Microservices Architecture: Decoupled services for flexibility and independent service testing, scaling and deployments.
* Asynchronous Communication: Using message brokers like RabbitMQ or Kafka for efficient, decoupled inter-service communication.
* Distributed Databases: Using polyglot persistence (multiple DBs) for optimal performance across various data operations.
* Event-Driven Design: Implementing event sourcing and CQRS for real-time inventory updates and separate read/write operations. This way we can incentivise DB reads. A master-slave architecture with eventual consistency like Cassandra can be used as read DB. The write DB can be something that supports stronger consistency like PostgreSQL. Sync between these DBs can be done using a message broker like rabbitMQ/ Kafka.
* Advanced Monitoring: Comprehensive monitoring of health and performance of different Microservices and alerting with tools like Prometheus and Grafana.


# Our System and Its Features
Our inventory management system is a simplified version, designed to demonstrate core concepts of microservices communication using RabbitMQ.
* Producer Service: Sends order details via RabbitMQ for asynchronous processing.
* Order Processing Microservice: Processes orders and updates the MongoDB database directly using 1-Phase-Commit
* Inventory Management Services - add_item_consumer, stock_management_consumer: Admin-restricted services for adding, modifying, and deleting inventory items.
* Health Monitoring Service: Implemented a Multithreaded Health Check Server with the main thread using RabbitMQ APIs to detect disconnected services, while another thread monitored the producer service by polling every 5s.

# Scaling and Enhancing Our System
* Enhanced Scalability:
  - Load Balancing: We can implement load balancers to distribute incoming requests evenly across multiple instances.
  - Auto-Scaling: We can use tools like Kubernetes for dynamic scaling based on load.
* Improved Data Consistency:
  - Distributed Transactions: Instead of direct 1PC transactions we can use 2PC or 3PC protocols to ensure stronger data consistency.
  - Event Sourcing and CQRS: Read and write operations can be separated logically by having a readDB and a writeDB. This gives better performance(faster reads, more consistent writes) and scalability.
* Advanced Monitoring and Logging:
  - Centralized Logging: We can use ELK (Elasticsearch, Logstash, Kibana) stack for centralized log management. ELK Stack is an Open Source Distributed monitoring solution and Log management solution.
  - Real-Time Monitoring: Prometheus and Grafana can be used for real-time metrics, health and performance monitoring, and alerting.
* API Gateway: We can use an API gateway for securing microservice endpoints and managing API traffic. An API gateway can serve many purposes such as: authorization, data transformation, request validation, request rate limiting, routing, and load balancing.
* Additional Functionalities which can be added:
  - Search Engine: We can implement a search engine like Elasticsearch for fast and efficient searching and filtering of inventory items.
  - Distributed Caching: We can use Redis or Memcached to cache frequently accessed data, reducing database load and improving response times.
  - Data Partitioning and Sharding: We can implement data sharding to distribute data across multiple databases or nodes, improving performance and scalability.
    The sharding strategy in our simple DB model:
    eg:
    `"watches" Collection`: shard based on brand(hash-based), price-range (range-based). Sharding based on brand distributes inventory items across shards by brand, allowing for efficient queries related to specific brands and balancing the load based on brand popularity.
    A sharding key must be chosen such that it evenly distributes data across shards to avoid hotspots and also aligns with common query patterns
  - Indexing: Indexing is a crucial technique for improving query performance in databases. For example, in the watches collection, creating an index on the brand field allows for faster retrieval of watches by brand, reducing the time required for queries that filter by brand. 

# ScreenShots

**Register/Login Pages:**

![Login/Register Frontend](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/7286a959-8fa6-49c4-acb7-139086086904)

**Admin Dashboard:**

![Admin Dashboard](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/591df5e2-51f7-4eda-9fac-8d68f8cecaf7)

**Add Item:**

![AddItem1](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/8ff4fb52-bc3a-414f-ac9e-a27eab31fe8b)
![AddItem2](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/6450d1c0-8153-494b-8d8b-6d9c0bf04d37)
![AddItem3](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/f428d61c-8d52-470b-b290-c5dcaec5c9df)

**Modify existing Stock:**

![UpdateStock1](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/e982627d-02b4-49db-b444-2313e2e91d0c)
![UpdateStock2](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/4c6bdafe-e6a0-4fbe-9294-c96b37a6bc1f)
![UpdateStock3](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/253107a2-71ef-40e8-9a76-0a107444c642)

**Remove Stock:**

![Remove1](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/e7e637fa-daec-4f34-bb91-012f62c967c6)
![Remove2](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/b6901b11-651f-4269-96d8-648e45d8e20b)

**User Dashboard:**

![UserDashboard](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/c179e318-b408-4319-9728-cc56ebe0be05)

**User Order Processing:** includes backend handling of edge cases when there is limited stock available(<1)

![OrderProc1](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/9d1cb4c7-576a-4e79-b012-ff61fa829391)
![OrderProc2](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/f3b4bb1a-06dc-47af-aa51-a88545632114)

**Server side health check**: for consumer1 :item creation, consumer2 : stock processing, consumer3: order processing and producer servers

![HealthCheck1](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/b509af97-562a-42e3-820c-b48c76e34da7)

When consumer 1 is down:

![Down1](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/08c4dbfd-0c78-4d14-9279-171ec1324618)
![Down2](https://github.com/Akatsuki49/558_559_587_609_3/assets/95576716/190a392d-d232-4913-a78c-d81847abc39f)

# Tech Stack:
* Flask: Micro web framework written in Python for building microservices.
* RabbitMQ: A MessageBroker: used For asynchronous, decoupled communication between microservices.
* Pika: Python library for interacting with RabbitMQ.
* MongoDB: A NoSQL documentDB used as the inventoryDB to persist inventory stock data and other purposes
* Docker: Containerization for consistent deployment and scalability.












