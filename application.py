from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'replace later'

@app.route("/", methods=['GET', 'POST'])

# Each time a user visits the page
def index():

    # Display html
    return render_template("index.html")

if __name__ == "__main__":

    # Run in debug method, don't have to re-start server
    app.run(debug=True)
