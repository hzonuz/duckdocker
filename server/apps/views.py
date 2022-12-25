from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics
from django.utils import timezone

from apps.models import App, Container, Status
from apps.runner import run_container, stop_container
from apps.serializers import AppSerializer, ContainerSerializer


class AppViewSet(ModelViewSet):
    serializer_class = AppSerializer

    def get_queryset(self):
        return App.objects.filter(user=self.request.user)

    def get_object(self):
        app_id = self.kwargs.get("app_id")
        return get_object_or_404(App, id=app_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RunContainerView(APIView):
    def post(self, request, *args, **kwargs):
        app = App.objects.get(id=kwargs["app_id"])
        container_id = run_container(app)
        container = Container.objects.create(
            app=app, container_id=container_id, status=Status.RUNNING
        )
        serializer = ContainerSerializer(container)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StopContainerView(APIView):
    def post(self, request, *args, **kwargs):
        _id = kwargs.get("container_id")
        if _id == "all":
            containers = Container.objects.filter(
                app_id=kwargs["app_id"], status=Status.RUNNING
            )
            for container in containers:
                stop_container(container.container_id)
                container.status = Status.STOPPED
                container.stopped_at = timezone.now()
                container.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        container = get_object_or_404(Container, container_id=_id)
        stop_container(container.container_id)
        container.status = Status.STOPPED
        container.stopped_at = timezone.now()
        container.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContainerDetailListView(generics.ListAPIView):
    serializer_class = ContainerSerializer
    pagination_class = None

    def get_queryset(self):
        return Container.objects.filter(app_id=self.kwargs["app_id"])
