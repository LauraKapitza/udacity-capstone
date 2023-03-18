from config import app
from models import *




@app.route('/')
def hello_world():  # put application's code here
    return 'Hello baby!'


if __name__ == '__main__':
    app.run()
