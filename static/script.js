const input_search = document.getElementById('input_search');
const browse_type = document.getElementById("browse_type");

function search() {
    console.log("Recherche : "+input_search.value);
    input_search.value = "";
    console.log(tree);
}

function browse() {
    console.log("Je parcours l'arbre en "+browse_type.value);
    browse_type.value = "";
}