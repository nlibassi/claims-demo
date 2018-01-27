import os
from flask import Flask

app = Flask(__name__)
#ensure use of correct environment variables depending on where the app is run from
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/')
def hello():
    return "Hey!"

@app.route('/<name>')
def hello_name(name):
    return "Hey {}!".format(name)

#print(os.environ['APP_SETTINGS'])

if __name__ == '__main__':
    app.run()