"use strict";
// Class definition
let datatable;

const Datatable = function() {
    // Private functions

    // demo initializer
    let init = function() {
		let datatable = $('.datatable').KTDatatable({
			layout: {
				class: 'datatable-bordered datatable-head-custom',
			},
			data: {
				//saveState: {cookie: false},
				type: 'local',
			},
			columns: [
				{
					field: 'ID',
					title: '#',
					sortable: false,
					width: 20,
					type: 'number',
					selector: {
						class: ''
					},
					textAlign: 'center',
				},
				{
					field: 'Acciones',
					title: 'Acciones',
					autoHide: false,
					sortable: false,
					width: 125,
					overflow: 'visible',
				}, 
			],
			pagination: false,
			loading: true,
		});
		
		init_search();
		init_actions(datatable);
		init_columns(datatable);
		init_paginator();
		return datatable;
	};

	let init_search = function () {
		let url = new URL(window.location.href)
		let searchInput = document.querySelector("#id_table_search");
		searchInput.value = url.searchParams.get("search");
		searchInput.addEventListener("keypress", function (e) {
			if (e.keyCode == 13) {
				url.search = "";
				url.searchParams.set("search", this.value)
				window.location.search = url.search
			}
		});
	}
	
	let init_actions = function (datatable) {
		document.querySelectorAll('.table-actions .list-action').forEach(elem => {
			elem.addEventListener('click', event => {
				let action = event.currentTarget.dataset.action
				let checkedNodes = datatable.rows('.datatable-row-active').nodes();
				if (checkedNodes.length) {
					$(`#mass-${action}-modal`).modal("show");
				}else{
					toastr.error("Debe seleccionar al menos un elemento para realizar esta acción.", "Error")
				}

			});
		});

		document.querySelector('#id_mass_update_field').addEventListener('change', async event => {
			document.querySelector('#id_mass_update_btn').disabled = !event.currentTarget.value;
			let modal = event.currentTarget.closest(".modal");
			let app_name = modal.dataset.app;
			let model_name = modal.dataset.model;
			let form = modal.querySelector('.form');
			if (form.childElementCount > 2) {
				form.lastElementChild.remove();
			}
			let field = await get_field_rendered(app_name, model_name, event.currentTarget.value)
			form.insertAdjacentHTML('beforeend', field.template);
			initSelect2(form);
		});
		
		document.querySelector('#id_mass_update_btn').addEventListener('click', async event => {
			let modal = event.currentTarget.closest('.modal');
			let url = modal.dataset.url;
			let field = document.querySelector('#id_mass_update_field').value

			let value;
			modal.querySelector('.form').lastElementChild
				.querySelectorAll(`[name=${field}]`).forEach(input => {
					if (input.type=="radio") {
						if (input.checked) {
							value = input.value;
						}
					}else{
						value = input.value;
					}
				});

			if (value) {
				let token = modal.querySelector('input[name=csrfmiddlewaretoken]').value;
				var ids = datatable.rows('.datatable-row-active').nodes().
					find('.checkbox > [type="checkbox"]').
					map((index, input) => {
						return input.value;
					});
				let form_data = new FormData()
				ids.each((index, id) => {
					form_data.append('ids', id);
				});
				form_data.append('value', value);
				form_data.append('field', field)
				form_data.append('csrfmiddlewaretoken', token);
				
				try {
					let res = await mass_update(url, form_data)
					location.reload();
				} catch (error) {
					console.log(error)
				}
			}else{
				toastr.error('No ha ingresado ningun valor', 'Error');
			}
		});
	}

	let init_columns = function (datatable) {
		document.querySelectorAll('.dropdown-menu .data-columns a').forEach(link => {
			link.addEventListener('click', event => {
				event.preventDefault();
				event.stopPropagation();
				
				let target = event.currentTarget;
				let input = target.querySelector('input');
				let column = target.dataset.column;
				input.checked = !input.checked;
				datatable.columns(column).visible(input.checked);
				//datatable.redraw();
			}) 
		});
	}

	let init_paginator = function () {
		let url = new URL(window.location.href)
		let paginate = document.querySelector('#id_paginate_by');
		if (paginate) {
			let paginate_by = url.searchParams.get('paginate_by')
			paginate.value = paginate_by || '10';
			paginate.addEventListener('change', event => {
				paginate_by = event.currentTarget.value
				let search = url.searchParams.get('search');
				url.search = '';
				if (search) {
					url.searchParams.set('search', search);
				}
				url.searchParams.set('paginate_by', paginate_by);
				window.location.search = url.search
			});
		}

		let paginator = document.querySelector('#id_paginator');

		if (paginator) {
			paginator.querySelectorAll('a').forEach(pagination => {
				pagination.addEventListener("click", event => {
					let page = event.currentTarget.dataset.page;
					url.searchParams.set("page", page)
					event.target.href = url.search
				})
			})
		}
	}

	let get_field_rendered = async (app, model, field) => {
		const url = `/insoles/forms/${app}/${model}/${field}/`
		let response = await fetch(url)
		return response.json()
	}

	let mass_update = async (url, form_data) => {
        let response = await fetch(url, {
          method: "POST",
          body: form_data,
          credentials: 'include',
        })
        return response.json();
    }

		

    return {
        // Public functions
        init: init,
    };
}();


document.addEventListener('DOMContentLoaded', () => {
	datatable = Datatable.init();
	//window.datatable = datatable;
});
