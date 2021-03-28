const KTFormRepeater = function (data = {"hola": "k ase"}) {
  const textarea = document.getElementsByName(data_field.getAttribute("data-id"))[0]
  data =JSON.parse(textarea.value)
  $('.json_field').repeater({
    initEmpty: false,
    defaultValues: data,
    show: function () {
      $(this).slideDown();
    },
    
    hide: function (deleteElement) {
      if (confirm('¿Está seguro que quiere eliminar este elemento?')) {
        $(this).slideUp(deleteElement);
      }
    }
  });
}
const data_field = document.querySelector('[data-id]');

KTFormRepeater()