const initSelect2 = function (selector) {
    let elem = selector ? $(selector) : $(document)
    elem.find('.django-select2').djangoSelect2({
      placeholder: 'Seleccione un elemento',
      dropdownAutoWidth: true,
      width: '100%',
      language: {
        noResults: function () {
          return    `<button class="btn btn-block btn-primary" onClick="select2create(this)">
                        <i class="fas fa-plus-circle">
                        </i>Crear nuevo
                    </button>`;
        }
      },
      escapeMarkup: function (markup) {
        return markup;
      }
    });
}