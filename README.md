Borg Connect - Data Monitoring System: Complete Project Summary
1. Overview
The Borg Connect system is a real-time data monitoring and visualization platform that:
•	Simulates data generation from a Borg Connect Node
•	Processes and aggregates data based on user-defined sampling parameters
•	Stores data in both Redis (for real-time access) and SQLite (for persistence)
•	Provides a dynamic web dashboard with auto-refresh functionality
•	Uses WebSockets for live updates and Redis for configuration management
________________________________________
2. System Architecture
The project consists of three main components:
A. Data Adapter (Backend)
•	Components:
o	borgConnectNode.py: Simulates data generation with random values
o	data_collector.py: Collects data and sends it to RabbitMQ
o	store_data.py: Stores raw data in SQLite
o	main.py: Orchestrates the data collection process
•	Key Features:
o	Continuously generates random data (6 values per second)
o	Publishes data to RabbitMQ (rawqueue)
o	Persists data in SQLite (database.db)
B. Aggregation Service (Backend)
•	Components:
o	aggregateservices.py: Processes raw data from RabbitMQ and computes aggregates
•	Key Features:
o	Supports multiple sampling types (avg, sum, min, max, latest)
o	Stores aggregated results in Redis (with a 5-second expiry)
o	Publishes aggregated data to RabbitMQ (aggregated_queue)
C. Web Dashboard (Frontend)
•	Components:
o	Django-based web interface (views.py, urls.py)
o	WebSocket consumer (consumers.py) for real-time updates
o	Interactive dashboard (dashboard.html) with Chart.js
•	Key Features:
o	User authentication (login.html)
o	Dynamic chart rendering with auto-refresh
o	Controls for sampling type, frequency, and start/stop
________________________________________
3. Data Flow
1.	Data Generation
o	borgConnectNode.py generates random data (6 values per second).
o	data_collector.py sends this data to RabbitMQ (rawqueue).
2.	Data Aggregation
o	aggregateservices.py consumes raw data from RabbitMQ.
o	Computes aggregates based on user-defined sampling type (avg, sum, etc.).
o	Stores results in Redis (key: aggregated_<instance_id>_<timestamp>).
3.	Data Visualization
o	Dashboard connects via WebSocket (ws://<host>/ws/dashboard/).
o	Fetches latest aggregated data from Redis.
o	Updates Chart.js in real-time.
4.	User Controls
o	Start Sampling:
	Saves settings (sampling_type, sampling_freq) to Redis.
	Triggers auto-refresh (page reloads every sampling_freq seconds).
o	Stop Sampling:
	Sets status to stopped in Redis.
	Stops auto-refresh.
________________________________________
4. Key Features & Implementation Details
A. Auto-Refresh Mechanism
•	Trigger: When user clicks Start, the page reloads every sampling_freq seconds.
•	Persistence:
o	User inputs (sampling_type, sampling_freq) are stored in localStorage.
o	On page reload, settings are restored from localStorage.
•	Stopping:
o	Clicking Stop clears the refresh interval.
B. Real-Time Updates with WebSockets
•	WebSocket Endpoint: ws://<host>/ws/dashboard/
•	Initial Data Load:
o	On connection, the dashboard fetches the last 10 aggregated values from Redis.
•	Live Updates:
o	New data points are pushed via WebSocket and added to the chart.
C. Redis for Configuration & Aggregated Data
•	Stored Data:
o	dashboard_settings:
json
{
  "sampling_type": "avg",
  "sampling_freq": 5,
  "status": "running"
}
o	Aggregated data (key format: aggregated_<instance_id>_<timestamp>).
•	Expiry:
o	Aggregated data expires after 5 seconds (configurable).
D. SQLite for Persistent Storage
•	Table Schema (data):
sql
CREATE TABLE IF NOT EXISTS data(
  timestamp INTEGER,
  data_values TEXT,
  instance_id TEXT
)
•	Usage:
o	All raw data is stored here for historical analysis.
________________________________________
5. Backend APIs (Django Views)
Endpoint	Method	Description
/login/	GET/POST	Handles user authentication
/dashboard/	GET	Renders the dashboard
/update_settings/	POST	Updates sampling settings in Redis
/get_settings/	GET	Retrieves current settings from Redis
/ws/dashboard/	WebSocket	Provides real-time data updates
________________________________________
6. Frontend (Dashboard) Features
•	Interactive Controls:
o	Dropdown for sampling_type (avg, sum, min, max, latest).
o	Input for sampling_freq (in seconds).
o	Start/Stop buttons.
•	Dynamic Chart:
o	Shows the last 20 data points.
o	Updates in real-time via WebSocket.
•	Auto-Reload:
o	Page reloads every sampling_freq seconds when sampling is active.
________________________________________
7. Error Handling & Edge Cases
•	Invalid Inputs:
o	If sampling_freq is not a positive number, shows an alert.
•	WebSocket Disconnection:
o	Automatically reconnects if the connection drops.
•	Redis Unavailability:
o	Falls back to default settings if Redis is down.
________________________________________
8. How to Run the Project
1.	Start or create Services:
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
# Django (with Channels)
daphne Borg_front.asgi:application

# Aggregation Service
python Services/aggregateservices.py --samplingtype avg --samplingfreq 5

# Data Adapter
python Adapter/main.py --borg-connect-node node1
2.	Access Dashboard:
o	Open http://localhost:8000/dashboard/
o	Log in (if authentication is enabled)
o	Configure sampling settings and start monitoring.
________________________________________
10. Conclusion
•	The Borg Connect system provides:
•	Real-time data monitoring
•	Customizable aggregation (avg, sum, min, max, latest)
•	Persistent storage (SQLite) + Caching (Redis)
•	Interactive dashboard with auto-refresh
•	Scalable architecture (RabbitMQ for decoupled processing)
