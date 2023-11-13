# PizzaWebsite Project

## Introduction

The PizzaWebsite project is an innovative solution designed for "Mario and Luigi's Pizzas," aimed at enhancing the efficiency and accuracy of pizza ordering and delivery processes.

## Problem Statement

The inability of customers to place orders remotely and the error-prone manual order handling system at Mario and Luigi's Pizzeria necessitated a technological intervention.

## Project Goals

- Develop a proof-of-concept for an automated pizza ordering and delivery system.
- Demonstrate the efficiency of an IT solution in managing increased customer orders.
- Improve workflow to support a growing customer base without errors.

## Key Features

1. **Customer Registration and Login**: Streamlines the ordering process by personalizing user experience.
2. **Interactive Dashboard**: Enables staff to efficiently manage orders and the pizza-making process.
3. **Order Tracking**: Provides real-time updates on order status to both customers and staff.
4. **Smart Oven Integration**: Employs Arduino technology for real-time monitoring of pizza readiness and oven temperature.

## Technical Stack

- **Frontend**: HTML, CSS
- **Backend**: Python (Flask)
- **Database**: MongoDB
- **Hardware Integration**: Arduino for Smart Oven functionality

## Project Structure

- `main.py`: Contains Flask routes and business logic.
- `templates/`: HTML files for the web interface.
- `static/`: CSS and image assets.
- `project-plan.md` & `team-charter.md`: Project documentation.

## Smart Oven Functionality

The Smart Oven feature, integrated with Arduino, is a crucial part of this project. It uses digital output pins to control LEDs and a buzzer, indicating the oven's status (empty, cooking, done). The `oven_cooking()` function randomly sets a cooking time, during which the yellow LED is on. Once cooking is complete, the green LED lights up, and the buzzer sounds, signaling that the pizza is ready.

## Asynchronous Functions in Python

Asynchronous functions in `main.py` are used for non-blocking operations, particularly in the Smart Oven feature. The `asyncio` library allows the program to perform other tasks while waiting for the oven to complete cooking, enhancing efficiency and responsiveness.

## JavaScript and MongoDB Integration

JavaScript is used for dynamic client-side interactions, particularly in updating order statuses on the dashboard. MongoDB, accessed through Python using the `pymongo` library, serves as the backend database, storing customer orders, product details, and session information.

## How to Run

1. **Clone the Repository**: `git clone https://github.com/nixxxo/PizzaWebsite.git`
2. **Install Dependencies**: Navigate to the project directory and install required Python packages: `pip install -r requirements.txt`
3. **Set Environment Variables**: Define necessary environment variables, such as `MONGO_DB_LINK` for MongoDB connection.
4. **Run the Flask App**: Execute `python main.py` to start the Flask server.
5. **Access the Web Interface**: Open a web browser and navigate to `http://localhost:5000`.

## Future Enhancements

- Expand pizza customization options.
- Implement real-time GPS tracking for deliveries.
- Utilize AI for predictive order management.
