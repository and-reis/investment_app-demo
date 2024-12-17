# Investment App Demo

**Disclaimer**:  
This project is a demonstration of my knowledge in backend development, using modern technologies like FastAPI, SQLAlchemy, and Docker. It is **NOT** intended for production use. Some functionalities are incomplete or simulated for security and privacy reasons.  

Do not use this project to perform real trades or manage finances without proper adjustments and validations. The author is not responsible for any misuse of this code.

---

## Project Purpose

The purpose of this application is to showcase my backend development skills through a practical project. By implementing key features of an investment portfolio management system, I aim to demonstrate proficiency in modern technologies, including:

- **FastAPI** for building scalable APIs.
- **SQLAlchemy** for database management.
- **Docker** for containerized development and deployment.

This project emphasizes clean architecture, code organization, and practical application of concepts like authentication, API design, and database migrations.

---

## Key Features

This application includes the following core features:

1. **User Management**:  
   - Role-based access control for three types of users:  
     - **Clients**: View and manage their investment portfolios.  
     - **Managers**: Oversee multiple client portfolios and execute trades.  
     - **Admins**: Manage the system, including user accounts and access levels.  

2. **Portfolio Management**:  
   - Track assets in a portfolio with details like current value, cost basis, and asset allocation.  
   - Perform **buy** and **sell** operations, with automatic calculations of profit/loss.  

3. **Profit and Loss (PnL) Tracking**:  
   - Real-time updates on investment performance, including historical comparisons.  

4. **Price Integration**:  
   - Integration with the Binance API to fetch real-time and historical market data.  

5. **Environment Separation**:  
   - Clear separation between development, testing, and production environments, ensuring secure and reliable workflows.

---

### **Application Scheduler**
The application includes a **scheduler** designed to execute background tasks directly within the application container. While this feature is currently **disabled** by default, it is configured to handle tasks such as:
- **Data Synchronization**: Regularly fetching updated prices or market data.
- **Portfolio Maintenance**: Automatically updating portfolio statistics.

If you wish to enable the scheduler, ensure the following:
1. Update the application configuration to activate the scheduler.
2. Restart the container with the updated configuration.

> **Note**: Running the scheduler inside the application container is ideal for simplicity, but for production environments, consider deploying it as a separate service for better scalability.

---

### Additional Information

#### **Example Scripts Directory**
This project includes a set of example scripts to demonstrate various functionalities, such as:
- **User Management**: Creating and querying users.
- **Portfolio Operations**: Simulating buy/sell trades and retrieving portfolio details.
- **Price Retrieval**: Fetching asset prices via endpoints or directly from the database.

You can find these scripts in the **`examples/`** directory. These examples are designed to help you understand the system's capabilities and how to interact with it programmatically.

--- 

## Tech Stack

The Investment App Demo is built using the following technologies:

1. **FastAPI**  
   - A modern, fast (high-performance) web framework for building APIs with Python, based on standard Python type hints. It was chosen for its developer-friendly features like automatic documentation and high scalability.

2. **SQLAlchemy**  
   - An ORM (Object-Relational Mapping) tool for managing and querying databases.  
   - **Reason for choice**: SQLAlchemy provides database-agnostic capabilities, allowing the system to be independent of the underlying database (e.g., PostgreSQL, MySQL, or SQLite). This flexibility ensures that users can adapt the system to their preferred database solution.  

3. **Pydantic**  
   - Used for data validation and serialization, ensuring reliable request and response handling. Its tight integration with FastAPI simplifies schema validation and type enforcement.  

4. **ccxt**  
   - A versatile library for cryptocurrency trading API integration, supporting multiple exchanges, including Binance.  
   - **Reason for choice**: ccxt allows the system to fetch price data not only from Binance but also from other cryptocurrency exchanges and even stock markets. This flexibility supports future expansion to other asset types like equities or commodities.  

5. **Docker**  
   - For containerized development and deployment, ensuring consistent environments across development, testing, and production. Docker simplifies onboarding for new developers and guarantees reproducible builds.

6. **pytest**  
   - A robust testing framework for Python, used to write and execute unit tests and integration tests. It was chosen for its simplicity and powerful features, ensuring code reliability and reducing bugs during development.

---

## Installation Guide

### Prerequisites

Before starting, ensure you have the following installed on your machine:

1. **Docker and Docker Compose**  
   - Docker simplifies running the application by providing a pre-configured container environment.  
   - You won’t need Python or libraries installed locally if using Docker. This is ideal for users who want to see the app in action without diving into Python setup.

