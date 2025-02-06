from apps.profiles.models.profiles import Profile
from apps.profiles.schemas import CalculateLevelAndSocialRank
from apps.utils.services import UserAPIService


class ProfileService:
    GRADUATE = "Graduado"
    MAX_LEVEL_ACCOUNTS = (
        119249,
        119247,
        119248,
        119738,
        119739,
        119246,
        119242,
        119769,
        119772,
        119781,
        119773,
        119770,
        119768,
    )

    @classmethod
    def get_social_rank(cls, level, graduation_status) -> str:
        if level == 0 or graduation_status != cls.GRADUATE:
            return "Aprendiz"
        elif 1 <= level <= 2:
            return "Unicornios de Bronce"
        elif 3 <= level <= 4:
            return "Unicornios de Plata"
        elif 5 <= level <= 6:
            return "Unicornios de Oro"
        elif 7 <= level <= 9:
            return "Dragones de Bronce"
        elif 10 <= level <= 14:
            return "Dragones de Plata"
        elif 15 <= level <= 19:
            return "Dragones de Oro"
        elif 20 <= level <= 29:
            return "Orden de la Cruz Dorada"
        elif 30 <= level <= 39:
            return "Orden del Caduceo"
        elif 40 <= level <= 49:
            return "Orden del Grial"
        elif 50 <= level <= 59:
            return "Supremo Consejo de Morgana"
        elif 60 <= level <= 69:
            return "Supremo Consejo de Circe"
        elif 70 <= level <= 79:
            return "Supremo Consejo de Hécate"
        elif level == 80:
            return "Orden de Merlín"
        else:
            return "Rango desconocido"

    @classmethod
    def get_level_and_social_rank(cls, user_data: dict) -> CalculateLevelAndSocialRank:
        custom_fields = user_data["customFields"]
        fields = {}

        for raw in custom_fields.values():
            fields.update(raw["fields"])

        clean_fields = {}

        for key, value in fields.items():
            clean_fields.update({key: value["value"]})

        current_level = (
            int(clean_fields.get("43", 0)) if clean_fields.get("43", 0) != "" else 0
        )
        current_social_rank = clean_fields.get("61", "")
        old_posts = (
            int(clean_fields.get("39", 0)) if clean_fields.get("39", 0) != "" else 0
        )
        new_posts = int(user_data.get("posts", 0))

        # Selected values
        posts = max(old_posts, new_posts) * 5
        galleons = (
            float(clean_fields.get("12", 0)) * 0.2 if clean_fields.get("12", "") else 0
        )
        object_points = (
            float(clean_fields.get("34", 0)) * 25 if clean_fields.get("34", "") else 0
        )
        creatures_points = (
            float(clean_fields.get("33", 0)) * 25 if clean_fields.get("33", "") else 0
        )
        knowledge_number = (
            float(clean_fields.get("41", 0)) * 4000 if clean_fields.get("41", "") else 0
        )
        skill_number = (
            float(clean_fields.get("42", 0)) * 12000
            if clean_fields.get("42", "")
            else 0
        )
        power_number = (
            float(clean_fields.get("63", 0)) * 6000 if clean_fields.get("63", "") else 0
        )
        dungeon_points = (
            float(clean_fields.get("71", 0)) * 25 if clean_fields.get("71", "") else 0
        )
        set_points = (
            float(clean_fields.get("11", 0)) * 1220 if clean_fields.get("11", "") else 0
        )
        badget_points = (
            float(clean_fields.get("60", 0)) if clean_fields.get("60", "") else 0
        )

        # Calculated Values
        posts = min(posts, 50000)
        galleons = min(galleons, 80000)
        object_points = min(object_points, 75000)
        creatures_points = min(creatures_points, 75000)
        knowledge_number = min(knowledge_number, 96000)
        skill_number = min(skill_number, 132000)
        power_number = min(power_number, 60000)
        dungeon_points = min(dungeon_points, 62500)
        set_points = min(set_points, 120000)

        # Calculate Experience
        experience = (
            posts
            + galleons
            + object_points
            + creatures_points
            + knowledge_number
            + skill_number
            + power_number
            + dungeon_points
            + set_points
            + badget_points
        )
        raw_level = experience / 10000
        level = int(round(raw_level, 0))

        if user_data.get("id") in cls.MAX_LEVEL_ACCOUNTS:
            level = 80

        graduation_status = clean_fields.get("40", "")
        social_rank = cls.get_social_rank(level, graduation_status)

        return CalculateLevelAndSocialRank(
            current_level=current_level,
            calculated_level=level,
            current_rank=current_social_rank,
            calculated_rank=social_rank,
        )

    @classmethod
    def update_level_and_social_rank(
        cls, profile: Profile, level: int, social_rank: str
    ):
        data = {
            "customFields[43]": f"{level}",
            "customFields[61]": f"{social_rank}",
        }

        UserAPIService.update_user_profile(profile.forum_user_id, raw_data=data)
        profile.magic_level = level
        profile.save()
