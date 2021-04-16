from itertools import chain
import os
import random
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
import tempfile

from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core import management
from django.http.response import StreamingHttpResponse
from django.test import TestCase, TransactionTestCase
from django.utils import translation

from data_admin.common.dataload import parseCSVdata
from data_admin.common.models import (
    User,
    Bucket,
    BucketDetail,
    Parameter,
    Comment,
    Follower,
    Notification,
)
from data_admin.common.tests import checkResponse
from . import models


class DataLoadTest(TestCase):

    fixtures = ["example1"]

    def setUp(self):
        os.environ["FREPPLE_TEST"] = "YES"
        self.client.login(username="admin", password="admin")
        super().setUp()

    def tearDown(self):
        Notification.wait()
        del os.environ["FREPPLE_TEST"]
        super().tearDown()

    def test_fixture_data(self):
        response = self.client.get("/data/example1/customer/?format=json")
        self.assertContains(response, '"records":3,')
        response = self.client.get("/data/example1/demand/?format=json")
        self.assertContains(response, '"records":14,')
        response = self.client.get("/data/example1/item/?format=json")
        self.assertContains(response, '"records":7,')
        response = self.client.get("/data/example1/location/?format=json")
        self.assertContains(response, '"records":3,')

    def test_csv_upload(self):
        self.assertEqual(
            [(i.name, i.category or u"") for i in models.Location.objects.all()],
            [
                (u"All locations", u""),
                (u"factory 1", u""),
                (u"factory 2", u""),
            ],  # Test result is different in Enterprise Edition
        )
        try:
            data = tempfile.NamedTemporaryFile(mode="w+b")
            data.write(b"name,category\n")
            data.write(b"factory 3,cat1\n")
            data.write(b"factory 4,\n")
            data.seek(0)
            response = self.client.post("/data/example1/location/", {"csv_file": data})
            checkResponse(self, response)
        finally:
            data.close()
        self.assertEqual(
            [
                (i.name, i.category or u"")
                for i in models.Location.objects.order_by("name")
            ],
            [
                (u"All locations", u""),
                (u"factory 1", u""),
                (u"factory 2", u""),
                (u"factory 3", u"cat1"),
                (u"factory 4", u""),
            ],  # Test result is different in Enterprise Edition
        )


class ExcelTest(TransactionTestCase):

    fixtures = ["example1"]

    def setUp(self):
        # Login
        if not User.objects.filter(username="admin").count():
            User.objects.create_superuser("admin", "your@company.com", "admin")
        self.client.login(username="admin", password="admin")
        os.environ["FREPPLE_TEST"] = "YES"
        super().setUp()

    def tearDown(self):
        Notification.wait()
        del os.environ["FREPPLE_TEST"]
        if os.path.exists("workbook.xlsx"):
            os.remove("workbook.xlsx")
        translation.activate(settings.LANGUAGE_CODE)
        super().tearDown()

    def run_workbook(self, language):
        # Change the language preference
        self.client.post(
            "/preferences/", {"pagesize": 100, "language": language, "theme": "orange"}
        )

        # Initial size
        countCustomer = models.Customer.objects.count()
        countDemand = models.Demand.objects.count()
        countItem = models.Item.objects.count()
        countLocation = models.Location.objects.count()
        countBucket = Bucket.objects.count()
        countBucketDetail = BucketDetail.objects.count()
        countParameter = Parameter.objects.count()
        self.assertTrue(countDemand > 0)

        # Export workbook
        response = self.client.post(
            "/execute/launch/exportworkbook/",
            {
                "entities": [
                    "example1.demand",
                    "example1.item",
                    "example1.customer",
                    "example1.location",
                    "common.parameter",
                    "common.bucket",
                    "common.bucketdetail",
                ]
            },
        )
        with open("workbook.xlsx", "wb") as f:
            f.write(response.content)

        # Erase the database
        management.call_command("empty")
        self.assertEqual(models.Customer.objects.count(), 0)
        self.assertEqual(models.Demand.objects.count(), 0)
        self.assertEqual(models.Item.objects.count(), 0)
        self.assertEqual(models.Location.objects.count(), 0)
        self.assertEqual(Bucket.objects.count(), 0)
        self.assertEqual(BucketDetail.objects.count(), 0)
        self.assertEqual(Parameter.objects.count(), 0)

        # Import the same workbook again
        with open("workbook.xlsx", "rb") as f:
            response = self.client.post(
                "/execute/launch/importworkbook/", {"spreadsheet": f}
            )
            if not isinstance(response, StreamingHttpResponse):
                raise Exception("expected a streaming response")
            checkResponse(self, response)

        # Verify the new content is identical
        self.assertEqual(models.Customer.objects.count(), countCustomer)
        self.assertEqual(models.Location.objects.count(), countLocation)
        self.assertEqual(models.Demand.objects.count(), countDemand)
        self.assertEqual(models.Item.objects.count(), countItem)
        self.assertEqual(Bucket.objects.count(), countBucket)
        self.assertEqual(BucketDetail.objects.count(), countBucketDetail)
        self.assertEqual(Parameter.objects.count(), countParameter)

    def test_workbook_brazilian_portuguese(self):
        self.run_workbook("pt-br")

    def test_workbook_chinese(self):
        self.run_workbook("zh-cn")

    def test_workbook_dutch(self):
        self.run_workbook("nl")

    def test_workbook_english(self):
        self.run_workbook("en")

    def test_workbook_french(self):
        self.run_workbook("fr")

    def test_workbook_hebrew(self):
        self.run_workbook("he")

    def test_workbook_croation(self):
        self.run_workbook("hr")

    def test_workbook_italian(self):
        self.run_workbook("it")

    def test_workbook_japanese(self):
        self.run_workbook("ja")

    def test_workbook_portuguese(self):
        self.run_workbook("pt")

    def test_workbook_russian(self):
        self.run_workbook("ru")

    def test_workbook_ukrainian(self):
        self.run_workbook("uk")

    def test_workbook_spanish(self):
        self.run_workbook("es")

    def test_workbook_taiwanese(self):
        self.run_workbook("zh-tw")


