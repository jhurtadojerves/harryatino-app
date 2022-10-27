"""sim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import superadmin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.pages.views import HomePage

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", superadmin.site.urls),
    path(
        "",
        include("apps.authentication.urls"),
    ),
    path("", include("apps.sales.urls")),
    path("", include("apps.workflows.urls")),
    path("", include("apps.insoles.urls")),
    path("", include("apps.dynamicforms.urls")),
    path("", include("apps.payments.urls")),
    path("", HomePage.as_view()),
    # Api v1
    path(route="api/v1/", view=include("api.urls")),
    path("select2/", include("django_select2.urls")),
    path("api-auth/", include("rest_framework.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
