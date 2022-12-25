from django.urls import path

from apps.views import (
    AppViewSet,
    RunContainerView,
    StopContainerView,
    ContainerDetailListView,
)

app_list = AppViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

app_detail = AppViewSet.as_view(
    {
        "get": "retrieve",
        "put": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns = [
    path("v0/", app_list, name="app-list"),
    path("<app_id>/v0/", app_detail, name="app-detail"),
    path(
        "<app_id>/run-container/v0/", RunContainerView.as_view(), name="run-container"
    ),
    path(
        "<app_id>/stop-container/<container_id>/v0/",
        StopContainerView.as_view(),
        name="stop-container",
    ),
    path(
        "<app_id>/containers/v0/",
        ContainerDetailListView.as_view(),
        name="container-detail-list",
    ),
]
