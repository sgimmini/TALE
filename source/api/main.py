import sys 
from fastapi import FastAPI, HTTPException
import uvicorn
import pydantic 
sys.path.append("..")
from .. import pre_processor
import os 

app = FastAPI()


@app.get("/")
def homepage()-> None:
    """Returns an hello on the front page"""
    return {"Hello Everyone"}

@app.get("/health")
def read_()-> None:
    """Returns an ok statement if server is running"""
    return {"200": "OK"}

@app.post("/calculate_sum")
def calculate_sum(data: dict) -> None:
    """Endpoint to reciewve data and return the sum"""
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="Invalid JSON data‚ format")
    try:
        values = [float(value) for value in data.values()]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid data values")
    return {"sum": sum(values)}

@app.get("/consume_directory")
def process_files(directory: str):
    """Endpoint to consume a directory and return the contents of the files"""
    if not isinstance(directory, str):
        raise HTTPException(status_code=400, detail="Invalid directory format")
    if not os.path.isdir(directory):
        raise HTTPException(status_code=400, detail="Invalid directory")

    # TODO: Add file processing logic here    
    output = []
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding="UTF-8") as f:  
            output.append(f.read())
    return {"file_contents": output}


def main():
    """
    Main Method
    """
    uvicorn.run(app=app, host='127.0.0.1', port=8000)

if __name__ == '__main__':
    main()