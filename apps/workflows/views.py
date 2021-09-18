# Django
from django.views.generic import View
from django.http import JsonResponse
from django.apps import apps

# Libraries
from django_fsm import has_transition_perm

# Local
from .exceptions import WorkflowException


class ChangeStateView(View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        try:
            transition_name = request.POST.get("transition")
            object = self.get_object()
            if not hasattr(object, transition_name):
                message = "La transición %s no existe." % transition_name
                return self.error(message)
            transition = getattr(object, transition_name)
            if not has_transition_perm(transition, request.user):
                return self.error("No tiene los permisos para realizar esta acción.")
            transition(**self.get_kwargs())
            object.save()
            return self.success("La acción ha sido realizada con éxito.")
        except WorkflowException as e:
            return self.error(str(e))

    def get_kwargs(self):
        if self.request.FILES:
            kwargs = {
                "value": self.request.FILES.get("value"),
                "user": self.request.user,
            }
        else:
            kwargs = {
                "value": self.request.POST.get("value"),
                "user": self.request.user,
            }
        return kwargs

    def get_object(self):
        app_name = self.kwargs.get("app")
        model_name = self.kwargs.get("model")
        pk = self.kwargs.get("pk")
        model_class = apps.get_model(app_name, model_name)
        object = model_class.objects.get(pk=pk)
        return object

    def success(self, message):
        response = {"message": message}
        return JsonResponse(response, status=200)

    def error(self, message):
        response = {"error": message}
        return JsonResponse(response, status=400)
