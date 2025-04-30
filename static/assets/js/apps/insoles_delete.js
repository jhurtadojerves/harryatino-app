const getCookieVanilla = name => {
    let cookieValueVanilla = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            cookieValueVanilla = null
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValueVanilla = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValueVanilla;
}

const init_insoles_delete = () => {
    try {
        const lines = [...document.getElementsByClassName("insoles-delete")]
        lines.map(line => {
            line.addEventListener("click", event => {
                event.preventDefault()
                confirmDelete(line)
            })
        })
    }
    catch{
        
    }
}

const handleInsolesDelete = async (line) => {
    const headers = new Headers({
        'X-CSRFToken': getCookieVanilla("csrftoken"),
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    })
    const url = line.dataset.line
    const response = await fetch(url, {
        method: "POST",
        body: {},
        headers: headers,
        credentials: "same-origin"
    })
    const data = await response.json()

    if (!response.ok){
        Swal.fire("Se produjo un error", data.message, "error")
    }
    else {
        Swal.fire({
            title: "",
            text: data.message,
            icon: "success"
        }).then((result) => {
            window.location.reload()
          })
    }

}

const confirmDelete = async (line) => {
    Swal.fire({
        title: "¿Estás seguro?",
        text: "Esta acción no se puede revertir",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Si, eliminar"
      }).then((result) => {
        if (result.isConfirmed) {
          handleInsolesDelete(line)
        }
      });
}

init_insoles_delete()
