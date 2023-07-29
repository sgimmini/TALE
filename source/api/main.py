from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

@app.get("/")
def homepage():
    """Returns an hello on the front page"""
    return {"Hello Everyone"}

@app.get("/health")
def read_():
    """Returns an ok statement if server is running"""
    return {"200": "OK"}

@app.post("/calculate_sum")
def calculate_sum(data: dict):‚
    """Endpoint to reciewve data and return the sum"""
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, de‚tail="Invalid JSON data‚ format")
    try:
        values = [float(value) for value in data.values()]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid data values")
    return {"sum": sum(values)}


if __name__ == '__main__':
    """Main Method"""
    uvicorn.run(app=app, host='127.0.0.1', port=8000)