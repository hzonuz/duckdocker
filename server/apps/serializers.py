from rest_framework import serializers

from apps.models import App, Container


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        exclude = ("app",)


class AppSerializer(serializers.ModelSerializer):
    containers = ContainerSerializer(many=True, read_only=True)

    class Meta:
        model = App
        fields = ("id", "name", "image", "command", "envs", "containers")
