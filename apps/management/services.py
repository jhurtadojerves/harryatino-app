from datetime import datetime
from typing import Tuple

from apps.management.models import LevelUpdateLine
from apps.profiles.models.profiles import Profile
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
                (
                    calculated_level,
                    calculated_social_rank,
                ) = cls.get_level_and_social_rank_data(user)
                lines.append(
                    LevelUpdateLine(
                        profile=profile.first(),
                        level_update=level_update,
                        content=user,
                        calculated_level=calculated_level,
                        calculated_social_rank=calculated_social_rank,
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
    def get_level_and_social_rank_data(cls, user_data: dict) -> Tuple[int, str]:
        level, social_rank, _, _ = ProfileService.get_level_and_social_rank(user_data)

        return level, social_rank
