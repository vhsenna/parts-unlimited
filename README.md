# Parts Unlimited

Parts Unlimited is a RESTful API designed for managing an inventory of parts. This API supports CRUD operations (Create, Read, Update, Delete) on parts and includes an endpoint for analyzing the most common words in part descriptions.

## Description
The Parts Unlimited API allows users to interact with a parts inventory database using Django and Django REST framework. It provides endpoints to create, read, update, and delete parts. Additionally, it offers functionality to analyze part descriptions, identifying the most frequently used words while excluding common stop words. This feature is beneficial for sales teams and data analysts to gain insights into part descriptions.

## Features

### CRUD Operations for Parts
- **List all parts:**
    ```http
    GET /api/parts/
    ```

- **Retrieve a part by ID:**
    ```http
    GET /api/parts/{id}/
    ```

- **Create a new part:**
    ```http
    POST /api/parts/
    ```

- **Update a part by ID:**
    ```http
    PUT /api/parts/{id}/
    ```

- **Delete a part by ID:**
    ```http
    DELETE /api/parts/{id}/
    ```

### Most Common Words Endpoint
Get the five most common words in part descriptions, excluding common stop words.

```http
GET /api/most-common-words/
```

### Interactive API Documentation
Explore and test the API endpoints interactively using the built-in Swagger UI documentation.

- [Swagger UI](http://localhost:8000/docs/)

### Database Management
- **MySQL Integration:** Utilizes MySQL for efficient data handling.
- **Database Migrations:** Easily manage database schema changes using Django migrations.
- **Fixture Data Loading:** Load initial data into the database for quick setup and testing.

### Environment Configuration
- **Environment Variables:** Configure database settings and other configurations using environment variables for flexibility and security.

### **Testing:**
- **Unit Tests:** Ensure API functionality and reliability by running unit tests.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/vhsenna/parts-unlimited.git
cd parts-unlimited
```

### 2. Instal Poetry
```bash
pip install poetry
```

### 3. Install Dependencies
```bash
poetry install
```

### 4. Activate Poetry Virtual Environment
```bash
poetry shell
```

### 5. Configure MySQL Database
1. **Install MySQL:** Ensure MySQL is installed and running.
2. **Create Databases:**
    ```sql
    CREATE DATABASE parts_db;
    CREATE DATABASE test_db;  -- Create a separate database for testing if needed.
    ```

### 6. Configure Environment Variables
Enter MySQL database credentials into the `.env` file.

### 7. Run Migrations
```bash
python manage.py migrate
```

### 8. Load Fixture Data (Optional)
```bash
python manage.py loaddata parts/fixtures/data.json
```

### 9. Running Tests
Execute unit tests to validate API functionality:
```bash
python manage.py test
```

### 10. Run the Development Server
Start the development server to interact with the API:
```bash
python manage.py runserver
```

## Future Improvements
- [ ] Ensure efficient database queries using Django ORM optimizations.
- [ ] Implement caching strategies.
- [ ] Use robust authentication methods like OAuth2 or JWT.
- [ ] Serve the API over HTTPS to encrypt data in transit.
- [ ] Use Docker to containerize the application
