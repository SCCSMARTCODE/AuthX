from dotenv import load_dotenv
load_dotenv(dotenv_path='../.env')

from api.v1 import CreateApp
from api.v1.routes import get_namespace_update

create_app = CreateApp(get_namespace_update())

app = create_app.app
api = create_app.api


@app.route('/')
def main():
    return "Welcome to Flask version of AuthX"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
