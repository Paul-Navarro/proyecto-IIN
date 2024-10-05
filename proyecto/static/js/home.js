function toggleFilters() {
    var filters = document.getElementById("filters");
    if (filters.style.display === "block") {
        filters.style.display = "none";
    } else {
        filters.style.display = "block";
    }
}

// Cierra el menú si se hace clic fuera de él
window.onclick = function(event) {
    if (!event.target.matches('.filter-button') && !event.target.closest('.filter-options')) {
        var dropdowns = document.getElementsByClassName("filter-options");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.style.display === "block") {
                openDropdown.style.display = "none";
            }
        }
    }
}
window.onload = function(event){
    /*
        Si se scrollea para ver contenidos en la etiqueta main
        entonces, se oculta el div de los filtros.
        Si no se hace esto. Dicho div queda suspendido hasta que se de click
        en otro lado que no sea el div de los filtros.
    */
    var cajaContenidos = document.getElementById("cajaContenidos");
    cajaContenidos.addEventListener("scroll",()=>{
        var filtros = document.getElementById("filters");
        if(filtros.style.display==="block"){
            filtros.style.display="none";
        }
    });
}

const redirigirLogin=()=>{
    window.location.href = "./accounts/login/";
}
const redirigirRegistro=()=>{
    window.location.href = "./accounts/signup/";
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function likeContenido(id_conte) {
    fetch(`/contenido/contenido/${id_conte}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById(`like-count-${id_conte}`).textContent = data.likes;
        document.getElementById(`unlike-count-${id_conte}`).textContent = data.unlikes;
    })
    .catch(error => console.error('Error:', error));
}

function unlikeContenido(id_conte) {
    fetch(`/contenido/contenido/${id_conte}/unlike/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById(`like-count-${id_conte}`).textContent = data.likes;
        document.getElementById(`unlike-count-${id_conte}`).textContent = data.unlikes;
    })
    .catch(error => console.error('Error:', error));
}