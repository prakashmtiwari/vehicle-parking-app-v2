from vpa import create_app
from vpa.beserver.config import BaseConfig


app = create_app()


if __name__ == "__main__":
    app.run(host=BaseConfig.APP_HOST, port=BaseConfig.APP_PORT, debug=BaseConfig.DEBUG)
