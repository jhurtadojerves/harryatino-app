const renderFormset = (prefix, addText = "Añadir Nuevo Item", additionalFunction = () => {}) => {
  $(`.inline.${prefix}`).formset({
    prefix: prefix,
    addText: `<i class="fas fa-plus icon-sm"></i> ${addText}`,
    addCssClass: "btn btn-light-primary font-weight-bolder add-row",
    deleteCssClass: "btn btn-icon btn-light-danger btn-sm delete-row",
    deleteText: '<i class="fas fa-times"></i>',
    added: function ($row) {
      additionalFunction($row)
    }
  })
}


document.addEventListener('DOMContentLoaded', () => {
  const formsets = document.querySelectorAll('.inline-group');
  for (let i=0;i<formsets.length;i++){
    const prefix = formsets[i].dataset.prefix
    renderFormset(prefix, 'Agregar elemento', function(row) {
      try{
        initSelect2(row);
      }
      catch (e) {

      }
      //init_inputmask(row);
    })
  }
});

