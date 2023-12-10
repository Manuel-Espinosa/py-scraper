from quart import Quart
from interface_adapters.blueprint import main_blueprint
#from quart_cors import cors
import os

SCRAPER_PORT = int(os.environ.get("SCRAPER_PORT", 8080))

app = Quart(__name__)
#app = cors(app)
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=SCRAPER_PORT, debug=True, use_reloader=False)  # Use use_reloader=False to avoid conflicts with Quart's reloader
