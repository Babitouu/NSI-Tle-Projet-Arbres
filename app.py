from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def tree():
    tree_type_search = False
    tree = None
    if request.form:
        if request.form["init"]:
            tree = request.form["value"]
            tree_type_search = request.form["type"] == "search"
    return render_template('index.html',tree_type_search=tree_type_search,tree=tree)

if __name__ == "__main__":
    app.run()