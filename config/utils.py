# Python


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
