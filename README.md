# Microservices Equation Calculator with Database

This project demonstrates a microservices architecture for calculating mathematical equations and storing the results in a MySQL database. The system consists of multiple services that work together to provide a complete solution.

## System Architecture

![Microservices Architecture](https://mermaid.ink/img/pako:eNqFkUFrwzAMhf-K0SkdpPTW0w4ZGyVhY7DRbofgOq0hToJj0YXS_z7HbbeVMXySePqe9CQ_QXoFiCEXtWbSk7F4MWHULnkoreU-upw-bpMEDOkmZm0q75_PRyek-bqInAWDDj9hi2US9qIuOZFRxWRcVYknsf8-RY8u0Vw6JydrtfYqzGECOsMNsmM5MRcc5kDCxjf_ylj-1ON0-tCdJU_3c6UGHWs3iGyH_F5e4hArJ9mjZbuN6rQWecNs0_w3W_So4WHgu09qptrvjpSGCeS0tm8FKGi9CONA65Qxqn_yCtxIHwuWZ6mKNRT8DX3r6xUm8NZWffQFr6XNsivc8uygNOSBbPiCl1aFMoPT7M3cu2jwv69_AvhWnQc)

### Services

1. **Suma Service (Addition)**
   - Endpoint: `/sumar`
   - Function: Calculates the sum of two numbers (a+b)
   - Port: 8001

2. **Resta Service (Subtraction)**
   - Endpoint: `/restar`
   - Function: Calculates the difference between two numbers (c-d)
   - Port: 8002

3. **Ecuacion Service (Equation)**
   - Endpoint: `/resolver`
   - Function: Uses suma and resta services to calculate (a+b)*(c-d)
   - Stores results in the database via db_service
   - Port: 8003

4. **Database Service (DB API)**
   - Endpoints: `/store` and `/results`
   - Function: Interfaces with MySQL database to store and retrieve calculation results
   - Port: 8004

5. **MySQL Database**
   - Stores all calculation results
   - Port: 3307 (mapped to 3306 internally)

## Database Schema

```sql
CREATE TABLE resultados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    a FLOAT NOT NULL,
    b FLOAT NOT NULL,
    c FLOAT NOT NULL,
    d FLOAT NOT NULL,
    suma FLOAT NOT NULL,
    resta FLOAT NOT NULL,
    resultado FLOAT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Running the Project

1. Make sure you have Docker and Docker Compose installed

2. Clone the repository:
   ```bash
   git clone <repository-url>
   cd microservicios
   ```

3. Build and start all services:
   ```bash
   docker compose up --build -d
   ```

4. Test the API:
   ```bash
   # Example request
   curl -X POST -H "Content-Type: application/json" -d '{"a": 10, "b": 5, "c": 8, "d": 3}' http://localhost:8003/resolver
   
   # Get stored results
   curl http://localhost:8004/results
   ```

## API Documentation

### Suma Service
- **POST /sumar**
  - Request: `{"a": float, "b": float}`
  - Response: `{"resultado": float}`

### Resta Service
- **POST /restar**
  - Request: `{"c": float, "d": float}`
  - Response: `{"resultado": float}`

### Ecuacion Service
- **POST /resolver**
  - Request: `{"a": float, "b": float, "c": float, "d": float}`
  - Response: `{"resultado": float}`

### DB Service
- **POST /store**
  - Request: `{"a": float, "b": float, "c": float, "d": float, "suma": float, "resta": float, "resultado": float}`
  - Response: `{"status": "success", "message": "Result stored successfully"}`

- **GET /results**
  - Response: `{"results": [{"id": int, "a": float, "b": float, "c": float, "d": float, "suma": float, "resta": float, "resultado": float, "fecha": timestamp}, ...]}`

## Notes

- The port mapping for the MySQL database is set to 3307:3306 to avoid conflicts with any local MySQL instances.
- The default credentials for the database are specified in the compose.yaml file.
