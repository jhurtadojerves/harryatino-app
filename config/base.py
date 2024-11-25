"""Base site for site models """

from superadmin import ModelSite


class BaseSite(ModelSite):
    """Model site base configuration"""

    # Templates
    list_template_name = "base/base_list.html"
    form_template_name = "base/base_form.html"
    detail_template_name = "base/base_detail.html"
    delete_template_name = "base/base_confirm_delete.html"

    # Success actions
    create_success_url = "detail"
    update_success_url = "detail"

    # Urls
    url_list_suffix = "listar"
    url_create_suffix = "crear"
    url_update_suffix = "editar"
    url_detail_suffix = "detalle"
    url_delete_suffix = "eliminar"

    # Pagination
    paginate_by = 10
