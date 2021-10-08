from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
app = Flask(__name__)

@app.route('/')
def test():
	return 'server working'

if __name__ == '__main__':
	from waitress import serve
	serve(app, host='0.0.0.0', port='8080')