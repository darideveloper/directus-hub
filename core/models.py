import os

from django.db import models
from django.conf import settings

import requests


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    endpoint_base = models.CharField(max_length=255, null=True, blank=True)
    docs_save_only_items_assets = models.BooleanField(
        default=True, help_text="Only save '/items' and '/assets' paths from the docs"
    )
    docs = models.JSONField(null=True, blank=True)
    logs = models.TextField(default="")
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
        if self.docs_save_only_items_assets:
            paths = data["paths"]
            clean_paths = {}
            for path, value in paths.items():
                if "/items/" in path or "/assets/" in path:
                    clean_paths[path] = value
            data["paths"] = clean_paths

        # Fix servder domain (add https://)
        data["servers"] = [{"url": "https://" + data["servers"][0]["url"]}]

        return data

    def __get_default_endpoint_base(self):
        endpoint_base = settings.DIRECTUS_DEFAULT_PROJECTS_BASE
        endpoint_base = endpoint_base.replace("{project}", self.name.lower())
        return endpoint_base

    def __create_endpoints(self, paths: dict):
        """Create an endpoint for a given path and value

        Args:
            paths (dict): The paths of the endpoints
        """
        get_method = Method.objects.get(name="GET")
        for path in paths.keys():
            endpoint, created = Endpoint.objects.get_or_create(
                project=self,
                endpoint=path,
            )
            if created:
                endpoint.methods.add(get_method)

    def save(self, *args, **kwargs):
        # Auto set endpoint base
        if not self.endpoint_base:
            self.endpoint_base = self.__get_default_endpoint_base()

        # refresh docs each time the project is saved
        self.docs = self.__get_docs()
        super().save(*args, **kwargs)

        # Save each endpoint of the project (by default with GET method)
        self.__create_endpoints(self.docs["paths"])


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
    endpoint = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    methods = models.ManyToManyField(Method, blank=True)
    api_id = models.CharField(
        default="1",
        max_length=100,
        help_text="The id to replace in the url api call (if exists)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.endpoint

    class Meta:
        verbose_name = "Endpoint"
        verbose_name_plural = "Endpoints"
