import os

from django.db import models
from django.conf import settings

import requests


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    endpoint_base = models.CharField(max_length=255, null=True, blank=True)
    docs_save_only_items = models.BooleanField(
        default=True, help_text="Only save '/items' paths from the docs"
    )
    docs = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __get_docs(self):
        # get docs from directus
        token_env_name = f"DIRECTUS_TOKEN_{self.name.upper()}"
        token = os.getenv(token_env_name)
        response = requests.get(
            f"{self.endpoint_base}{settings.DIRECTUS_DOCS}",
            headers={"Authorization": f"{token}"},
        )

        # Remove unrequired paths
        data = response.json()
        if self.docs_save_only_items:
            paths = data["paths"]
            clean_paths = {}
            for path, value in paths.items():
                if "/items/" in path:
                    clean_paths[path] = value
            data["paths"] = clean_paths
            
        # Fix servder domain (add https://)
        data["servers"] = [{"url": "https://" + data["servers"][0]["url"]}]

        return data

    def __get_default_endpoint_base(self):
        endpoint_base = settings.DIRECTUS_DEFAULT_PROJECTS_BASE
        endpoint_base = endpoint_base.replace("{project}", self.name.lower())
        return endpoint_base

    def save(self, *args, **kwargs):
        # Auto set endpoint base
        if not self.endpoint_base:
            self.endpoint_base = self.__get_default_endpoint_base()

        # refresh docs each time the project is saved
        self.docs = self.__get_docs()
        super().save(*args, **kwargs)


class Method(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Method"
        verbose_name_plural = "Methods"


class Endpoint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    endpoint = models.CharField(max_length=255)
    methods = models.ManyToManyField(Method)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Endpoint"
        verbose_name_plural = "Endpoints"
