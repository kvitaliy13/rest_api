import random
import string

from factory import Faker
from factory.django import DjangoModelFactory

from .models import AddedMPass, MPassUser, Coords, Image

locale = 'ru_RU'


def rand_str(str_len):
    r_str = ''
    for _ in range(random.randint(0, str_len)):
        r_str += random.choice(string.ascii_letters + string.digits)
    return r_str


class UserFactory(DjangoModelFactory):
    class Meta:
        model = MPassUser

    name = Faker('first_name', locale=locale)
    name_pat = Faker('middle_name', locale=locale)
    name_sur = Faker('last_name', locale=locale)
    phone = Faker('phone_number', locale=locale)
    email = Faker('ascii_email')


class CoordsFactory(DjangoModelFactory):
    class Meta:
        model = Coords

    lat = Faker('latitude')
    lon = Faker('longitude')
    height = random.randint(0, 8000)


class MPassFactory(DjangoModelFactory):
    class Meta:
        model = AddedMPass

    beauty_title = Faker('random_element', elements=['пер. ', 'г. ', ])
    title = Faker('text', max_nb_chars=random.randint(5, 20), locale=locale)
    other_titles = Faker('text', max_nb_chars=random.randint(5, 50), locale=locale)
    connects = Faker('text', max_nb_chars=random.randint(5, 40), locale=locale)
    add_time = Faker('date_time_this_decade')
    level_win = rand_str(2)
    level_spr = rand_str(2)
    level_sum = rand_str(2)
    level_aut = rand_str(2)

    user = UserFactory()
    coords = CoordsFactory()


class ImageFactory(DjangoModelFactory):
    class Meta:
        model = Image

    title = Faker('text', max_nb_chars=random.randint(5, 50), locale=locale)
    data = Faker('image')
