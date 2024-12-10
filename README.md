# **Movie Discovery and Analysis Platform**

## **Table of Contents**

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Install and Start MongoDB](#4-install-and-start-mongodb)
  - [5. Install and Start Redis](#5-install-and-start-redis)
- [Configuration](#configuration)
  - [1. Environment Variables](#1-environment-variables)
  - [2. Application Settings](#2-application-settings)
- [Running the Application](#running-the-application)
  - [1. Load Recommendation Data](#1-load-recommendation-data)
  - [2. Start the Flask Application](#2-start-the-flask-application)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Users](#users)
  - [Movies](#movies)
  - [Reviews](#reviews)
  - [Recommendations](#recommendations)
- [Testing](#testing)
  - [1. Run Automated Tests](#1-run-automated-tests)
  - [2. Test Coverage](#2-test-coverage)
- [Deployment](#deployment)
  - [1. Environment Configuration](#1-environment-configuration)
  - [2. Use a Production WSGI Server](#2-use-a-production-wsgi-server)
  - [3. HTTPS Setup](#3-https-setup)
  - [4. Containerization (Optional)](#4-containerization-optional)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)
- [Additional Notes](#additional-notes)
- [Acknowledgements](#acknowledgements)

---

## **Introduction**

The **Movie Discovery and Analysis Platform** is a comprehensive web application that allows users to discover, review, and receive recommendations for movies. It leverages both content-based and collaborative filtering algorithms to provide personalized movie suggestions.

The platform offers a RESTful API built with Flask, integrated with MongoDB for data storage, and utilizes JWT for authentication and authorization.

---

## **Features**

- **User Authentication**: Secure user registration and login with password strength validation and account lockout mechanisms.
- **Movie Management**: CRUD operations for movies, allowing authenticated users to add, update, or delete movie entries.
- **Reviews**: Users can add reviews and ratings to movies, which contribute to the overall average rating.
- **Watchlist**: Users can maintain a personal watchlist of movies they wish to watch.
- **Search and Filtering**: Search movies by title, genre, year, and rating, with pagination support.
- **Recommendations**:
  - **Collaborative Filtering**: Recommends movies based on user similarities and ratings.
  - **Content-Based Filtering**: Suggests movies based on content similarity and user preferences.
- **API Documentation**: Interactive API documentation with Swagger UI.

---

## **Architecture**

The application follows a modular structure with clear separation of concerns:

- **`app.py`**: Application factory that initializes the Flask app and extensions.
- **`routes/`**: Contains all the API route definitions.
  - `user_routes.py`: Routes related to user operations.
  - `movie_routes.py`: Routes related to movie operations.
- **`models/`**: Defines data models and business logic.
- **`extensions/`**: Initializes extensions like database connections, authentication, and rate limiting.
- **`schemas/`**: Contains Marshmallow schemas for input validation.
- **`utils/`**: Utility functions and custom validators.
- **`recommendations/`**: Module for loading and handling recommendation data.

---

## **Technology Stack**

- **Backend Framework**: Flask
- **Database**: MongoDB
- **Authentication**: Flask-JWT-Extended
- **Input Validation**: Marshmallow
- **Rate Limiting**: Flask-Limiter
- **API Documentation**: Flasgger (Swagger UI)
- **Recommendations**:
  - **Content-Based Filtering**: TF-IDF and Cosine Similarity
  - **Collaborative Filtering**: User-based similarity calculations
- **Testing**: Pytest, Flask-Testing

---

## **Prerequisites**

Before setting up the application, ensure you have the following installed:

- **Python 3.9+**
- **MongoDB**
- **Redis** (for rate limiting storage)
- **pip** (Python package installer)
- **Virtualenv** (recommended)

---

## **Installation**

### **1. Clone the Repository**

```bash
git clone https://github.com/yourusername/movie-discovery-platform.git
cd movie-discovery-platform
```

### **2. Create a Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### **3. Install Dependencies**
pip install -r requirements.txt

### **4. Install and Start MongoDB**

Ensure MongoDB is installed and running on your local machine.

- **Install MongoDB**: [Installation Guide](https://docs.mongodb.com/manual/installation/)

- **Start MongoDB**:

  **On macOS and Linux:**

  ```bash
  mongod --config /usr/local/etc/mongod.conf


### **5. Install and Start Redis**

Redis is used by Flask-Limiter for rate limiting storage.

- **Install Redis**: [Installation Guide](https://redis.io/topics/quickstart)

- **Start Redis**:

  ```bash
  redis-server


### **Configuration**
#### **1. Environment Variables**
Create a `.env` file in the project root and set the following environment variables:

# .env

# Flask settings
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key

# Database settings
MONGO_URI=mongodb://localhost:27017/movie_db

# Redis settings
REDIS_URL=redis://localhost:6379/0

#### **2. Application Settings**
Ensure app.py and other modules read configurations from environment variables.



## **Running the Application**
#### **1. Load Recommendation Data**
Before starting the application, ensure that the recommendation data is loaded:

Place the following files in the recommendations/data/ directory:
tfidf_matrix.pkl
cosine_sim_matrix.pkl
movies_features.csv

#### **2. Start the Flask Application**
python app.py

The application will run at http://localhost:2.

## **API  Documentation**
Access the interactive API documentation at:
http://localhost:5000/apidocs

Use the Swagger UI to explore and test the API endpoints.

## **API  Endpoints**
Below is a summary of the main API endpoints. For detailed information, refer to the API documentation.

#### **Authentication**
##### **Register**
POST /users/register

##### **Login**
POST /users/login

##### **Token Refresh**
POST /users/refresh

#### **Users**
##### **Get Watchlist**
GET /users/watchlist

##### **Add to Watchlist**
POST /users/watchlist

##### **Remove from Watchlist**
DELETE /users/watchlist

#### **Movies**
##### **Get All Movies**
GET /movies

##### **Get Movie by ID**
GET /movies/{movie_id}

##### **Add Movie**
POST /movies

##### **Update Movie**
PUT /movies/{movie_id}

##### **Delete Movie**
DELETE /movies/{movie_id}

##### **search Movies**
GET /movies/search

#### **Reviews**
##### **Get Reviews for a Movie**
GET /movies/{movie_id}/reviews

##### **Add Review**
POST /movies/{movie_id}/reviews

#### **Recommendations**
##### **Get Recommendations**
GET /movies/recommendations

#### **Testing**
##### **1.Run Automated Tests**
pytest

##### **2.Test Coverage**
coverage run -m pytest
coverage report -m

## **Deployment**

### **1. Environment Configuration**

Ensure that environment variables are properly configured for the production environment.

### **2. Use a Production WSGI Server**

It's recommended to use a production-grade WSGI server like Gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 app:create_app()
```

#### **Contributing**

Contributions are welcome! Please read the CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

#### **License**
This project is licensed under the MIT License - see the LICENSE.md file for details.

#### **Acknowledgments**
- **Flask**: A lightweight web framework for Python.
- **MongoDB**: A NoSQL database for storing movie data.
- **Flask-JWT-Extended**: A Flask extension for JWT authentication.
- **Marshmallow**: A library for data validation and serialization.
- **Flask-Limiter**: A Flask extension for rate limiting.
- **Flasgger**: A Flask extension for generating API documentation.
- **Flask-Testing**: A Flask extension for testing.
- **Pytest**: A testing framework for Python.
- **Coverage**: A code coverage tool for Python.




---

```bash
git clone https://github.com/yourusername/movie-discovery-platform.git
cd movie-discovery-platform



