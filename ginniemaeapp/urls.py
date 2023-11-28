from django.urls import path
from .views import DashBoard
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path("", DashBoard.as_view(), name="dashboard")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)