const dependent_fields = () => {
  let pd_fields = [...document.querySelectorAll("[data-select2-formset]")]
  pd_fields.map(field => {
    let id = field.id.split("-")
    if (id.length === 3) {
      let int_id = parseInt(id[1])
      let data = field.dataset.select2DependentFields.split("-")
      data[1] = int_id
      field.dataset.select2DependentFields = data.join("-")
    }
  })
}