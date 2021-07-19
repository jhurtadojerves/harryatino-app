document.addEventListener('DOMContentLoaded', () => {
    const reports = document.querySelectorAll('.export');
    reports.forEach((elem, index) => {
        elem.addEventListener('click', event => {
            event.preventDefault();
            let form = document.getElementById('export-form');
            let token = form.querySelector('input[name=csrfmiddlewaretoken]')
            let url = `/reporting/${form.dataset.app}/${form.dataset.model}/${event.currentTarget.dataset.type}/`;
            form.innerText = '';
            form.appendChild(token);
            form.action = url;
            let ids = datatable.rows('.datatable-row-active').nodes().
                find('.checkbox > [type="checkbox"]').
                map((index, input) => {
                    return input.value;
                }).toArray();

            if (ids.length) {
                ids.forEach(id => {
                    let hidden = document.createElement("input"); 
                    hidden.setAttribute("type", "hidden"); 
                    hidden.setAttribute("name", "ids"); 
                    hidden.value = id
                    form.appendChild(hidden)
                })
            }else{
                toastr.error("Debe seleccionar al menos un elemento para realizar esta acción.", "Error")
            }

            let fields = document.querySelectorAll('.data-columns input[type=checkbox]:checked')
            fields.forEach(field => {
                let hidden = document.createElement("input"); 
                hidden.setAttribute("type", "hidden"); 
                hidden.setAttribute("name", "fields"); 
                hidden.value = field.name
                form.appendChild(hidden)
            });

            form.submit();
        });
    });
});