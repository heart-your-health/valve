from app import create_app, db
app = create_app("config")


if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')