from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv(dotenv_path='.env.sample')


@app.route('/')
def main():
    return "Welcome to Flask version of AuthX"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
