#Entry point of the flask app

from app import create_app

if __name__ == "__main__":
	app = create_app()
	app.run(debug=True)