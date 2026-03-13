from pyscript import when, display, document

@when("click", "footer")
def handler():
    display("Button clicked!")