class freppleREST(APITestCase):

    fixtures = ["example1"]

    # Default request format is multipart
    factory = APIRequestFactory(enforce_csrf_checks=True)

    def setUp(self):
        # Login
        self.client = APIClient()
        self.client.login(username="admin", password="admin")
        os.environ["FREPPLE_TEST"] = "YES"
        super().setUp()

    def tearDown(self):
        Notification.wait()
        del os.environ["FREPPLE_TEST"]
        super().tearDown()

    def test_api_listpages_getapi(self):
        response = self.client.get("/api/")
        checkResponse(self, response)

        response = self.client.get("/api/example1/demand/")
        checkResponse(self, response)

        response = self.client.get("/api/example1/item/")
        checkResponse(self, response)

        response = self.client.get("/api/example1/customer/")
        checkResponse(self, response)

        response = self.client.get("/api/example1/location/")
        checkResponse(self, response)

        response = self.client.get("/api/common/parameter/")
        checkResponse(self, response)

        response = self.client.get("/api/common/bucket/")
        checkResponse(self, response)

        response = self.client.get("/api/common/bucketdetail/")
        checkResponse(self, response)

    def test_api_demand(self):
        response = self.client.get("/api/example1/demand/")
        checkResponse(self, response)
        response = self.client.options("/api/example1/demand/")
        checkResponse(self, response)
        recordsnumber = models.Demand.objects.count()
        data = {
            "name": "Order UFO 25",
            "description": None,
            "category": None,
            "subcategory": None,
            "item": "product #A",
            "customer": "Customer near factory 1",
            "location": "factory 1",
            "due": "2021-12-01T00:00:00",
            "status": "closed",
            "operation": None,
            "quantity": "110.0000",
        }
        response = self.client.post("/api/example1/demand/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Demand.objects.count(), recordsnumber + 1)
        self.assertEqual(models.Demand.objects.filter(name="Order UFO 25").count(), 1)
        data = {
            "name": "Order UFO 26",
            "description": None,
            "category": None,
            "subcategory": None,
            "item": "product #A",
            "customer": "Customer near factory 1",
            "location": "factory 1",
            "due": "2021-12-01T00:00:00",
            "status": "closed",
            "quantity": "220.0000",
        }
        response = self.client.post("/api/example1/demand/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Demand.objects.count(), recordsnumber + 2)
        self.assertEqual(models.Demand.objects.filter(name="Order UFO 26").count(), 1)

        data = [
            {
                "name": "Order UFO 27",
                "description": None,
                "category": "TEST DELETE",
                "subcategory": None,
                "item": "product #A",
                "location": "factory 1",
                "customer": "Customer near factory 1",
                "due": "2021-12-01T00:00:00",
                "status": "closed",
                "quantity": "220.0000",
            },
            {
                "name": "Order UFO 28",
                "description": None,
                "category": "TEST DELETE",
                "subcategory": None,
                "item": "product #A",
                "customer": "Customer near factory 1",
                "location": "factory 1",
                "due": "2021-12-01T00:00:00",
                "status": "closed",
                "quantity": "220.0000",
            },
        ]
        response = self.client.post("/api/example1/demand/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Demand.objects.count(), recordsnumber + 4)
        self.assertEqual(
            models.Demand.objects.filter(category="TEST DELETE").count(), 2
        )

        # Demand GET MULTIPART
        response = self.client.get("/api/example1/demand/Order UFO 25/")
        checkResponse(self, response)
        self.assertEqual(models.Demand.objects.filter(name="Order UFO 25").count(), 1)
        # Demand OPTIONS
        response = self.client.options("/api/example1/demand/Order UFO 25/")
        checkResponse(self, response)
        # Demand GET JSON tests
        response = self.client.get("/api/example1/demand/Order UFO 26/", format="json")
        checkResponse(self, response)
        self.assertEqual(models.Demand.objects.filter(name="Order UFO 26").count(), 1)
        # Demand PUT MULTIPART tests
        data = {
            "name": "Order UFO 25",
            "description": "Put multipart",
            "category": None,
            "subcategory": None,
            "item": "product #A",
            "customer": "Customer near factory 1",
            "location": "factory 1",
            "due": "2021-12-01T00:00:00",
            "status": "closed",
            "quantity": "110.0000",
        }
        response = self.client.put(
            "/api/example1/demand/Order UFO 25/", data, format="json"
        )
        checkResponse(self, response)
        self.assertEqual(models.Demand.objects.count(), 18)
        self.assertEqual(
            models.Demand.objects.filter(description="Put multipart").count(), 1
        )
        # Demand PUT JSON tests
        data = {
            "name": "Order UFO 26",
            "description": "Put json",
            "category": None,
            "subcategory": None,
            "item": "product #A",
            "customer": "Customer near factory 1",
            "location": "factory 1",
            "due": "2021-12-01T00:00:00",
            "status": "closed",
            "quantity": "110.0000",
        }
        response = self.client.put(
            "/api/example1/demand/Order UFO 26/", data, format="json"
        )
        checkResponse(self, response)
        self.assertEqual(models.Demand.objects.count(), recordsnumber + 4)
        self.assertEqual(
            models.Demand.objects.filter(description="Put json").count(), 1
        )
        # Demand PUT FORM tests
        data = {
            "name": "Order UFO 26",
            "description": "Put form",
            "category": None,
            "subcategory": None,
            "item": "product #A",
            "customer": "Customer near factory 1",
            "location": "factory 1",
            "due": "2021-12-01T00:00:00",
            "status": "closed",
            "quantity": "110.0000",
        }
        response = self.client.put(
            "/api/example1/demand/Order UFO 26/", data, format="json"
        )
        checkResponse(self, response)
        self.assertEqual(models.Demand.objects.count(), recordsnumber + 4)
        self.assertEqual(
            models.Demand.objects.filter(description="Put form").count(), 1
        )

        # Demand DELETE tests
        response = self.client.delete(
            "/api/example1/demand/Order UFO 26/", format="form"
        )
        self.assertEqual(response.status_code, 204)
        response = self.client.delete(
            "/api/example1/demand/Order UFO 25/", format="json"
        )
        self.assertEqual(response.status_code, 204)
        response = self.client.delete("/api/example1/demand/Demand 01/", format="api")
        self.assertEqual(response.status_code, 204)
        response = self.client.delete(
            "/api/example1/demand/?category=TEST DELETE", format="api"
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            models.Customer.objects.filter(category="TEST DELETE").count(), 0
        )

    def test_api_customer(self):
        response = self.client.get("/api/example1/customer/")
        checkResponse(self, response)
        recordsnumber = models.Customer.objects.count()
        self.assertEqual(
            models.Customer.objects.count(), 3
        )  # Different between Enterprise Edition and Community Edition
        response = self.client.options("/api/example1/customer/")
        checkResponse(self, response)
        data = {"name": "Customer near Area 51"}
        response = self.client.post("/api/example1/customer/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Customer.objects.count(), recordsnumber + 1)
        self.assertEqual(
            models.Customer.objects.filter(name="Customer near Area 51").count(), 1
        )
        data = {"name": "Customer near Area 52"}
        response = self.client.post("/api/example1/customer/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Customer.objects.count(), recordsnumber + 2)
        self.assertEqual(
            models.Customer.objects.filter(name="Customer near Area 52").count(), 1
        )
        data = [
            {"name": "Customer near Area 99", "source": "TEST DELETE"},
            {"name": "Customer near Area 100", "source": "TEST DELETE"},
        ]
        response = self.client.post("/api/example1/customer/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Customer.objects.count(), recordsnumber + 4)
        self.assertEqual(
            models.Customer.objects.filter(source="TEST DELETE").count(), 2
        )

        # Customer GET MULTIPART
        response = self.client.get("/api/example1/customer/Customer near Area 51/")
        checkResponse(self, response)
        self.assertEqual(
            models.Customer.objects.filter(name="Customer near Area 51").count(), 1
        )
        # Customer OPTIONS
        response = self.client.options("/api/example1/customer/Customer near Area 51/")
        checkResponse(self, response)
        # Customer GET JSON tests
        response = self.client.get(
            "/api/example1/customer/Customer near Area 52/", format="json"
        )
        checkResponse(self, response)
        self.assertEqual(
            models.Customer.objects.filter(name="Customer near Area 52").count(), 1
        )
        # Customer PUT MULTIPART tests
        data = {"name": "Customer near Area 51", "description": "Patch multipart"}
        response = self.client.patch(
            "/api/example1/customer/Customer near Area 51/", data
        )
        checkResponse(self, response)
        self.assertEqual(models.Customer.objects.count(), recordsnumber + 4)
        self.assertEqual(
            models.Customer.objects.filter(description="Patch multipart").count(), 1
        )
        # Customer PUT JSON tests
        data = {"name": "Customer near Area 52", "description": "Patch json"}
        response = self.client.patch(
            "/api/example1/customer/Customer near Area 52/", data, format="json"
        )
        checkResponse(self, response)
        self.assertEqual(models.Customer.objects.count(), recordsnumber + 4)
        self.assertEqual(
            models.Customer.objects.filter(description="Patch json").count(), 1
        )

        # Customer PUT FORM tests
        data = {
            "name": "Customer near Area 52",
            "description": "Patch json",
            "category": None,
            "subcategory": None,
            "source": "Put json",
            "lastmodified": "2015-12-04T10:18:40.048861",
        }

        response = self.client.patch(
            "/api/example1/customer/Customer near Area 52/", data, format="json"
        )
        checkResponse(self, response)
        self.assertEqual(models.Customer.objects.count(), recordsnumber + 4)
        self.assertEqual(models.Customer.objects.filter(source="Put json").count(), 1)

        # Customer bulk filtered GET test
        response = self.client.get(
            "/api/example1/customer/?name__contains=Area", format="json"
        )
        checkResponse(self, response)
        self.assertEqual(
            models.Customer.objects.filter(name__contains="Area").count(), 4
        )

        # Customer DELETE tests
        # Bulk "contains" filtered DELETE
        response = self.client.delete(
            "/api/example1/customer/?name__contains=Area 5", format="form"
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            models.Customer.objects.filter(name__contains="Area").count(), 2
        )
        # Single DELETE
        response = self.client.delete(
            "/api/example1/customer/Customer near factory 1/", format="api"
        )
        self.assertEqual(response.status_code, 204)
        # Bulk filtered DELETE
        response = self.client.delete(
            "/api/example1/customer/?source=TEST DELETE", format="json"
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            models.Customer.objects.filter(source="TEST DELETE").count(), 0
        )


class NotificationTest(TransactionTestCase):
    def setUp(self):
        os.environ["FREPPLE_TEST"] = "YES"
        if not User.objects.filter(username="admin").count():
            User.objects.create_superuser("admin", "your@company.com", "admin")
        super().setUp()

    def tearDown(self):
        Notification.wait()
        del os.environ["FREPPLE_TEST"]
        super().tearDown()

    def test_follow_item(self):
        user = User.objects.create_user(
            username="test user",
            email="tester@yourcompany.com",
            password="big_secret12345",
        )
        user.user_permissions.add(
            *Permission.objects.filter(
                codename__in=("view_item", "view_supplier", "view_purchaseorder")
            )
        )
        Follower(
            user=user,
            content_type=ContentType.objects.get(model="item"),
            object_pk="test item",
        ).save()
        for _ in parseCSVdata(
            models.Item,
            [["name", "category"], ["test item", "test category"]],
            user=user,
        ):
            pass
        for _ in parseCSVdata(
            models.Item,
            [["name", "category"], ["test item", "new test category"]],
            user=user,
        ):
            pass
        item = models.Item.objects.get(name="test item")
        Comment(
            content_object=item,
            object_repr=str(item)[:200],
            user=user,
            comment="test comment",
            type="comment",
        ).save()

        # Check what notifications we got
        Notification.wait()
        # for x in Notification.objects.all():
        #    print(x)
        self.assertEqual(Notification.objects.count(), 3)

    def test_performance(self):
        # Admin user follows all items
        user = User.objects.get(username="admin")
        Follower(
            user=user,
            content_type=ContentType.objects.get(model="item"),
            object_pk="all",
            type="M",  # The test email backend doesn't send email, so we can't check it
        ).save()

        items = [["item %s" % cnt] for cnt in range(1000)]

        # Create 2 users. Each user follows all 1000 items.
        for cnt in range(2):
            u = User.objects.create_user(
                username="user%s" % cnt,
                email="user%s" % cnt,
                password="big_secret12345",
                pk=cnt + 10,
            )
            u.user_permissions.add(
                *Permission.objects.filter(codename__in=("view_item", "view_demand"))
            )
            for i in items:
                Follower(
                    user=u,
                    content_type=ContentType.objects.get(model="item"),
                    object_pk=i[0],
                ).save()
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(Follower.objects.count(), 2001)

        # Upload CSV data with 1000 items
        # print("start items", datetime.now())
        errors = 0
        for _ in parseCSVdata(models.Item, chain([["name"]], items), user=user):
            errors += 1
        self.assertEqual(models.Item.objects.count(), 1000)

        # Upload CSV data with 1000 customers
        # print("start customers", datetime.now())
        customers = [["customer %s" % cnt, "test"] for cnt in range(1000)]
        for _ in parseCSVdata(
            models.Customer, chain([["name", "category"]], customers), user=user
        ):
            errors += 1
        self.assertEqual(models.Customer.objects.count(), 1000)

        # Upload CSV data with 1000 locations
        # print("start locations", datetime.now())
        locations = [["location %s" % cnt, "test"] for cnt in range(1000)]
        for _ in parseCSVdata(
            models.Location, chain([["name", "category"]], locations), user=user
        ):
            errors += 1
        self.assertEqual(models.Location.objects.count(), 1000)

        # Upload CSV data with 1000 demands
        # print("start demands", datetime.now())
        demands = [
            [
                "demand %s" % cnt,
                random.choice(items)[0],
                random.choice(customers)[0],
                random.choice(locations)[0],
                1,
                "2020-01-01",
            ]
            for cnt in range(1000)
        ]
        for _ in parseCSVdata(
            models.Demand,
            chain(
                [["name", "item", "customer", "location", "quantity", "due"]], demands
            ),
            user=user,
        ):
            errors += 1
        self.assertEqual(models.Demand.objects.count(), 1000)
        self.assertEqual(errors, 4)

        # The Loading is finished now, but the notifications aren't ready yet. It takes
        # longer to process all notifications and send emails by the worker.
        #
        # The real performance test is to run with and without the followers.
        # The load process should take the same time with or without the followers.
        # The time required for the notification worker instead grows with the number of
        # followers that need to be checked.
        # print("END DATA LOAD", datetime.now())
        Notification.wait()
        # print("END NOTIFICATON WORKERS", datetime.now())

        self.assertEqual(Comment.objects.count(), 4000)
        self.assertEqual(Notification.objects.count(), 6000)
