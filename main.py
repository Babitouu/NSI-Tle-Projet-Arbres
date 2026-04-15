# Import des modules PyScript pour interagir avec la page web (DOM + évènements)
from pyscript import web, when, display, document
# Import des objets JavaScript pour afficher des logs et observer le redimensionnement du SVG
from js import console, ResizeObserver, window, alert
# Import de l'outil permettant de créer un proxy Python utilisable côté JavaScript
from pyodide.ffi import create_proxy
# Import du module d'expressions régulières
import re
import json
# Import du module local de gestion des arbres
from arbre import *

# Récupération des formulaires présents dans la page
form_values_type = web.page["#form_values_type"]
form_search = web.page["#form_search"]
form_browse = web.page["#form_browse"]

# Récupération des champs de saisie utilisés dans les formulaires
input_values = web.page["#input_values"]
input_type = web.page["#input_type"]
input_search = web.page["#input_search"]
input_browse = web.page["#input_browse"]

# Récupération des blocs affichés/masqués dynamiquement
search_div = web.page["#search_div"]
browse_div = web.page["#browse_div"]

# Récupération des éléments SVG pour afficher l'arbre (conteneur global, liens et nœuds)
svg_tree = web.page["#tree"]
svg_tree_links = web.page["#tree_links"]
svg_tree_nodes = web.page["#tree_nodes"]

# Récupération des éléments pour l'affichage de la hauteur, de la taille et du parcours
display_browse_type = web.page["#display_browse_type"]
display_browse_list = web.page["#display_browse_list"]
display_height = web.page["#height"]
display_size = web.page["#size"]
display_values = web.page["#display_values"]

toolbox_button = web.page["#nav_settings"]

# Récupération des éléments d'historique
history_select = web.page["#history_select"]
history_button = web.page["#history_button"]

tree = Arbre()

# Initialiser l'historique (vide par défaut)
def load_history():
    stored = window.localStorage.getItem("tree_history")
    if stored:
        return json.loads(stored)
    return []

def save_history(history):
    # Garder seulement les 5 derniers éléments
    history_limited = history[-5:]
    window.localStorage.setItem("tree_history", json.dumps(history_limited))

def add_to_history(values_str, tree_type):
    history = load_history()
    # Chercher si l'élément existe déjà
    entry = [values_str, tree_type]
    if entry in history:
        history.remove(entry)
    # Ajouter à la fin
    history.append(entry)
    save_history(history)
    update_history_select()

def update_history_select():
    history = load_history()
    history_select.innerHTML = "<option value='' disabled selected>Sélection de l'arbre</option>"
    for idx, (values, type_name) in enumerate(history):
        option = document.createElement("option")
        option.value = idx
        display_type = "Recherche" if type_name == "search" else "Binaire"
        option.textContent = f"{values[:20]}... ({display_type})"
        history_select.appendChild(option)

# Initialiser le select au chargement
update_history_select()

@when("click", toolbox_button)
def toolbox_menu():
    if "container_visible" in web.page["#toolbox"].classes:
        web.page["#toolbox"].classes.remove("container_visible")
    else:
        web.page["#toolbox"].classes.add("container_visible")

# Fonction de traitement de l'arbre (utilisée par le formulaire et l'historique)
def process_tree_values(initial_values, tree_type):
    toolbox_menu()

    global tree

    tree = Arbre()

    if tree_type == "search":
        if "display_none" in search_div.classes:
            search_div.classes.remove("display_none")
        values = [
            float(x) if "." in x else int(x)
            for x in re.sub(r"[^0-9,.\-]", "", initial_values).split(",")
            if x and x != "" and x != "-" and x != "."
        ]
    else:
        if "display_none" not in search_div.classes:
            search_div.classes.add("display_none")
        cleaned = initial_values.replace("[","").replace("]","").replace("'","").replace("\"","").replace(" ","").split(",")
        values = [None if x == "None" else x for x in cleaned]

    display_values.textContent = str(values).replace(",", ", ")

    if len(values) > 0:
        if tree_type == "search":
            for elt in values:
                tree.inserer(elt)
        else:
            tree.inserer_classic(values)

        display_height.textContent = tree.hauteur()
        display_size.textContent = tree.taille()

        if "display_none" in browse_div.classes:
            browse_div.classes.remove("display_none")

        display_browse_list.textContent = ""
        display_browse_type.textContent = ""

        generate_tree(tree_type)
        
        # Ajouter à l'historique
        add_to_history(initial_values, tree_type)
        
        # Réinitialiser panzoom après génération du contenu
        window.init_panzoom()

    else:
        display_height.textContent = "-"
        display_size.textContent = "-"
        display_browse_list.textContent = ""
        display_browse_type.textContent = ""
        display_values.textContent = ""
        if "display_none" not in browse_div.classes:
            browse_div.classes.add("display_none")
        if "display_none" not in search_div.classes:
            search_div.classes.add("display_none")
    form_values_type.reset()

