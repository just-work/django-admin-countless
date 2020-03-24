from django.contrib.auth.models import User
from django.db import connection
from django.test import TestCase
from django.test import utils
from django.urls import reverse

from test_project.test_app import models


class CountlessAdminTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(is_superuser=True, is_staff=True)
        self.client.force_login(self.user, None)
        models.MyModel.objects.create()

    def test_no_count(self):
        """ No count queries are executed on changelist page."""
        url = reverse("admin:test_app_mymodel_changelist")
        with utils.CaptureQueriesContext(connection) as context:
            r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        for query in context.captured_queries:
            self.assertNotIn("COUNT", query['sql'])
