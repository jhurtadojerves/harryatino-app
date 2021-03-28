window.subTableInit = function(e) {
    $('<div/>').attr('id', 'child_data_ajax_' + e.currentTarget.dataset.value).appendTo(e.detailCell).KTDatatable({
        data: {
            type: 'remote',
            source: {
                read: {
                    url: '/api/v1/sorters/',
                    params: {
                        // custom query params
                        query: {
                            parent_id: e.currentTarget.dataset.value,
                        },
                    },
                },
            },
            pageSize: 5,
            serverPaging: true,
            serverFiltering: false,
            serverSorting: true,
        },

        // layout definition
        layout: {
            scroll: false,
            footer: false,

            // enable/disable datatable spinner.
            spinner: {
                type: 1,
                theme: 'default',
            },
        },

        sortable: true,

        // columns definition
        columns: [
            {
                field: 'id',
                title: '',
                sortable: false,
                width: 20,
            }, {
                field: 'code',
                title: 'Código',
            }, {
                field: 'name',
                title: 'Nombre',
            }
        ],
        detail: {
            title: 'Hola',
            content: subTableInit,
        }
    });
}
document.addEventListener('DOMContentLoaded', function(e) {

    datatable.options.columns[0] = {
        field: 'ID',
        title: '#',
        sortable: false,
        width: 20,
        textAlign: 'center', 
    }

    datatable.options.detail = {
        title: 'Hola',
        content: subTableInit,
    }

    //datatable.reload();
});