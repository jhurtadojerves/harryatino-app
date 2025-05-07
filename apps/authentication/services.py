from django.contrib.auth.models import Group

from apps.authentication.models.users import User
from apps.profiles.models.profiles import Profile


class AccessTokenService:
    @classmethod
    def prepare_profile(cls, profile: Profile, token: str) -> User:
        group = cls.get_group()
        user = AccessTokenService.get_user(profile, token)
        user.groups.add(group)
        profile.user = user
        profile.save()

        return user

    @classmethod
    def get_group(cls) -> Group:
        return Group.objects.get(name="Usuarios")

    @classmethod
    def get_user(cls, profile, password):
        if profile.user:
            return profile.user

        return User.objects.create_user(username=profile.nick, password=str(password))
