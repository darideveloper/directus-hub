from core.tests_base.test_models import TestCoreModelBase

from django.conf import settings


class ProjectTestCase(TestCoreModelBase):

    def setUp(self):
        super().setUp()

        # Create initial data
        self.project = self.create_project(
            name=settings.DIRECTUS_TEST_PROJECT_NAME,
            endpoint_base=settings.DIRECTUS_TEST_PROJECT_URL,
        )

    def test_save_docs_created(self):
        """Test that the docs are created when the project is saved"""
        self.assertIsNotNone(self.project.docs)

    def test_save_docs_only_items(self):
        """Test that the docs are only items when the project is saved"""
        self.project.docs_save_only_items_assets = True
        self.project.save()

        paths = self.project.docs["paths"].keys()
        paths_items = [path for path in paths if "/items/" or "/assets/" in path]
        self.assertEqual(len(paths_items), len(paths))

    def test_save_docs_not_only_items(self):
        """Test that the docs are not only items when the project is saved"""
        self.project.docs_save_only_items_assets = False
        self.project.save()

        paths = self.project.docs["paths"].keys()
        paths_items = [path for path in paths if "/items/" in path]
        self.assertNotEqual(len(paths_items), len(paths))

    def test_save_endpoint_base_auto_set(self):
        """Test that the endpoint base is auto set when the project is saved"""

        project_base_url = settings.DIRECTUS_DEFAULT_PROJECTS_BASE.replace(
            "{project}", settings.DIRECTUS_TEST_PROJECT_NAME.lower()
        )

        self.assertIsNotNone(self.project.endpoint_base)
        self.assertEqual(self.project.endpoint_base, project_base_url)

    def test_save_docs_server_domain(self):
        """Test that the server domain is added to the docs"""
        self.project.save()
        self.assertEqual(
            self.project.docs["servers"][0]["url"].startswith("https://"), True
        )
