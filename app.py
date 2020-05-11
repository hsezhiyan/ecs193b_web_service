from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
	return render_template("search_page.html")