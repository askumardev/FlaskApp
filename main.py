from flask import Flask, render_template, request

app = Flask(__name__)

# @app.route("/", methods=["GET", "POST"])
# def hello_world():
#    marks = {
#       "Math": 90,
#       "Science": 85,
#       "History": 92
#    }
#    return render_template("index.html", marks=marks)
@app.route("/", methods=["GET", "POST"])
def hello_world():

   return render_template("pages/index.html")


app.run(port=8000, debug=True)