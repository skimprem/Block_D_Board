from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

CATEGORIES = [
    ('tanks', 'Танки'),
    ('hills', 'Хиллы'),
    ('damage_dealer', 'ДД'),
    ('traders', 'Торговцы'),
    ('guild_masters', 'Гилдмастеры'),
    ('quest_givers', 'Квестгиверы'),
    ('blacksmiths', 'Кузнецы'),
    ('tanners', 'Кожевники'),
    ('potion_masters', 'Зельевар'),
    ('spell_masters', 'Мастера заклинаний')
]

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default=None)
    accept = models.BooleanField(default=False)
    pub_time = models.DateTimeField(auto_now_add=True)

    def preview(self):
        return f'{self.text[0:124]}...'

    def get_absolute_url(self):
        return reverse("feedbacks")

class Advert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=14, choices=CATEGORIES, help_text='Выберите категорию', default=None)
    pub_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, help_text='Введите название', default=None)
    content = RichTextUploadingField()
    feedbacks = models.ManyToManyField(Feedback, through='AdvertFeedback')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("advert", kwargs={"pk": self.pk})

class AdvertFeedback(models.Model):
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)

class NotificationMail(models.Model):
    username = models.CharField(max_length=100)
    title = models.CharField(max_length=250)
    text = models.TextField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    link = models.URLField(max_length=200, default=None)