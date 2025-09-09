
import uuid

from django.test import TestCase

from core import models as core_models


class TestCoreModelBase(TestCase):
    """Test core models"""

    def __replace_random_string__(self, string: str) -> str:
        """Replace random string with a random string

        Args:
            string (str): The string to replace

        Returns:
            str: The replaced string
        """
        random_string = str(uuid.uuid4())
        return string.replace("{x}", random_string)

    def create_project(
        self,
        name: str = "Project test {x}",
        endpoint_base: str = "",
        docs_save_only_items_assets: bool = True,
    ):
        """Create a project

        Args:
            name (str): The name of the project
            endpoint_base (str): The base endpoint of the project
            docs_save_only_items_assets (bool): Whether to save only items and assets from the docs

        Returns:
            core_models.Project: The created project
        """

        # Replace texts
        name = self.__replace_random_string__(name)

        # Create instance
        project = core_models.Project.objects.create(
            name=name,
            endpoint_base=endpoint_base,
            docs_save_only_items_assets=docs_save_only_items_assets,
        )
        return project
