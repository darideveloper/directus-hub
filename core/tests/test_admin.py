from core.tests_base.test_admin import TestAdminBase


class ProjectAdminTests(TestAdminBase):
    """Tests for the ProjectAdmin"""

    def setUp(self):
        super().setUp()
        self.endpoint = "/admin/core/project/"

    def test_search_bar(self):
        """Validate search bar working"""

        self.submit_search_bar(self.endpoint)


class EndpointAdminTests(TestAdminBase):
    """Tests for the EndpointAdmin"""

    def setUp(self):
        super().setUp()
        self.endpoint = "/admin/core/endpoint/"

    def test_search_bar(self):
        """Validate search bar working"""
        self.submit_search_bar(self.endpoint)


class MethodAdminTests(TestAdminBase):
    """Tests for the MethodAdmin"""

    def setUp(self):
        super().setUp()
        self.endpoint = "/admin/core/method/"

    def test_search_bar(self):
        """Validate search bar working"""
        self.submit_search_bar(self.endpoint)
