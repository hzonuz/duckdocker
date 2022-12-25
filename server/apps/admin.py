from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from apps.models import App, Container

admin.site.register(App, SimpleHistoryAdmin)
admin.site.register(Container, SimpleHistoryAdmin)
