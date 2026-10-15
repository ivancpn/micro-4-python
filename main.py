import os

from magazzino.app import create_app

app = create_app()

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", "8084"))
    app.run(host="127.0.0.1", port=porta, debug=True)
