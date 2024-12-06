const initFileCustom = () => {
  $('.custom-file-input').on('change', function () {
    let fileName = $(this).val()
    $(this).removeClass("is-invalid")
    $(this).next('.custom-file-label').addClass("selected").html(fileName)
  })
}

initFormset = () => {
  const formsets = document.querySelectorAll('.inline-group');
  for (let i = 0; i < formsets.length; i++) {
    const prefix = formsets[i].dataset.prefix
    renderFormset(prefix, 'Agregar elemento', function (row) {
      try {
        dependent_fields()
        initSelect2(row)
        initFileCustom()
        initFileCustom()
      } catch (e) {
        console.log(e)
      }
    })
    // Logic for delete add button if is required
    let disable = formsets[i].dataset.add
    if (disable === "disable") {
      let add_row = [...document.getElementsByClassName("add-row")]
      add_row.map(element => {
        element.remove()
      })
    }
  }
}

const addErrors = (selector, values) => {
  let container = selector.querySelector("div.invalid-feedback")
  container.style.display = 'block'
  let ul = container.querySelector("ul")
  ul.innerHTML = '';
  for (let value of values) {
    ul.insertAdjacentHTML("beforeend", `<li>${value}</li>`)
  }
}

const initErrors = (errors) => {
  for (const [key, values] of Object.entries(errors)) {
    let elem = document.getElementById(`id_${key}`)
    if (elem) {
      elem.classList.add("is-invalid")
      let inputForm = elem.closest("div.form-group")
      let inputFormset = elem.closest("td.formset-group")
      if (inputForm) addErrors(inputForm, values)
      else if (inputFormset) addErrors(inputFormset, values)
    }
  }
}

const buildForm = (template, create_url, modal_title="Crear Instancia") => {
  if (template.length <= 1) {
    Swal.fire("No encontrado", "No se encuentra configurado el formulario", "warning");
    return 0
  }
  const modal = document.getElementById('insoles-instance-forms')
  modal.querySelector('form').action = create_url
  modal.querySelector('.modal-body').innerHTML = ''
  modal.querySelector('.modal-body').insertAdjacentHTML('beforeend', template)
  modal.querySelector('#modalLabel').textContent = modal_title
  $(modal).modal('show')
  dependent_fields()
  initFormset()
  initSelect2(modal)
  initSelect(modal)
  init_inputmask(modal)
  initFileCustom()

}

const sendForm = (url, data) => {
  return fetch(url, {
    method: "POST",
    body: data,
  }).then(async response => {
    if (!response.ok) {
      console.log(response)
      const data = await response.json()
      if (data.errors) initErrors(data.errors)
      throw new Error(data.error)
    }
    return response.json()
  }).catch(error => toastr.error(`Solicitud fallida: ${error.message}`, 'Error'))
}

const handleClickForm = () => {
  const forms = [...document.getElementsByClassName("form-instance-insoles")]
  forms.map(form => {
    form.addEventListener("click", ev => {
      ev.preventDefault()
      let url = ev.target.dataset.url
      let modal_title = ev.target.dataset.title
      if (!url) {
        url = form.dataset.url
      }
      if (!modal_title){
        modal_title = "Crear Instancia"
      }
      getFormWorkflow(url)
        .then(res => buildForm(res.template, res.create_url, modal_title))
        .catch(error => toastr.error(error, 'Error'))
    })
  })
}

let handleSubmitForm = async (ev, saveForm) => {
  KTApp.blockPage()
  let form = new FormData(saveForm)
  if (saveForm.submitter) form.append("button", saveForm.submitter)
  let response = await sendForm(saveForm.action, form)
  if (response && response.message) {
    toastr.success(response.message, 'Notificación')
    window.location.reload()
  }
  KTApp.unblockPage()
}

let insoles_form = () => {
  let saveForm = document.getElementById("insoles-instance-form")
  saveForm.addEventListener("submit", async (ev) => {
    try{
        let submitButton = document.getElementById("preventSubmit");
        if (submitButton.disabled) {
            ev.preventDefault();
            return;
        }
        submitButton.disabled = true;
        setTimeout(() => {
            submitButton.disabled = false;
        }, 5000);
    }
    catch (error) {
        console.log(error)
    }

    ev.preventDefault()
    await handleSubmitForm(ev, saveForm)
  })
  handleClickForm()
}
insoles_form()
