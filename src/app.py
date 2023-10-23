from flask import Flask
from interface_adapters.blueprint import main_blueprint
import os

SCRAPER_PORT = int(os.environ.get("SCRAPER_PORT", 5000))

app = Flask(__name__)
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=SCRAPER_PORT, debug=True)
