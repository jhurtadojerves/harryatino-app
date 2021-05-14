from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated


class AuthenticationPermissionMixin:
    """Mixin de Authentication Permission"""

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class SerializerClassMixin:
    """Mixin Class created for overwrite serializers class"""

    form_action = ["create", "update", "partial_update", "destroy"]
    list_serializer_class = None
    retrieve_serializer_class = None
    form_serializer_class = None

    def get_serializer_class(self):
        """Overwrite method get serializer class"""
        if self.serializer_class is not None:
            return super().get_serializer_class()
        elif self.action in self.form_action and self.action is not None:
            return self.form_serializer_class
        return getattr(self, f"{self.action}_serializer_class")
