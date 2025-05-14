from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import time
from mysql.connector import Error
import os

app = FastAPI()

# Model for equation results
class EquationResult(BaseModel):
    a: float
    b: float
    c: float
    d: float
    suma: float
    resta: float
    resultado: float

# Wait for MySQL to be ready
def wait_for_db():
    max_retries = 30
    retry_interval = 2
    for _ in range(max_retries):
        try:
            conn = mysql.connector.connect(
                host="db",
                user="root",
                password=os.environ.get("MYSQL_ROOT_PASSWORD", "root_password"),
                database=os.environ.get("MYSQL_DATABASE", "ecuaciones")
            )
            conn.close()
            return True
        except Error:
            time.sleep(retry_interval)
    return False

# Initialize the database and tables
@app.on_event("startup")
async def startup_db_client():
    if not wait_for_db():
        print("Failed to connect to the database")
        return
    
    try:
        conn = mysql.connector.connect(
            host="db",
            user="root",
            password=os.environ.get("MYSQL_ROOT_PASSWORD", "root_password"),
            database=os.environ.get("MYSQL_DATABASE", "ecuaciones")
        )
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS resultados (
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
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully")
    except Error as e:
        print(f"Error initializing database: {e}")

# Store equation results
@app.post("/store")
def store_result(result: EquationResult):
    try:
        conn = mysql.connector.connect(
            host="db",
            user="root",
            password=os.environ.get("MYSQL_ROOT_PASSWORD", "root_password"),
            database=os.environ.get("MYSQL_DATABASE", "ecuaciones")
        )
        cursor = conn.cursor()
        
        query = '''
        INSERT INTO resultados (a, b, c, d, suma, resta, resultado)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        values = (
            result.a, 
            result.b, 
            result.c, 
            result.d, 
            result.suma, 
            result.resta, 
            result.resultado
        )
        
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"status": "success", "message": "Result stored successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Get all stored results
@app.get("/results")
def get_results():
    try:
        conn = mysql.connector.connect(
            host="db",
            user="root",
            password=os.environ.get("MYSQL_ROOT_PASSWORD", "root_password"),
            database=os.environ.get("MYSQL_DATABASE", "ecuaciones")
        )
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM resultados ORDER BY fecha DESC")
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {"results": results}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
