const confirmChangeState = (sender) => {
    const input = sender.dataset.input || "checkbox";
    const placeholder = sender.dataset.placeholder || "Estoy seguro?";
    swal.fire({
        icon: "warning",
        input: input,
        inputPlaceholder: placeholder,
        title:sender.dataset.title,
        inputAttributes: {required: true},
        confirmButtonText: `Si, ${sender.innerText}`,
        inputValidator: (value) => {
            if ((sender.dataset.input === "file" && value) && !(value.size <= sender.dataset.max_size)) {
            return `El tamaño máximo permitido del archivo es ${sender.dataset.max_size} bytes, su archivo pesa ${value.size} bytes`
            }
            return !value && "Seleccione la opción para continuar!"
        },
        showLoaderOnConfirm: true,
        preConfirm: (result) => {
            const form = document.getElementById('stateForm');
            form.querySelector('[name=transition]').value = sender.dataset.transition;
            let data = new FormData(form);
            data.append("value", result)
            return workflowChangeState(form.action, data)
        },
        allowOutsideClick: () => !Swal.isLoading()
    }).then(async (result) => {
        if (result.isConfirmed) {
            Swal.fire({
                icon: "success",
                text: "Acción realizada con éxito",
                timer: 2000,
                timerProgressBar: true,
            }).then((result) => {
                if (result.isDismissed || result.isConfirmed) {
                    window.location.reload();
                }
            })
        }
    })
}

const workflowChangeState = (url, data) => {
    return fetch(url, {
        method: "POST",
        body: data,
    }).then(async response => {
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error)
        }
        return response.json()
    })
    .catch(error => {
        Swal.showValidationMessage(
        `Solicitud fallida: ${error.message}`
        )
    })
}

const initWorkflow = () => {
    const elements = document.querySelectorAll('.transition');
    elements.forEach(elem => {
      elem.addEventListener('click', event => {
        event.preventDefault();
        confirmChangeState(event.currentTarget)
      });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initWorkflow();
});
