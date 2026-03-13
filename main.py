from pyscript import web, when, display, document

input_values = web.page["#input_values"]
input_type = web.page["#input_type"]

search_div = web.page["#search_div"]
browse_div = web.page["#browse_div"]

@when("submit", "#form_values_type")
def handler():
    if "display_none" in search_div.classes:
        if input_type.value == "search":
            search_div.classes.remove("display_none")
    if "display_none" in browse_div.classes:
        if input_values.value != "":
            browse_div.classes.remove("display_none")
