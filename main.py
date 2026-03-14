from pyscript import web, when, display, document
from js import console

form_values_type = web.page["#form_values_type"]
form_search = web.page["#form_search"]
form_browse = web.page["#form_browse"]

input_values = web.page["#input_values"]
input_type = web.page["#input_type"]
input_search = web.page["#input_search"]
input_browse = web.page["#input_browse"]

search_div = web.page["#search_div"]
browse_div = web.page["#browse_div"]

@when("submit", form_values_type)
def submit_form_values_type():
    if "display_none" in browse_div.classes and input_values.value != "":
        browse_div.classes.remove("display_none")
    if "display_none" in search_div.classes and input_type.value == "search":
        search_div.classes.remove("display_none")
    console.log("La valeur est : ",input_values.value," et le type de l'arbre est : ",input_type.value)

@when("submit", form_search)
def submit_form_search():
    console.log("Recherche demandée pour : ",input_search.value)
    form_search.reset()


@when("submit", form_browse)
def submit_form_browse():
    console.log("Parcours demandé : ",input_browse.value)
    form_browse.reset()