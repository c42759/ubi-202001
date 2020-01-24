from django.conf.urls import url
from urban_environment.api import alerts

urlpatterns = (
    url(r"^$", alerts, name="urban_alerts_list"),
    url(r'^(?P<alert_id>[0-9]+)?$', alerts, name="urban_alerts_patch"),
)