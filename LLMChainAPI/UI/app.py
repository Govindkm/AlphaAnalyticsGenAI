from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route("/")
def home():
	return render_template("index.html")


@app.route("/")
def default():
	return render_template("layout.html")



if __name__ == "__main__":
	app.run(debug=False)
