import os
from flask import Flask
from flaskr.__init__ import create_app

app = create_app(test_config=None)

if __name__ == '__main__':
	app.run()
