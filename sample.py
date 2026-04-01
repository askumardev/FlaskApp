from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if(request.method == "POST"):
        # print(request.form)
    else:
        return render_template("index.html")
    # print(request.method)
    # print(request.form)
   

# @app.route("/")
# def home():
#     return render_template("home.html")

# @app.route("/services")
# def services():
#     return render_template("services.html")

# @app.route("/contact")
# def contact():
#     return render_template("contact.html")

# @app.route("/about")
# def about():
#     return render_template("about.html")

# app.run(debug=True)
app.run(port=8000, debug=True)