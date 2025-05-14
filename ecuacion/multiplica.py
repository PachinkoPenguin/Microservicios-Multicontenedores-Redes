from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
app = FastAPI()

class Input(BaseModel):
    a: float
    b: float
    c: float
    d: float

@app.post("/resolver")
def resolver(valores: Input):
    try:
        # Get a+b from suma service
        suma_resp = requests.post("http://suma:8000/sumar", json={"a": valores.a, "b": valores.b})
        suma = suma_resp.json()["resultado"]
        
        # Get c-d from resta service
        resta_resp = requests.post("http://resta:8000/restar", json={"c": valores.c, "d": valores.d})
        resta = resta_resp.json()["resultado"]
        
        # Calculate final result
        resultado = suma * resta
        
        # Store result in database
        db_data = {
            "a": valores.a,
            "b": valores.b,
            "c": valores.c,
            "d": valores.d,
            "suma": suma,
            "resta": resta,
            "resultado": resultado
        }
        
        # Send result to db_service
        db_resp = requests.post("http://db_service:8000/store", json=db_data)
        
        if db_resp.status_code != 200:
            print(f"Warning: Failed to store results in database: {db_resp.text}")
        
        return {"resultado": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")