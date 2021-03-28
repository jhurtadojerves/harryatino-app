"""Define mixins to profile"""


class ProfileListMixin:
    """Profile List Mixin"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nick = self.request.GET.get("nick", False)
        forum_id = self.request.GET.get("forum_id", False)
        buyer = self.request.GET.get("buyer", False)
        page = self.request.GET.get("page", 1)
        search_url = ""
        if nick:
            search_url = f"&nick={nick}"
        if forum_id:
            search_url = f"&forum_id={forum_id}"
        if buyer:
            search_url = f"&buyer={buyer}"

        context.update(
            {
                "nick": nick,
                "forum_id": forum_id,
                "buyer": buyer,
                "page": page,
                "search_url": search_url,
            }
        )
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        nick = self.request.GET.get("nick", False)
        forum_id = self.request.GET.get("forum_id", False)
        buyer = self.request.GET.get("buyer", False)
        search_params = dict()
        if nick:
            search_params.update({"nick__icontains": nick})
        elif forum_id:
            search_params.update({"forum_user_id__startswith": forum_id})
        elif buyer:
            search_params.update({"pk": buyer})
        if search_params:
            queryset = queryset.filter(**search_params)
        return queryset
