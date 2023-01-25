import json
import random

from django.shortcuts import reverse
from django.utils.timezone import make_aware
from factory.faker import faker
from rest_framework.test import APITestCase

from .factories import MPassFactory, CoordsFactory, UserFactory, ImageFactory
from .models import Image, AddedMPass


class BaseTestCase(APITestCase):
    report = None
    coords = None
    user = None
    images_count = None

    report1 = None
    coords1 = None
    user1 = None
    images_count1 = None

    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()

        fake = faker.Faker()

        cls.coords = CoordsFactory()
        cls.user = UserFactory(
            email='test@test.test'
        )
        cls.report = MPassFactory(
            user=cls.user,
            coords=cls.coords,
            add_time=make_aware(fake.date_time_this_decade()),
        )
        cls.images_count = random.randint(1, 5)
        for _ in range(cls.images_count):
            cls.last_image = ImageFactory(
                mpass=cls.report
            )

        cls.coords1 = CoordsFactory()
        cls.user1 = UserFactory()
        cls.report1 = MPassFactory(
            user=cls.user1,
            coords=cls.coords1,
            add_time=make_aware(fake.date_time_this_decade()),
            status='pending'
        )
        cls.images_count1 = random.randint(1, 5)
        for _ in range(cls.images_count1):
            cls.last_image1 = ImageFactory(
                mpass=cls.report1
            )


class AppModelsTestCase(BaseTestCase):

    def test_user_created_properly(self):
        self.assertEqual(self.user.username, 'test@test.test')

    def test_report_status_set(self):
        self.assertEqual(self.report.status, 'new')

    def test_images_created(self):
        self.assertEqual(Image.objects.filter(mpass=self.report).count(), self.images_count)


class AppInterfaceTestCase(BaseTestCase):

    def test_get_submit_not_allowed(self):
        path = reverse('mpass-list')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['message'], 'Method "GET" not allowed.')

    def test_put_submit_ok(self):
        path = reverse('mpass-list')
        data = {
            'beauty_title': 'cons',
            'title': 'Excepteur',
            'add_time': '1969-08-21T23:17:55.0Z',
            'coords': {
                'latitude': -90901551.14551522,
                'longitude': 48394979.318392396,
                'height': -83112821
            },
            'user': {
                'email': 'u48me8TQuCS@eyqEFRIYVDGEGw.jt',
                'name': 'incididunt do aliqua',
                'otc': 'minim',
                'phone': 'magna es',
                'fam': 'anim Ut'
            },
            'id': 2017,
            'status': 'pending',
            'connect': 'labore elit',
            'level': {
                'autumn': 'si',
                'summer': '',
                'winter': '',
                'spring': ''
            },
            'other_titles': 'ullamco nostrud ea ex ut',
            'images': [
                {
                    'title': 'est culpa enim tempor occaecat',
                    'data': 'aliquip'
                }]
        }
        response = self.client.post(path, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(True, AddedMPass.objects.filter(id=response.json()['id']).exists())

    def test_get_report_ok(self):
        path = reverse('mpass-detail', args=[self.report.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.report.id)

    def test_get_report_not_found(self):
        path = reverse('mpass-detail', args=[9999])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['message'], 'Not found.')

    def test_get_filtered_empty(self):
        path = reverse('mpass-list-filtered')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_filtered_ok(self):
        path_base = reverse('mpass-list-filtered')
        path = f'{path_base}?user_email={self.user.email}'
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)

    def test_patch_ok(self):
        path = reverse('mpass-detail', args=[self.report.id])
        data = {
            'title': 'foo / bar'
        }
        response = self.client.patch(path, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state'], 1)
        self.assertEqual(AddedMPass.objects.get(id=self.report.id).title, 'foo / bar')

    def test_patch_not_found(self):
        path = reverse('mpass-detail', args=[9999])
        response = self.client.patch(path)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['state'], 0)
        self.assertEqual(response.json()['message'], 'Not found.')

    def test_patch_forbidden(self):
        path = reverse('mpass-detail', args=[self.report1.id])
        response = self.client.patch(path)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['state'], 0)
        self.assertEqual(response.json()['message'], 'Object status forbids changes')