2. **Git**  
   - To clone the repository.

---

### Local Setup (Without Docker)

If you prefer not to use Docker, follow these steps to run the application locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/and-reis/investment-app-demo.git
   cd investment-app-demo
   ```

2. **Install Python dependencies**:
   - Ensure you have Python 3.12+ installed.  
   - Create a virtual environment (optional):
     ```bash
     python -m venv venv
     source venv/bin/activate   # Linux/Mac
     venv\Scripts\activate      # Windows
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Set up environment variables**:
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit the `.env` file and configure variables (e.g., `DATABASE_URL`, `BINANCE_API_KEY`).

4. **Start the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API**:
   Open your browser and go to:
   - Swagger: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

---

### Docker Setup

This project includes a `docker-compose.yml` file that simplifies the setup and execution of the application. Below are the key features and configurations:

---

#### Key Features of `docker-compose.yml`

1. **Execution Modes**:
   - The `EXECUTION_MODE` environment variable defines how the application will run:
     - `test`: Runs the application and executes test scripts in `backend/tests/`.
     - `dev`: Starts the application for development, using a database inside the container and syncing local code changes with the container.
     - `prod`: Simulates a production environment, with operational endpoints accessible for end-to-end testing.

2. **Database Container** (`srvdbinvest`):
   - Uses PostgreSQL 15.3 in an Alpine Linux-based image.
   - Configured with:
     - A default user (`appuser`), password (`password`), and database (`invest_db`).
   - **Volume Persistence**: 
     - The `./volumes/db_data` directory is mounted to `/var/lib/postgresql/data` in the container, ensuring database persistence across container restarts.
     - On first execution, SQL scripts in `./volumes/sqlscripts` are automatically executed, allowing you to preload data or initialize the database schema.

3. **Application Container** (`invest_app`):
   - Synchronizes the local `./backend` directory to `/home` inside the container:
     - This setup ensures that changes to the code are immediately reflected in the running container, ideal for development.
     - The synchronization can be disabled by removing the `volumes` configuration if a fully isolated container is preferred.
   - Exposes port `8000` to allow access to the application endpoints.

4. **Network Configuration**:
   - Uses a custom bridge network (`devnetwork`) to enable communication between the app and database containers.

---

#### `docker-compose.yml` Overview

```yaml
services:
  invest_app:    
    container_name: cntappinvest
    build: .    
    environment:
      - PYTHONPATH=/home      
      - EXECUTION_MODE=test  # Define execution mode: prod/test/dev
      - IS_DOCKER="true"      # Indicates the app is running in a container
    ports:
      - "8000:8000"
    networks:
      - devnetwork
    volumes:
      - ./backend:/home  # Sync local code with container
    env_file:
      - .env
    depends_on:
      - srvdbinvest
            
  srvdbinvest:
    image: postgres:15.3-alpine
    container_name: cntdbinvest
    environment:
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: password
      POSTGRES_DB: invest_db
    ports:
      - "5432:5432"
    networks:
      - devnetwork      
    volumes: 
        - ./volumes/db_data:/var/lib/postgresql/data  # Database persistence
        - ./volumes/sqlscripts:/docker-entrypoint-initdb.d  # Initialize database

networks:
  devnetwork:
    driver: bridge
```

---

#### Running the Application

1. **Clone the repository**:
   ```bash
   git clone https://github.com/and-reis/investment-app-demo.git
   cd investment-app-demo
   ```

2. **Set the desired execution mode** in the `docker-compose.yml` file:
   ```yaml
   environment:
     - EXECUTION_MODE=dev  # Options: test, dev, prod
   ```

3. **Start the containers**:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   - Swagger: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

---

#### Notes

- **Database Initialization**:  
  On the first run, the container will execute SQL scripts located in `./volumes/sqlscripts`. Use this directory to include `.sql` files for schema creation or initial data loading.

- **Development Workflow**:  
  By syncing the `./backend` directory to `/home` in the container, any changes to the local codebase will be immediately reflected in the running application. For an isolated environment, remove the `volumes` configuration in the `invest_app` service.

- **Execution Mode and Port Configuration**:  
  The `EXECUTION_MODE` variable and exposed ports can be adjusted as needed to match your testing or deployment requirements.

---

### Note on Database Migrations

For simplicity, this project does not include tools like Alembic for database migration management. Users are free to integrate such tools based on their own preferences or project needs.  

---

## Running Tests

