"""Define mixins to list and edit profile"""

# Django
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

# Forms
# from .forms import ProfileForm


class UserListMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(pk=self.request.user.pk)
        return queryset


"""

class UserFormMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"profile_form": self.get_profile_form(),}
        )
        return context

    def get_profile_form(self):
        kwargs = self.get_form_kwargs()
        kwargs.update({"instance": self.object.profile})
        profile_form = ProfileForm(**kwargs)
        return profile_form

    def form_valid(self, form):
        profile_form = self.get_profile_form()
        if profile_form.is_valid():
            profile_form.save()
            form.save()
            return redirect(self.get_success_url())
        else:
            form.errors.update(**profile_form.errors)
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object == request.user:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)
"""


class UserProfileMixin:
    def get_object(self, queryset=None):
        return self.request.user
