import os

from django.core.management.base import BaseCommand
from django.utils import timezone

from core import models

import requests

BASE_FILE = os.path.basename(__file__)

now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")


class Command(BaseCommand):
    help = "Test all endpoints from all projects"

    def test_endpoint_methods(self, endpoint_url: str, method: str, api_id: int):
        """Test the methods of an endpoint

        Args:
            endpoint_url (str): The url of the endpoint
            method (str): The method to test
            api_id (int): The id to replace in the url api call (if exists)
        """

        # Replace id from url
        endpoint_url = endpoint_url.replace("{id}", api_id)

        # Get now for logs
        response = requests.request(method, endpoint_url)

        # Submit request and validate response
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return f"error - {now} - Error testing {method} - {endpoint_url}: {e}"
        return f"ok - {now} - {method} - {endpoint_url}"

    def handle(self, *args, **kwargs):
        # Get all projects
        projects = models.Project.objects.all()

        # Add date separator in project logs
        date_separator = f"---------- {now} ----------\n"

        for project in projects:
            print(f"Testing project: {project.name}")

            project.logs += date_separator
            project.save()

            # Test all endpoints from the project
            endpoints = models.Endpoint.objects.filter(project=project)
            for endpoint in endpoints:
                endpoint_url = f"{project.endpoint_base}{endpoint.endpoint}"

                # Test all methods of the endpoint
                methods = endpoint.methods.all()
                for method in methods:
                    log = self.test_endpoint_methods(
                        endpoint_url, method.name, endpoint.api_id
                    )
                    print(f"\t{method.name} {log}")
