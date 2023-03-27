from flask import Flask
from src import app
from src.controllers import UserControllers

if __name__ == '__main__':
    app.run(debug=True)