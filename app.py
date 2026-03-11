from flask import Flask, render_template, request

app = Flask(__name__, template_folder=".")

@app.route('/', methods=["GET", "POST"])
def home():
    tree_type_search = request.form["tree_type"] == "search" if request.form else False
    return render_template('index.html',tree_type_search=tree_type_search)

if __name__ == "__main__":
    app.run()