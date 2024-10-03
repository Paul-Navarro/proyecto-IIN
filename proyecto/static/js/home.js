function toggleFilters() {
    var filters = document.getElementById("filters");
    if (filters.style.display === "block") {
        filters.style.display = "none";
    } else {
        filters.style.display = "block";
    }
}

// Save filters automatically when any filter is changed
document.querySelectorAll('#filters input, #filters select').forEach(function (filter) {
    filter.addEventListener('change', function () {
        guardarFiltros();  // Save filters to sessionStorage whenever a filter changes
    });
});

// Guardar los filtros en sessionStorage
function guardarFiltros() {
    const filtrosSeleccionados = {
        moderadas: document.querySelector('input[name="moderadas"]').checked,
        no_moderadas: document.querySelector('input[name="no_moderadas"]').checked,
        pagadas: document.querySelector('input[name="pagadas"]').checked,
        suscriptores: document.querySelector('input[name="suscriptores"]').checked,
        autor: document.querySelector('select[name="autor"]').value,
        fecha_desde: document.querySelector('input[name="fecha_desde"]').value,
        fecha_hasta: document.querySelector('input[name="fecha_hasta"]').value
    };
    sessionStorage.setItem('filtros_seleccionados', JSON.stringify(filtrosSeleccionados));
}

// Apply filters when the user clicks the search button (lupa)
document.querySelector(".btnBuscar").addEventListener("click", function (event) {
    var searchInput = document.querySelector(".busqueda").value.trim();

    // Ensure the user has entered a search query
    if (searchInput === "") {
        event.preventDefault();  // Prevent search if the search bar is empty
        alert("Por favor, escribe algo en la barra de búsqueda.");
    } else {
        // Save filters and submit the form to search with filters
        guardarFiltros();  // Ensure filters are saved before search
        document.getElementById("search-form").submit();  // Perform the search
    }
});

// Function to load filters from sessionStorage and populate the filters UI (if necessary)
function cargarFiltros() {
    const filtrosGuardados = sessionStorage.getItem('filtros_seleccionados');
    if (filtrosGuardados) {
        const filtros = JSON.parse(filtrosGuardados);

        document.querySelector('input[name="moderadas"]').checked = filtros.moderadas;
        document.querySelector('input[name="no_moderadas"]').checked = filtros.no_moderadas;
        document.querySelector('input[name="pagadas"]').checked = filtros.pagadas;
        document.querySelector('input[name="suscriptores"]').checked = filtros.suscriptores;
        document.querySelector('select[name="autor"]').value = filtros.autor;
        document.querySelector('input[name="fecha_desde"]').value = filtros.fecha_desde;
        document.querySelector('input[name="fecha_hasta"]').value = filtros.fecha_hasta;
    }
}

// Call cargarFiltros on page load to restore any saved filters
window.onload = function () {
    cargarFiltros();

    // Close filter menu when clicking outside of it
    window.onclick = function (event) {
        if (!event.target.matches('.filter-button') && !event.target.closest('.filter-options')) {
            var dropdowns = document.getElementsByClassName("filter-options");
            for (var i = 0; i < dropdowns.length; i++) {
                var openDropdown = dropdowns[i];
                if (openDropdown.style.display === "block") {
                    openDropdown.style.display = "none";
                }
            }
        }
    };

    // Close filter menu when scrolling the content area
    var cajaContenidos = document.getElementById("cajaContenidos");
    cajaContenidos.addEventListener("scroll", () => {
        var filtros = document.getElementById("filters");
        if (filtros.style.display === "block") {
            filtros.style.display = "none";
        }
    });
};


/*
// Al enviar el formulario de búsqueda, guarda o limpia los filtros en sessionStorage
document.getElementById('search-form').addEventListener('submit', function(event) {
    var query = document.querySelector('.busqueda').value;

    // Si no se ha escrito nada en la búsqueda, previene el submit
    if (!query.trim()) {
        event.preventDefault();
        alert('Por favor, escribe algo en la búsqueda.');
    } else {
        // Si no hay filtros seleccionados, limpia sessionStorage
        if (noHayFiltrosSeleccionados()) {
            sessionStorage.removeItem('filtros_seleccionados');
        } else {
            // Si hay filtros seleccionados, guárdalos en sessionStorage
            guardarFiltros();
        }
    }
});

// Verifica si no hay ningún filtro seleccionado (todos vacíos o no marcados)
function noHayFiltrosSeleccionados() {
    return !document.querySelector('input[name="moderadas"]').checked &&
           !document.querySelector('input[name="no_moderadas"]').checked &&
           !document.querySelector('input[name="pagadas"]').checked &&
           !document.querySelector('input[name="suscriptores"]').checked &&
           document.querySelector('select[name="autor"]').value === "" &&
           document.querySelector('input[name="fecha_desde"]').value === "" &&
           document.querySelector('input[name="fecha_hasta"]').value === "";
}

// Guarda los filtros seleccionados en sessionStorage
function guardarFiltros() {
    const filtrosSeleccionados = {
        moderadas: document.querySelector('input[name="moderadas"]').checked,
        no_moderadas: document.querySelector('input[name="no_moderadas"]').checked,
        pagadas: document.querySelector('input[name="pagadas"]').checked,
        suscriptores: document.querySelector('input[name="suscriptores"]').checked,
        autor: document.querySelector('select[name="autor"]').value,
        fecha_desde: document.querySelector('input[name="fecha_desde"]').value,
        fecha_hasta: document.querySelector('input[name="fecha_hasta"]').value
    };
    
    sessionStorage.setItem('filtros_seleccionados', JSON.stringify(filtrosSeleccionados));
}
*/



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