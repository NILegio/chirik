from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.


class Character(AbstractUser):
#    email = models.EmailField(verbose_name='email address', max_length=50, unique=True)
    friends = models.ManyToManyField('self', related_name='friends', blank=True)

    class Meta:
        verbose_name = 'character'
        verbose_name_plural = 'characters'

    def __str__(self):
        return '{}'.format(self.username)


class HashtagList(models.Model):
    hashtag = models.TextField(max_length=50, unique=True)
    popularity = models.IntegerField(default=0, blank=True)
    change_time = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return "{}".format(self.hashtag)


class Blog(models.Model):
    owner = models.ForeignKey(Character, related_name='blog')
    pub_date = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=280)
    hashtag_b = models.ManyToManyField(HashtagList, blank=True)
    dislikes = models.IntegerField(default=100)


    def __str__(self):
        return '{} {}'.format(self.owner.username, self.pub_date)


class Commentary(models.Model):
    blog = models.ForeignKey(Blog, related_name='commentary')
    text = models.TextField(max_length=280)
    pub_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(Character)
    dislikes = models.IntegerField(default=100)

    def __str__(self):
        return '{} {}'.format(self.owner.username, self.pub_date)
