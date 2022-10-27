const forms = [...document.querySelectorAll("[data-errors]")]
const errors_container = document.getElementById("form-errors")

const createErrorElement = (message) => {
    let alert = document.createElement("div")
    alert.classList.add("alert")
    alert.classList.add("alert-danger")
    alert.classList.add("col-12")
    alert.setAttribute("role", "alert")
    alert.innerText = message
    return alert
}

forms.map(form => {
    let errors = form.dataset.errors
    if (errors && errors_container){
        errors = JSON.parse(errors)
        let form_errors = errors["__all__"]
        if (form_errors)
        {
            form_errors.map(error => {
                errors_container.appendChild(createErrorElement(error.message))
            })
        }
    }

})



