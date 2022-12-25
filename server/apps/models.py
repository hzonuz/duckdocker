from django.db import models


class App(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="apps")
    name = models.CharField(max_length=128)
    image = models.CharField(max_length=128)
    command = models.CharField(max_length=128, blank=True, null=True)
    envs = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Status(models.IntegerChoices):
    CREATED = 0
    RUNNING = 1
    STOPPED = 2


class Container(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name="containers")
    container_id = models.CharField(max_length=128)
    status = models.PositiveIntegerField(choices=Status.choices, default=Status.CREATED)
    created_at = models.DateTimeField(auto_now_add=True)
    stopped_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.container_id
