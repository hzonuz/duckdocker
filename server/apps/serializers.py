from rest_framework import serializers

from apps.models import App, Container


class BriefAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ("image", "command", "envs")


class BriefContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        exclude = ("id", "app", "created_at", "stopped_at")


class AppSerializer(serializers.ModelSerializer):
    containers = BriefContainerSerializer(many=True, read_only=True)

    class Meta:
        model = App
        fields = ("id", "name", "image", "command", "envs", "containers")


class ContainerSerializer(serializers.ModelSerializer):
    app = serializers.SerializerMethodField()

    def get_app(self, obj):
        app = App.history.as_of(obj.created_at).latest("history_date")
        return BriefAppSerializer(app).data

    class Meta:
        model = Container
        exclude = ("id",)
