# E-Commerce REST API

A production-style REST API for an e-commerce platform built with Flask, 
SQLAlchemy, and JWT authentication. Features an ML-powered product 
recommendation endpoint using sentence transformers and cosine similarity.

## Tech Stack
- **Backend:** Python, Flask, SQLAlchemy, Flask-Migrate
- **Auth:** JWT (Flask-JWT-Extended), bcrypt
- **ML:** Sentence Transformers (all-MiniLM-L6-v2), scikit-learn
- **Database:** SQLite (development), PostgreSQL (production)
- **Deployment:** Render

## Setup

### 1. Clone the repo
git clone https://github.com/your-username/ecommerce-api.git
cd ecommerce-api

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

### 3. Install dependencies
pip install -r requirements.txt

### 4. Set environment variables
Copy .env.example to .env and fill in your values.

### 5. Run migrations
flask db upgrade

### 6. Start the server
python run.py

## API Endpoints

### Auth
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /auth/register | Register new user | No |
| POST | /auth/login | Login and get token | No |

### Products
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | /products | List all products | User |
| GET | /products?category=electronics | Filter by category | User |
| GET | /products/:id | Get single product | User |
| POST | /products | Create product | Admin |
| GET | /products/:id/recommendations | ML recommendations | User |

### Orders
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /orders | Place an order | User |
| GET | /orders | Get order history | User |
| GET | /orders/:id | Get single order | User |

### Admin
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | /admin/orders | View all orders | Admin |
| PATCH | /admin/orders/:id/status | Update order status | Admin |
| DELETE | /admin/products/:id | Delete product | Admin |

## ML Recommendations

The `/products/:id/recommendations` endpoint uses semantic similarity 
to find related products. Product names and descriptions are encoded 
using the `all-MiniLM-L6-v2` sentence transformer model, and cosine 
similarity is used to rank results.

This means "noise cancelling headphones" and "audio device with sound 
isolation" would score high similarity even with no shared keywords.

## Example Request

POST /auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}

Response:
{
    "access_token": "eyJhbGci...",
    "user": { "id": 1, "email": "user@example.com", "role": "customer" }
}