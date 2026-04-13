from pyscript import web, when, display, document
from js import console, ResizeObserver
from pyodide.ffi import create_proxy
import arbre

form_values_type = web.page["#form_values_type"]
form_search = web.page["#form_search"]
form_browse = web.page["#form_browse"]

input_values = web.page["#input_values"]
input_type = web.page["#input_type"]
input_search = web.page["#input_search"]
input_browse = web.page["#input_browse"]

search_div = web.page["#search_div"]
browse_div = web.page["#browse_div"]

svg_tree = web.page["#tree"]
svg_tree_links = web.page["#tree_links"]
svg_tree_nodes = web.page["#tree_nodes"]

@when("submit", form_values_type)
def submit_form_values_type():
    if input_values.value != "" and input_type.value == "search":
        if "display_none" in browse_div.classes:
            browse_div.classes.remove("display_none")
        if "display_none" in search_div.classes:
            search_div.classes.remove("display_none")
    generate_tree([1,2,3,4,5,6,7], input_type.value)
    # generate_tree(input_values.value, input_type.value)
    # console.log("La valeur est : ",input_values.value," et le type de l'arbre est : ",input_type.value)

def callback(*_):
    console.log("La largeur de l'arbre est : ",svg_tree.clientWidth)

observer = ResizeObserver.new(create_proxy(callback))
observer.observe(document.getElementById("tree"))

@when("submit", form_search)
def submit_form_search():
    console.log("Recherche demandée pour : ",input_search.value)
    form_search.reset()

@when("submit", form_browse)
def submit_form_browse():
    console.log("Parcours demandé : ",input_browse.value)
    form_browse.reset()

def generate_tree(values, type):
    links = ""
    nodes = ""
    width = svg_tree.clientWidth
    if type == "default":
        h = hauteur(values)
        px_par_unite = width / (2 ** (h + 1))
        for r in range(h):
            esp = 2 ** (h - r)
            for n in range(2 ** r):
                x1 = (2 * n + 1) * esp * px_par_unite
                y1 = 100 * r
                for a in range(2):
                    x2 = (2 * n + 0.5 + a) * esp * px_par_unite
                    y2 = 100 * (r + 1)
                    links += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="svg_link" />'
                nodes += f"""
                    <g transform="translate({x1}, {y1})">
                        <circle r="22" fill="#0f172a" stroke="#22d3ee" stroke-width="3" />
                        <text text-anchor="middle" dy="5" class="node-text">10</text>
                    </g>
                """
        svg_tree_links.innerHTML = links
        svg_tree_nodes.innerHTML = nodes

