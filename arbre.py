from collections import deque # pour le parcours en largeur

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

    def inserer_classic(self, liste):
        """
        Construit un arbre binaire classique à partir
        d'une liste en parcours en largeur.
        Les None représentent des cases vides.
        """
        if not liste or liste[0] is None:
            self.noeud = None
            return

        self.noeud = Node(liste[0])
        file = deque([self.noeud])

        i = 1

        while file and i < len(liste):
            courant = file.popleft()

            # fils gauche
            if i < len(liste):
                if liste[i] is not None:
                    courant.sag = Node(liste[i])
                    file.append(courant.sag)
                i += 1

            # fils droit
            if i < len(liste):
                if liste[i] is not None:
                    courant.sad = Node(liste[i])
                    file.append(courant.sad)
                i += 1
    
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
        file = deque([self]) # on initialise la file avec la racine de l'arbre, c'est le seul element de son niveau
        while file: # tant qu'il y a des elements dans la file
            tmp = file.popleft() # on defile le premier element de la file qui est necessairement le noeud le plus a gauche du niveau actuel ou au dessus
            resultat.append(tmp.valeur()) # on ajoute la valeur du noeud a la liste resultat
            gauche = tmp.gauche() 
            droite = tmp.droit()
            if gauche and not gauche.estVide(): # si le sous-arbre gauche existe et n'est pas vide
                file.append(gauche) # alors on l'enfile pour le traiter plus tard, il sera traite apres tous les noeuds du niveau actuel ou au dessus
            if droite and not droite.estVide(): # si le sous-arbre droit existe et n'est pas vide
                file.append(droite) # alors on l'enfile pour le traiter plus tard, il sera traite apres tous les noeuds du niveau actuel ou au dessus et apres le sous-arbre gauche du meme niveau
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

