# Python

# Third party integration
import requests


def get_user_menu(menu_list, user):
    menus = list()
    for menu in menu_list:
        obj_menu = {
            "name": menu.name,
            "url": menu.get_url(),
            "icon": menu.icon_class or "",
            "submenus": get_user_menu(menu.submenus.all(), user),
            "is_root": not menu.parent,
            "is_group": menu.is_group,
        }
        if not obj_menu["submenus"] and (
            not menu.public_menus.filter(is_active=True).exists()
            and (menu.is_group or not menu.action.has_permissions(user))
        ):
            continue
        menus.append(obj_menu)

    return menus


def get_short_url(long_url):
    headers = {
        "Authorization": "Bearer 53565e69c665d3c4cd8f42059e45efa5ebb3b686",
        "Content-Type": "application/json",
    }

    params = {"long_url": long_url}
    response = requests.post(
        "https://api-ssl.bitly.com/v4/shorten", headers=headers, json=params
    )
    return response.json()


def get_encoded_verbose(string):
    a, b = "áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN"
    trans = str.maketrans(a, b)
    translate = string.translate(trans)
    return str(translate)
