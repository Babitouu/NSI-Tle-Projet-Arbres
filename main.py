# Import des modules PyScript pour interagir avec la page web (DOM + évènements)
from pyscript import web, when, display, document
# Import des objets JavaScript pour afficher des logs et observer le redimensionnement du SVG
from js import console, ResizeObserver
# Import de l'outil permettant de créer un proxy Python utilisable côté JavaScript
from pyodide.ffi import create_proxy
# Import du module d'expressions régulières
import re
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

test = web.page["#nav_p"]

@when("click", test)
def teste():
    if "container_visible" not in web.page["#toolbox"].classes:
        web.page["#toolbox"].classes.add("container_visible")
    else:
        web.page["#toolbox"].classes.remove("container_visible")

    if "container_visible" not in web.page["#content"].classes:
        web.page["#content"].classes.add("container_visible")
    else:
        web.page["#content"].classes.remove("container_visible")

tree = Arbre()

# Gestion de la soumission du formulaire principal (valeurs + type d'arbre)
@when("submit", form_values_type)
def submit_form_values_type():
    global tree

    values = [
        float(x) if "." in x else int(x)
        for x in re.sub(r"[^0-9,.\-]", "", input_values.value).split(",")
        if x
    ]

    display_values.textContent = str(values)

    if len(values) > 0 and values[0] != "":
        # Si c'est un ABR
        if input_type.value == "search":
            tree = Arbre(Node(values[0]))
            values.pop(0)
            for elt in values:
                tree.inserer(elt)

            if "display_none" in browse_div.classes:
                browse_div.classes.remove("display_none")
            if "display_none" in search_div.classes:
                search_div.classes.remove("display_none")

            display_height.textContent = tree.hauteur()
            display_size.textContent = tree.taille()


        generate_tree(input_type.value)
        form_values_type.reset()

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

# Callback déclenché quand la largeur du SVG change
def callback(*_):
    console.log("La largeur de l'arbre est : ",svg_tree.clientWidth)

# Observation continue du redimensionnement de la zone d'affichage de l'arbre
callback_proxy = create_proxy(callback)
observer = ResizeObserver.new(callback_proxy)
observer.observe(document.getElementById("tree"))

# Gestion de la soumission du formulaire de recherche
@when("submit", form_search)
def submit_form_search():
    console.log("Recherche demandée pour : ",input_search.value)
    # Réinitialisation du formulaire après traitement
    form_search.reset()

# Gestion de la soumission du formulaire de parcours
@when("submit", form_browse)
def submit_form_browse():
    display_browse_type.textContent = "préfixe" if input_browse.value == "prefixe" else "en largeur" if input_browse.value == "largeur" else input_browse.value
    display_browse_list.textContent = eval("tree.parcours_"+input_browse.value+"()")
    # Réinitialisation du formulaire après traitement
    form_browse.reset()

# Fonction de génération de l'arbre dans le SVG (liens + nœuds)
def generate_tree(type):
    # Chaînes HTML/SVG qui vont accumuler tous les éléments graphiques
    links = ""
    nodes = ""

    # Largeur disponible dans le conteneur SVG pour calculer les positions
    width = svg_tree.clientWidth

    # Cas d'affichage d'un arbre binaire classique
    if type == "default":
        # Calcul de la hauteur de l'arbre, puis de l'échelle horizontale utilisée pour placer les nœuds
        h = tree.hauteur()
        px_par_unite = width / (2 ** (h + 1))

        # Parcours par niveau (r = rang du niveau)
        for r in range(h):
            # Espacement horizontal entre les nœuds de ce niveau
            esp = 2 ** (h - r)

            # Parcours de chaque nœud du niveau courant
            for n in range(2 ** r):
                # Position du nœud parent
                x1 = (2 * n + 1) * esp * px_par_unite
                y1 = 100 * r

                # Génération des deux liens vers les enfants (gauche puis droite)
                for a in range(2):
                    x2 = (2 * n + 0.5 + a) * esp * px_par_unite
                    y2 = 100 * (r + 1)
                    links += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="svg_link" />'

                # Génération du nœud (cercle + texte)
                nodes += f"""
                    <g transform="translate({x1}, {y1})">
                        <circle r="22" fill="#0f172a" stroke="#22d3ee" stroke-width="3" />
                        <text text-anchor="middle" dy="5" class="node-text">10</text>
                    </g>
                """

        # Injection finale du contenu SVG dans la page
        svg_tree_links.innerHTML = links
        svg_tree_nodes.innerHTML = nodes

