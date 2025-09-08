import json

from django.conf import settings

from core.tests_base.test_models import TestCoreModelBase


class ProjectJsonViewTestCase(TestCoreModelBase):
    """Test open api json view"""
    
    def setUp(self):
        super().setUp()
        
        # Create initial data
        self.project = self.create_project(
            name=settings.DIRECTUS_TEST_PROJECT_NAME,
            endpoint_base=settings.DIRECTUS_TEST_PROJECT_URL,
        )
        
        self.endpoint = f"/core/project/{settings.DIRECTUS_TEST_PROJECT_NAME}/json/"

    def test_get_project_json(self):
        """Test that the project json is returned"""
        
        # Validate response
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)
        
        # Validate content
        self.assertEqual(json.loads(response.content), self.project.docs)
        
        
class ProjectSwaggerDocsViewTestCase(TestCoreModelBase):
    """Test open api swagger docs view"""
    
    def setUp(self):
        super().setUp()
        
        # Create initial data
        self.project = self.create_project(
            name=settings.DIRECTUS_TEST_PROJECT_NAME,
            endpoint_base=settings.DIRECTUS_TEST_PROJECT_URL,
        )
        
        self.endpoint = f"/core/project/{settings.DIRECTUS_TEST_PROJECT_NAME}/swagger/"
        
    def test_get_project_swagger_docs(self):
        """Test that the project swagger docs are returned"""
        
        # Validate response
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Swagger UI")
        
        
