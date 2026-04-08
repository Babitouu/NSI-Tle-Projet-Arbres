from pyscript import web, when, display, document
from js import console, ResizeObserver
from pyodide.ffi import create_proxy
from collections import deque # pour le parcours en largeur
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
    if "display_none" in browse_div.classes and input_values.value != "":
        browse_div.classes.remove("display_none")
    if "display_none" in search_div.classes and input_type.value == "search":
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

# CODE POUR LA FILE DEQUE

def file_vide():
    return deque()

def enfiler(file, element):
    file.append(element) # on enfile par la tête

def est_vide(file):
    return len(file) == 0

def defiler(file):
    return file.popleft() # on defile par la queue

# exemple file deque : on defile ici -> [1,2,3,4,5] <- on enfile ici

class Node:
    def __init__(self, valeur = None, sag = None, sad = None):
        self.v = valeur
        self.sag = sag
        self.sad = sad

class Arbre:
    def __init__(self, N = None):
        self.noeud = N
    
    #methodes de base

    def estVide(self):
        return self.noeud is None
    
    def gauche(self):
        if self.noeud:
            return Arbre(self.noeud.sag)
        else:
            return None
    
    def droit(self):
        if self.noeud:
            return Arbre(self.noeud.sad)
        else:
            return None
    
    def valeur(self):
        return self.noeud.v
    
    def hauteur(self):
        if self.estVide():
            return 0
        return 1 + max(self.gauche().hauteur() if self.gauche() else 0,self.droit().hauteur() if self.droit() else 0)
    
    def taille(self):
        if self.estVide():
            return 0
        return 1 + (self.gauche().taille() if self.gauche() else 0) + (self.droit().taille() if self.droit() else 0)

    def inserer(self, valeur):
        """
        insère une valeur dans l'arbre binaire de recherche
        """
        # si l'arbre est vide
        if self.estVide():
            self.noeud = Node(valeur) # alors la racine prend la valeur
        else:
            # si la valeur est plus petite
            if valeur < self.noeud.v:
                # si le sous-arbre gauche n'existe pas
                if self.noeud.sag is None:
                    # on insere la valeur
                    self.noeud.sag = Node(valeur)
                # si le sous-arbre existe
                else:
                    # on rappelle la methode sur le sous-arbre gauche
                    Arbre(self.noeud.sag).inserer(valeur)
            # si la valeur est plus grande
            elif valeur > self.noeud.v:
                # si le sous-arbre droit n'existe pas
                if self.noeud.sad is None:
                    # on insere la valeur
                    self.noeud.sad = Node(valeur)
                # si le sous-arbre droit existe
                else:
                    # on rappelle la methode sur le sous-arbre droit
                    Arbre(self.noeud.sad).inserer(valeur)
            
            # sinon la valeur existe deja, on ne l'insere pas

    
    # PARCOURS NORMAUX
    
    def parcours_infixe(self):
        """
        parcours de l'arbre en infixe : sous-arbre gauche -> racine -> sous-arbre droit
        """
        if self.estVide():
            return []
        return (
            (self.gauche().parcours_infixe() if self.gauche() else [])
            + [self.valeur()]
            + (self.droit().parcours_infixe() if self.droit() else [])
        )

    def parcours_prefixe(self):
        """
        parcours de l'arbre en prefixe : racine -> sous-arbre gauche -> sous-arbre droit
        """
        if self.estVide():
            return []
        return (
            [self.valeur()]
            + (self.gauche().parcours_prefixe() if self.gauche() else [])
            + (self.droit().parcours_prefixe() if self.droit() else [])
        )

    def parcours_suffixe(self):
        """
        parcours de l'arbre en suffixe : sous-arbre gauche -> sous-arbre droit -> racine
        """
        if self.estVide():
            return []
        return (
            (self.gauche().parcours_suffixe() if self.gauche() else [])
            + (self.droit().parcours_suffixe() if self.droit() else [])
            + [self.valeur()]
        )
    
    # PARCOURS EN LARGEUR

    def parcours_largeur(self):
        """
        parcours en largeur : de gauche a droite niveau par niveau en commencant du haut de l'arbre
        """
        if self.estVide():
            return []
        resultat = []
        file = deque([self])
        while file:
            tmp = file.popleft()
            resultat.append(tmp.valeur())
            gauche = tmp.gauche()
            droite = tmp.droit()
            if gauche and not gauche.estVide():
                file.append(gauche)
            if droite and not droite.estVide():
                file.append(droite)
        return resultat

    def rechercher(self, valeur):
        """
        recherche une valeur dans l'arbre binaire de recherche
        retourne True si trouvee, False sinon
        """
        if self.estVide(): # si c'est vide la question ne se pose pas
            return False
        if valeur == self.noeud.v: # si la valeur est egale a la valeur du noeud actuel
            return True # alors elle est trouvee
        elif valeur < self.noeud.v: # si la valeur est inferieure a la valeur du noeud actuel
            gauche = self.gauche()
            return gauche.rechercher(valeur) if gauche else False # on rappelle la fonction sur le sous-arbre gauche s'il existe
                                                                  # sinon la valeur n'est pas trouvee et on retourne False
        else: # si la valeur est superieure a la valeur du noeud actuel
            droite = self.droit()
            return droite.rechercher(valeur) if droite else False # on rappelle la fonction sur le sous-arbre droit s'il existe
                                                                  # sinon la valeur n'est pas trouvee et on retourne False

