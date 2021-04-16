from django.http.response import StreamingHttpResponse
from django.test import TestCase

from ..models import User


def checkResponse(testcase, response):
    if isinstance(response, StreamingHttpResponse):
        for rec in response.streaming_content:
            rec
    testcase.assertEqual(response.status_code, 200)


class DataLoadTest(TestCase):
    def setUp(self):
        # Login
        self.client.login(username="admin", password="admin")

    def test_common_parameter(self):
        response = self.client.get("/data/common/parameter/?format=json")
        if not isinstance(response, StreamingHttpResponse):
            raise Exception("expected a streaming response")
        for i in response.streaming_content:
            if b'"records":' in i:
                return
        self.fail("Didn't find expected number of parameters")


class UserPreferenceTest(TestCase):
    def test_get_set_preferences(self):
        user = User.objects.all().get(username="admin")
        before = user.getPreference("test")
        self.assertIsNone(before)
        user.setPreference("test", {"a": 1, "b": "c"})
        after = user.getPreference("test")
        self.assertEqual(after, {"a": 1, "b": "c"})
