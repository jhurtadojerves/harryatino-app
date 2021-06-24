const form = document.getElementById("insoles-form")
let create_form = document.getElementById(`id_create_form`)
let load_data = document.getElementById(`load_data`)
let username_element = document.getElementById(`username`)
let member_id_url = document.getElementById(`member_id_url`)
let initial_date = document.getElementById(`initial_date`)
let end_date = document.getElementById(`end_date`)
const modal = document.getElementById('insoles-forms')
let set_url = ""

const fetchMethodGet = async (url) => {
  let response = await fetch(url)
  if (response.status !== 200) {
    toastr.error('Los sentimos no se puede realizar esta acción.', 'No autorizado')
    return Promise.reject(new Error(response.statusText))
  }
  return await response.json()
}

const fetchMethodPost = async (url, form_data, credentials = "include", headers = {}) => {
  let response = await fetch(url, {
    method: "POST",
    body: form_data,
    headers: headers,
    credentials: credentials,
  })
  let data = await response.json()
  $(modal).modal('hide')
  if (data.status === 200) {
    toastr.success(data.message, 'Realizado', options = {
      "closeButton": true, "progressBar": true, "newestOnTop": true,
    });
  } else {
    toastr.error(data.message, 'Error', options = {
      "closeButton": true, "progressBar": true, "newestOnTop": true,
    });
  }

}
create_form.addEventListener("click", async (e) => {
  modal.querySelector('#render_form').innerHTML = ''
  $(modal).modal('show')
})
load_data.addEventListener("click", async (ev) => {
  if (form.checkValidity() && member_id_url.value !== "" && end_date.value !== "" && initial_date.value !== "") {
    member_id_url.value
    let {
      create_url,
      template,
      username
    } = await fetchMethodGet(`${create_form.dataset.url}?user_id=${member_id_url.value}&initial_date=${initial_date.value}&end_date=${end_date.value}`)
    modal.querySelector('form').action = create_url
    modal.querySelector('#render_form').innerHTML = ""
    modal.querySelector('#render_form').insertAdjacentHTML('beforeend', template)
    init_inputmask()
    $(".selectpicker").selectpicker('refresh');
  }
})

form.addEventListener("submit", ev => {
  ev.preventDefault()
  fetchMethodPost(`${create_form.dataset.url}?user_id=${member_id_url.value}`, new FormData(form))
})


