from django.contrib import admin

from core import models


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "endpoint_base"]
    search_fields = ["name", "description", "endpoint_base"]
    list_filter = ["created_at", "updated_at"]
    ordering = ["name"]


@admin.register(models.Method)
class MethodAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ["created_at", "updated_at"]
    ordering = ["name"]


@admin.register(models.Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "endpoint"]
    search_fields = ["name", "description", "endpoint"]
    list_filter = ["created_at", "updated_at", "project", "methods"]
    ordering = ["project", "name"]
