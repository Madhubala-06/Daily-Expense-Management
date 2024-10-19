# Daily Expenses Sharing Application - Backend

## Objective

The Daily Expenses Sharing Application allows users to manage and share daily expenses effectively. This application enables users to add expenses and split them based on three different methods: equal amounts, exact amounts, and percentages. The application manages user details, validates inputs, and generates downloadable balance sheets.

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [API Endpoints](#api-endpoints)
6. [Database Schema](#database-schema)
7. [Validation](#validation)
8. [Running the Application](#running-the-application)

## Features

- **User Management**: Manage user details (email, name, mobile number).
- **Expense Management**: Users can add expenses and split them using:
  - **Equal**: Split equally among all participants.
  - **Exact**: Specify the exact amount each participant owes.
  - **Percentage**: Specify the percentage each participant owes (ensuring the total adds up to 100%).
- **Balance Sheet**: 
  - Display individual and overall expenses.
  - Downloadable balance sheet feature.

### Expense Calculation Examples

1. **Equal Split**:
   - Scenario: You go out with 3 friends. The total bill is 3000. Each friend owes 1000.
2. **Exact Amount**:
   - Scenario: You go shopping with 2 friends and pay 4299. Friend 1 owes 799, Friend 2 owes 2000, and you owe 1500.
3. **Percentage Split**:
   - Scenario: You attend a party with 2 friends and one of your cousins. You owe 50%, Friend 1 owes 25%, and Friend 2 owes 25%.

## Technologies Used

| Technology      | Description                              |
|-----------------|------------------------------------------|
| Python          | Backend programming language             |
| FastAPI         | Web framework for building APIs          |
| SQLAlchemy      | ORM for database interactions            |
| MySQL           | Database management system               |
| Pydantic        | Data validation and settings management  |

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Madhubala-06/Daily-Expense-Management.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Daily-Expense-Management
   ```

3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - For Windows:
     ```bash
     venv\Scripts\activate
     ```
   - For macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set up the environment variable for the database connection:

1. Create a `.env` file in the project root and add the following line:
   ```
   SQLALCHEMY_DATABASE_URL=mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
   ```
   Replace `<username>`, `<password>`, `<host>`, `<port>`, and `<database_name>` with your MySQL database details.

## API Endpoints

### User Endpoints

- Create User:
  - `POST /users`
  - Request Body:
    ```json
    {
      "email": "user@example.com",
      "name": "User Name",
      "mobile": "1234567890"
    }
    ```

- Retrieve User Details:
  - `GET /users/{user_id}`

### Expense Endpoints

- Add Expense:
  - `POST /expenses`
  - Request Body:
    ```json
    {
      "description": "Dinner with friends",
      "amount": 3000,
      "method": "equal",
      "participants": {
        "user_id_1": "1000",
        "user_id_2": "1000",
        "user_id_3": "1000"
      }
    }
    ```

- Retrieve Individual User Expenses:
  - `GET /expenses/user/{user_id}`

- Retrieve Overall Expenses:
  - `GET /expenses`

- Download Balance Sheet:
  - `GET /balance-sheet/{user_id}`

## Database Schema

To set up the database for the application, create the following tables:

### Users Table

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    mobile_number VARCHAR(15),
    hashed_password VARCHAR(255) NOT NULL
);
```

### Expenses Table

```sql
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    description VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    method ENUM('equal', 'exact', 'percentage'),
    date DATETIME DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Expense Details Table

```sql
CREATE TABLE expense_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expense_id INT,
    user_id INT,
    amount_owed DECIMAL(10, 2),
    percentage DECIMAL(5, 2),
    FOREIGN KEY (expense_id) REFERENCES expenses(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Validation

User inputs are validated to ensure:

- Required fields are present.
- Email format is valid.
- Percentages in the percentage split method add up to 100%.

## Running the Application

1. Start the application:
   ```bash
   uvicorn app.main:app --reload
   ```
   This will start the server at `http://127.0.0.1:8000`.

2. Access the application: Open your browser and navigate to `http://127.0.0.1:8000` to start using the application.

