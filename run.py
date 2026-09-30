"""Ponto de entrada da aplicação integrada Flask + Dash."""

from app.api import create_app

app = create_app(include_dashboard=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
