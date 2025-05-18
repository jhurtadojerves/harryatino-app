from datetime import datetime

from apps.management.models import LevelUpdateLine, ProfileHistory
from apps.profiles.models.profiles import Profile
from apps.profiles.schemas import CalculateLevelAndSocialRank
from apps.profiles.services import ProfileService
from apps.utils.services import UserAPIService


class LevelUpdateService:
    @classmethod
    def create_lines(cls, level_update):
        timestamp = cls.get_timestamp()
        users = cls.get_user_data(timestamp)
        profiles = Profile.objects.all()
        lines = []

        for user in users:
            profile = profiles.filter(forum_user_id=user["id"])

            if profile:
                data = cls.get_level_and_social_rank_data(user)
                lines.append(
                    LevelUpdateLine(
                        profile=profile.first(),
                        level_update=level_update,
                        content=user,
                        calculated_level=data.calculated_level,
                        calculated_social_rank=data.calculated_rank,
                        old_level=data.current_level,
                    )
                )

        LevelUpdateLine.objects.bulk_create(lines)

        return level_update

    @classmethod
    def get_user_data(cls, timestamp, per_page=1000):
        users_data = UserAPIService.get_multiple_users(timestamp, per_page)

        return users_data

    @classmethod
    def get_timestamp(cls):
        now = datetime.now()
        month = (now.month - 3) % 12 or 12
        year = now.year if now.month > 3 else now.year - 1
        previous_date = now.replace(day=1, month=month, year=year)

        return datetime.timestamp(previous_date)

    @classmethod
    def get_level_and_social_rank_data(
        cls, user_data: dict
    ) -> CalculateLevelAndSocialRank:
        return ProfileService.get_level_and_social_rank(user_data)


class ProfileHistoryService:
    @classmethod
    def create(cls, forum_user_id: int, data: dict):
        profile = Profile.objects.filter(forum_user_id=forum_user_id).first()
        history = ProfileHistory.objects.create(
            forum_user_id=forum_user_id,
            profile=profile,
            original_data=data,
            new_data={},
        )

        return history

    @classmethod
    def update(cls, history_id: int, data: dict):
        history = ProfileHistory.objects.filter(id=history_id).first()
        history.new_data = data
        history.save()

        return history

    @classmethod
    def get_field_name(cls, field: str):
        field_mapping = {
            "customFields[61]": "Rango Social",
            "customFields[43]": "Nivel Mágico",
            "customFields[92]": "Rango en el Bando",
            "customFields[12]": "Galeones",
            "customFields[65]": "Ficha de Personaje",
            "customFields[64]": "Bóveda",
            "customFields[66]": "Bóveda Trastero",
            "customFields[18]": "Bando",
            "customFields[62]": "Libros de Hechizos",
            "customFields[13]": "Familia",
            "customFields[15]": "Trabajo",
            "customFields[30]": "Escalafón laboral",
            "customFields[14]": "Raza",
            "customFields[40]": "Graduación",
            "customFields[78]": "Poderes de Criaturas",
            "customFields[34]": "Puntos de Poder en Objetos",
            "customFields[33]": "Puntos de Poder en Criaturas",
            "customFields[71]": "Puntos en Mazmorras",
            "customFields[11]": "Puntos de Fabricación",
            "customFields[36]": "Rango de Objetos",
            "customFields[35]": "Rango de Criaturas",
            "customFields[21]": "Objeto mágico legendario",
            "customFields[79]": "Arcanos",
            "customFields[80]": "Guerreros Uzza",
            "customFields[19]": "Conocimientos",
            "customFields[20]": "Habilidades Mágicas",
            "customFields[60]": "Medallas",
            "customFields[76]": "Inactividad en el Bando (Oculto)",
            "customFields[39]": "Posteos para cálculo (Oculto)",
            "customFields[41]": "Nº conocimientos (Oculto)",
            "customFields[42]": "Nº Habilidades (Oculto)",
            "customFields[63]": "Nº Poderes (Oculto)",
            "customFields[67]": "Casa de Hogwarts",
            "customFields[83]": "Equipo de Quidditch",
            "customFields[90]": "Cantidad de Tickets",
        }

        return field_mapping.get(field, field)
