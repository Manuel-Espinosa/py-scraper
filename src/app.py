from flask import Flask
from interface_adapters.blueprint import main_blueprint
from flask_cors import CORS  # Import CORS
import os

SCRAPER_PORT = int(os.environ.get("SCRAPER_PORT", 5000))

app = Flask(__name__)
CORS(app)
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=SCRAPER_PORT, debug=True)