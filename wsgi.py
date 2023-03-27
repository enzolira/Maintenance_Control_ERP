from flask import Flask
from src import app as application
from src.controllers import UserControllers

if __name__ == '__main__':
    application.run()