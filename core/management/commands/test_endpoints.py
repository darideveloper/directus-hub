import os

from django.core.management.base import BaseCommand
from django.core.management import call_command

from core import models

BASE_FILE = os.path.basename(__file__)


class Command(BaseCommand):
    help = "Test all endpoints from all projects"

    def handle(self, *args, **kwargs):
        # Get all projects
        projects = models.Project.objects.all()
        for project in projects:
            print(f"Testing project: {project.name}")
            # Test all endpoints from the project
            
            endpoints = models.Endpoint.objects.filter(project=project)
            for endpoint in endpoints:
                print(f"Testing endpoint: {endpoint.name}")