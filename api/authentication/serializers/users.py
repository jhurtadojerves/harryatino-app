# DRF
from rest_framework.serializers import ModelSerializer

# Local
from apps.authentication.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id",)
