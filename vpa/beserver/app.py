from vpa import create_app
from vpa.beserver.extensions import cache

app = create_app()


if __name__ == "__main__":
    app.run()
