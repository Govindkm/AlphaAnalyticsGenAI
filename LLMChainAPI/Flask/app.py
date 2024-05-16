from flask import Flask, render_template, request, url_for
from tools.tools import processWithReAct

app = Flask(__name__)


@app.route("/")
def home():
	return render_template("index.html")


@app.route("/loaddata", methods=['POST'])
def loaddata():
    input = request.get_data(as_text=True)
    return processWithReAct(input)

if __name__ == "__main__":
	app.run(debug=False)