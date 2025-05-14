const confirmChangeState = (sender) => {
    const input = sender.dataset.input || "checkbox";
    const placeholder = sender.dataset.placeholder || "Estoy seguro?";
    swal.fire({
        icon: "warning",
        input: input,
        inputPlaceholder: placeholder,
        title: sender.dataset.title,
        text: sender.dataset.text,
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

const confirmChangeStateForm = (sender, template) => {
    let stateForm = document.getElementById('stateForm')
    let token = document.querySelector("input[name=csrfmiddlewaretoken]")
    swal.fire({
        icon: "warning",
        html: template,
        title: sender.dataset.title,
        confirmButtonText: `Si, ${sender.innerText}`,
        showLoaderOnConfirm: true,
        onOpen: () => {
            init_inputmask()
            initSelect2()
            initSelect()
            initFileCustom()
        },
        preConfirm: (result) => {
            let form = document.getElementById('stateWorkflowForm')
            if (!form.checkValidity()) {
                form.reportValidity()
                return Swal.showValidationMessage(
                    `Solicitud fallida: Todos los campos del formulario son obligatorio!`
                )
            }
            let data = new FormData(form);
            data.append("transition", sender.dataset.transition)
            data.append(token.name, token.value)
            let url = sender.dataset.url || stateForm.action
            return workflowChangeState(url, data)
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
    }).catch(error => {
        Swal.showValidationMessage(
            `Solicitud fallida: ${error.message}`
        )
        document.getElementById("swal2-validation-message").style.display = "block";
    })
}

const getFormWorkflow = async (url) => {
    let response = await fetch(url)
    if (!response.ok) {
        let error = response.statusText
        if (response.status === 400) {
            let errors = await response.json()
            error = errors.error
        }
        return Promise.reject(new Error(error))
    }
    return await response.json()
}

const getUrlWorkflow = (sender, params = {}) => {
    let stateForm = document.getElementById('stateForm')
    let url = window.location.origin
    if (sender.dataset.url) url += sender.dataset.url
    else url = stateForm.action
    url = new URL(url)
    for (const [key, value] of Object.entries(params)) {
        url.searchParams.append(key, value)
    }
    return url.href
}

const initWorkflow = () => {
    const elements = document.querySelectorAll('.transition');

    elements.forEach(elem => {
        elem.addEventListener('click', event => {
            event.preventDefault();
            let sender = event.currentTarget
            if (sender.dataset.form) {
                let url = getUrlWorkflow(sender, {"transition": sender.dataset.transition})
                getFormWorkflow(url)
                    .then(res => confirmChangeStateForm(sender, res.template))
                    .catch(error => Swal.fire({
                                title: "Se produjo un error",
                                text: error.message,
                                icon: "error",
                            }))
            } else {
                confirmChangeState(sender)
            }
        })
    })
}

document.addEventListener('DOMContentLoaded', () => {
    initWorkflow();
});
