from app import create_app
from config import config

if __name__ == "__main__":
    app = create_app(config)
    app.run(host="0.0.0.0", port=5000, debug=True)