Testing is a critical part of this project to ensure code quality and functionality. The application supports automated tests that run in `test` mode, with special configurations for handling database persistence and generating reports.

---

### Test Modes and Behavior

1. **Standard Tests**:
   - Focus on individual functionalities, ensuring they behave as expected.
   - These tests **do not persist data** in the database and are executed in an isolated environment.

2. **Functional Tests with Persistence**:
   - Simulate End-to-End (E2E) scenarios that interact with the full stack, including the database.
   - These tests persist specific data in the database, allowing the creation of audit trails or reports for documentation purposes.
   - Examples:
     - Testing user role-based access.
     - Verifying portfolio management workflows.

3. **Execution Workflow**:
   - In `test` mode, the app container:
     1. Starts the application.
     2. Executes all tests, including functional tests.
     3. Outputs test results to the terminal.
     4. Automatically shuts down after completion.
   - This behavior can be extended to generate final reports or integrate with CI/CD pipelines.

---

### Running Tests with Docker

1. **Set the `EXECUTION_MODE` to `test`** in `docker-compose.yml`:
   ```yaml
   environment:
     - EXECUTION_MODE=test
   ```

2. **Start the containers**:
   ```bash
   docker-compose up --build
   ```

3. **View the test results**:
   - The terminal will display the status of all executed tests.
   - Status includes the number of tests run, passed, failed, or skipped.

4. **Generate Reports** (Optional):
   - Extend the test suite to output results in formats like JUnit XML or HTML for further documentation or audit purposes.

---

### Running Tests Locally (Optional)

If not using Docker, follow these steps:

1. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

2. **Run tests** using `pytest`:
   ```bash
   pytest
   ```

3. **Persist Data for Specific Tests**:
   - Manually configure functional tests to persist results in the database for auditing or reporting purposes.

---

### Notes and Recommendations

- **Selective Database Persistence**:
  - Only tests deemed necessary (e.g., E2E or functional tests) should persist data to the database. Standard tests will not affect the database state.

- **Container Auto-Teardown**:
  - In `test` mode, the container runs the application, executes tests, and shuts down automatically. This ensures a clean environment for subsequent runs.

- **Future Improvements**:
  - Implement a feature to automatically generate and save test reports (e.g., HTML or JSON) for auditing and documentation.

---

## Contributing

Contributions to the Investment App Demo are welcome, but please note that this project is primarily a **technical demonstration** and is **not actively maintained**. While I may occasionally review and merge contributions, this project is not under continuous development, and responses to issues or pull requests may be delayed.

---

### Guidelines for Contributions

1. **Scope of Contributions**:  
   Contributions are encouraged only if they align with the project's purpose as a technical demonstration. Examples include:
   - Fixing bugs in existing functionality.
   - Improving documentation.
   - Adding small, self-contained features that showcase extensibility (e.g., additional API endpoints or test cases).

2. **Expectations for Response Time**:  
   - Issues and pull requests may not receive immediate attention. I will review contributions as my schedule permits.

3. **Submitting a Pull Request**:  
   If you'd like to contribute:
   - **Fork the repository**: Create a copy of the project in your GitHub account.
   - **Make your changes**: Add tests or documentation updates as necessary.
   - **Submit a pull request**: Provide a clear description of your changes and how they align with the project's goals.

4. **Bug Reports and Feature Requests**:  
   - Bug reports should include clear, reproducible steps and expected outcomes.
   - Feature requests will be reviewed based on their relevance to the purpose of the project.

---

### Note to Users

This project is not intended for active production use or long-term development. While the codebase is designed to be extensible, users interested in further developing or deploying the application should consider forking the repository and tailoring it to their needs.

---

### **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

### **Acknowledgements**

This project would not have been possible without the contributions of several open-source tools and communities. Special thanks to:

- **[ccxt](https://github.com/ccxt/ccxt)**: For providing a robust library to work with real-time and historical data from cryptocurrency exchanges, enabling seamless data integration for this app.
- **Binance API**: For offering reliable market data that powers many of the app's functionalities. (This project is not affiliated with Binance or officially notified by the company.)
- **[FastAPI](https://fastapi.tiangolo.com/)**: For making modern API development efficient and enjoyable with features like automatic interactive documentation.
- **The Open-Source Community**: For building and maintaining the tools and libraries that make projects like this one possible.

---
### Live Demo and Code

- 📦 **Repository**: [Investment App Demo](https://github.com/and-reis/investment_app-demo)
- 👤 **Author**: Anderson Reis
- 🚀 **Version**: 1.0
