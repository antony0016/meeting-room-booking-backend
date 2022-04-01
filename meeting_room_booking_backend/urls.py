# django
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

# drf
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions

# drf-simplejwt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# swagger document
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# customize apps
from users.views import NicknameViewSet
from meeting_rooms.views import ReservationViewSet, MeetingRoomViewSet, LocationViewSet, RoomExchangeRequestViewSet
from pop_messages.views import PopMessageViewSet

DOCUMENT_PERMISSIONS = tuple([permissions.AllowAny])

schema_view = get_schema_view(
    openapi.Info(
        title="SOIC Meeting Room System",
        default_version='v1',
        description="",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="seki.xu@mail.soic.org.tw"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=DOCUMENT_PERMISSIONS,
)

router = DefaultRouter()
router.register("users", NicknameViewSet)
router.register("rooms", MeetingRoomViewSet)
router.register("locations", LocationViewSet)
router.register("reservations", ReservationViewSet)
router.register("room_exchange_request", RoomExchangeRequestViewSet)
# router.register("verification", VerificationViewSet)
router.register("pop_messages", PopMessageViewSet)

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('docs/', include_docs_urls('Meeting room API', permission_classes=DOCUMENT_PERMISSIONS)),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^.*$', TemplateView.as_view(template_name="index.html")),
]