# Gestion de la soumission du formulaire principal (valeurs + type d'arbre)
@when("submit", form_values_type)
def submit_form_values_type():
    process_tree_values(input_values.value, input_type.value)

# Callback déclenché quand la largeur du SVG change
def callback(*_):
    window.init_panzoom()

# Observation continue du redimensionnement de la zone d'affichage de l'arbre
callback_proxy = create_proxy(callback)
observer = ResizeObserver.new(callback_proxy)
observer.observe(document.getElementById("tree"))

# Gestion du chargement depuis l'historique
@when("click", history_button)
def load_from_history():
    if history_select.value != "":
        history = load_history()
        idx = int(history_select.value)
        if idx < len(history):
            values_str, type_str = history[idx]
            process_tree_values(values_str, type_str)

# Gestion de la soumission du formulaire de recherche
@when("submit", form_search)
def submit_form_search():
    toolbox_menu()
    nodes = web.page.find(".tree_node")
    texts = web.page.find(".node_text")
    for i in range(len(nodes)):
        if "tree_node_searched" in nodes[i].classes:
            nodes[i].classes.remove("tree_node_searched")

    value_clean = re.sub(r"[^0-9,.\-]", "", input_search.value) if input_search.value and input_search.value != "" and input_search.value != "-" else ""
    if value_clean != "" and tree.rechercher(float(value_clean) if "." in value_clean else int(value_clean)):
        for i in range(len(nodes)):
            if texts[i].textContent == input_search.value:
                nodes[i].classes.add("tree_node_searched")
    else:
        alert("Valeur non trouvée")

    # Réinitialisation du formulaire après traitement
    form_search.reset()

# Gestion de la soumission du formulaire de parcours
@when("submit", form_browse)
def submit_form_browse():
    toolbox_menu()
    display_browse_type.textContent = "préfixe" if input_browse.value == "prefixe" else "en largeur" if input_browse.value == "largeur" else input_browse.value
    display_browse_list.textContent = eval("tree.parcours_"+input_browse.value+"()")
    # Réinitialisation du formulaire après traitement
    form_browse.reset()

# Fonction de génération de l'arbre dans le SVG (liens + nœuds)
def generate_tree(type):
    # Chaînes HTML/SVG qui vont accumuler tous les éléments graphiques
    links = ""
    nodes = ""

    esp_y = 100
    esp_x = 20
    fact = 2
 
    hauteur_globale = tree.hauteur()

    def generate_recur(arbre, x=0, y=0):
        nonlocal links, nodes
        
        # Vérifier que l'arbre n'est pas vide
        if arbre is None or arbre.estVide():
            return
        
        profondeur = int(y / esp_y)
        offset = (fact ** (hauteur_globale - profondeur - 1)) * esp_x
        x_new_noeuds_g = x - offset
        x_new_noeuds_d = x + offset
        y_new_noeud = y+esp_y

        nodes += f"""
            <g transform="translate({x}, {y})">
                <circle class="tree_node" data-value="{arbre.noeud.v}" />
                <text dy="5" class="node_text">{arbre.noeud.v}</text>
            </g>
        """

        gauche = arbre.gauche()
        if gauche and not gauche.estVide():
            links += f'<line x1="{x}" y1="{y}" x2="{x_new_noeuds_g}" y2="{y_new_noeud}" class="svg_link" />'
            generate_recur(gauche, x_new_noeuds_g, y_new_noeud)
        
        droit = arbre.droit()
        if droit and not droit.estVide():
            links += f'<line x1="{x}" y1="{y}" x2="{x_new_noeuds_d}" y2="{y_new_noeud}" class="svg_link" />'
            generate_recur(droit, x_new_noeuds_d, y_new_noeud)

    generate_recur(tree)

    svg_tree_links.innerHTML = links
    svg_tree_nodes.innerHTML = nodes
