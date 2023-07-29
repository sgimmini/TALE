from fastapi import FastAPI
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

if __name__ == '__main__':
    """Main Method"""
    uvicorn.run(app=app, host='127.0.0.1', port=8000)