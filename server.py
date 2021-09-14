from flaskapp import app
from flaskapp.controllers import shows, reviews, users

if __name__ == "__main__":
    app.run(debug=True)