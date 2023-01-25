from django.contrib.auth.models import AbstractUser
from django.db import models


class MPassUser(AbstractUser):
    name = models.CharField(verbose_name='first name', max_length=255)
    name_sur = models.CharField(verbose_name='surname', max_length=255)
    name_pat = models.CharField(verbose_name='patronymic',
                                max_length=255,
                                null=True,
                                blank=True)
    phone = models.CharField(verbose_name='phone number',
                             max_length=20,
                             null=True,
                             blank=True)
    email = models.EmailField(verbose_name='e-mail', unique=True, max_length=255)

    class Meta:
        db_table = 'pereval_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = self.email
        super(MPassUser, self).save(*args, **kwargs)


class Coords(models.Model):
    lat = models.FloatField(verbose_name='latitude')
    lon = models.FloatField(verbose_name='longitude')
    height = models.IntegerField()

    class Meta:
        db_table = 'pereval_coords'
        verbose_name = 'mountain pass coordinates'
        verbose_name_plural = "mountain passes' coordinates"


class AddedMPass(models.Model):
    STATUS_NEW = 'new'
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_NEW, STATUS_NEW),
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_ACCEPTED, STATUS_ACCEPTED),
        (STATUS_REJECTED, STATUS_REJECTED),
    ]

    beauty_title = models.CharField(verbose_name='object type', max_length=30)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(verbose_name='other titles', max_length=255)
    connects = models.CharField(verbose_name='pass connects', max_length=255)
    level_win = models.CharField(verbose_name='winter difficulty level',
                                 max_length=2,
                                 null=True,
                                 blank=True)
    level_spr = models.CharField(verbose_name='spring difficulty level',
                                 max_length=2,
                                 null=True,
                                 blank=True)
    level_sum = models.CharField(verbose_name='summer difficulty level',
                                 max_length=2,
                                 null=True,
                                 blank=True)
    level_aut = models.CharField(verbose_name='autumn difficulty level',
                                 max_length=2,
                                 null=True,
                                 blank=True)
    add_time = models.DateTimeField(verbose_name='added on')
    coords = models.ForeignKey(Coords, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(MPassUser, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default=STATUS_NEW)

    class Meta:
        db_table = 'pereval_added'
        verbose_name = 'added mountain pass'
        verbose_name_plural = 'added mountain passes'

    def get_levels(self):
        return {
            'winter': self.level_win,
            'spring': self.level_spr,
            'summer': self.level_sum,
            'autumn': self.level_aut,
        }

    def set_levels(self, **kwargs):
        self.level_win = kwargs.get('winter', '')
        self.level_spr = kwargs.get('spring', '')
        self.level_sum = kwargs.get('summer', '')
        self.level_aut = kwargs.get('autumn', '')
        self.save()


class Image(models.Model):
    mpass = models.ForeignKey(AddedMPass,
                              related_name='mpass_images',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    data = models.BinaryField(null=True)

    class Meta:
        db_table = 'pereval_images'
        verbose_name = 'mountain pass image'
        verbose_name_plural = "mountain passes' images"
