from fastapi import FastAPI
import uvicorn


app = FastAPI(title='AuthX', description="FastAPI section of AuthX", version="1.0.0")


@app.get('/')
def main():
    return "Welcome to FastAPI version of AuthX"


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, host='localhost')
