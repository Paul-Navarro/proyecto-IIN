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









/*Estrellitas*/ 
// Función para manejar la selección de estrellas
function seleccionarEstrellas(id_conte) {
    const estrellas = document.querySelectorAll(`#estrellas-${id_conte} .estrella`);

    estrellas.forEach(estrella => {
        estrella.addEventListener('click', function() {
            const valor = this.getAttribute('data-value');
            calificarContenido(id_conte, valor); // Enviar la calificación al servidor
            marcarEstrellas(id_conte, valor); // Marcar visualmente las estrellas seleccionadas inmediatamente
        });
    });
}

window.onload = function() {
    const cajasEstrellas = document.querySelectorAll('.estrellas-container');

    cajasEstrellas.forEach(caja => {
        const id_conte = caja.getAttribute('data-id');
        let valorInicial = caja.getAttribute('data-valor'); // Obtener el valor inicial almacenado

        // Verificación para comprobar si el valor está correcto
        console.log(`Valor de estrellas para el contenido ${id_conte}: ${valorInicial}`);

        // Convertir valorInicial a número y establecerlo a 0 si no es válido
        valorInicial = parseInt(valorInicial) || 0;

        marcarEstrellas(id_conte, valorInicial); // Marcar las estrellas al cargar la página
        seleccionarEstrellas(id_conte); // Habilitar la selección de estrellas
    });
}

function marcarEstrellas(id_conte, valor) {
    const estrellas = document.querySelectorAll(`#estrellas-${id_conte} .estrella`);
    estrellas.forEach(estrella => {
        if (parseInt(estrella.getAttribute('data-value')) <= valor) {
            estrella.classList.add('selected');
        } else {
            estrella.classList.remove('selected');
        }
    });
}

function calificarContenido(id_conte, estrellas) {
    fetch(`/contenido/contenido/${id_conte}/calificar/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ estrellas: estrellas }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Actualizar el promedio visualmente
            document.getElementById(`promedio-estrellas-${id_conte}`).textContent = `Promedio: ${data.promedio_estrellas}`;
            
            // No es necesario volver a llamar a marcarEstrellas aquí porque ya lo hicimos cuando se seleccionaron las estrellas
            // Marcar las estrellas seleccionadas permanentemente
            // marcarEstrellas(id_conte, estrellas); // Ya lo hicimos antes

            // Actualizar el label con la nueva calificación del usuario para este contenido
            document.getElementById(`calificacion-usuario-${id_conte}`).textContent = `Tu calificación anterior: ${estrellas} estrellas`;
        }
    })
    .catch(error => console.error('Error:', error));
}


