from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from precise_bbcode.fields import BBCodeTextField
from django.utils.safestring import mark_safe
# Create your models here.


class Character(AbstractUser):
    friends = models.ManyToManyField('self', related_name='friends_by', symmetrical=False, blank=True)#related_name='friends'

    class Meta:
        verbose_name = 'character'
        verbose_name_plural = 'characters'

    def __str__(self):
        return '{}'.format(self.username)

    def get_absolute_url(self):
        return reverse('aas:user', kwargs={'username': self.username})


class HashtagList(models.Model):
    hashtag = models.TextField(max_length=50, unique=True)
    popularity = models.IntegerField(default=0, blank=True)
    change_time = models.DateField(auto_now=True)

    def __str__(self):
        return "{}".format(self.hashtag)


class Blog(models.Model):
    owner = models.ForeignKey(Character, related_name='blog')
    pub_date = models.DateTimeField(auto_now=True)
    text = BBCodeTextField(max_length=280)
    hashtag_b = models.ManyToManyField(HashtagList, blank=True)
    dislikes = models.IntegerField(default=100)

    def __str__(self):
        return '{} {}'.format(self.owner.username, self.pub_date)

    def get_absolute_url(self):
        return reverse('aas:comments', kwargs={'username': self.owner.username, 'id':self.id})


class Commentary(models.Model):
    #path = ArrayField(models.IntegerField())
    blog = models.ForeignKey(Blog, related_name='commentary')
    content = models.TextField(max_length=280)
    pub_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(Character)
    dislikes = models.IntegerField(default=100)

    def __str__(self):
        return self.content[0:200]

    def get_offset(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return level

    def get_col(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return 12 - level
