# Models
from superadmin.models import Menu
from .utils import get_user_menu
from apps.pages.models import Page


def menu(request):
    return {"menu_tree": build_user_menu(request.user), "pages": Page.objects.all()}


def build_user_menu(user):
    object_list = Menu.objects.filter(parent__isnull=True)
    menu_list = get_user_menu(object_list, user)
    return menu_list
