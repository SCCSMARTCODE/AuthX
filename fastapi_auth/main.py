from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get('/')
def main():
    return "Welcome to FastAPI version of AuthX"


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
