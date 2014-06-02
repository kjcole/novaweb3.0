from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    created_by = models.ForeignKey(User)
    title = models.CharField(max_length=100, null=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.title

class Thread(models.Model):
    category = models.ForeignKey(Category)
    created_by = models.ForeignKey(User)
    title = models.CharField(max_length=100, null=False)

    def __unicode__(self):
        return self.title

class Post(models.Model):
    poster = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)
    post = models.TextField(max_length=1000, null=False)
    image = models.ImageField(upload_to='forum_images/%Y/%m/%d', blank=True, null=True)
    document = models.FileField(upload_to='forum_docs/%Y/%m/%d', blank=True, null=True)
    
    def __unicode__(self):
        return "%s : %s" % (self.thread, self.post)

class Document(models.Model):
    poster = models.ForeignKey(User)
    file_name = models.CharField(max_length=50)
    reports = models.FileField(upload_to='reports_docs/%Y/%m/%d', blank=True, null=True)

    def __unicode__(self):
        return self.file_name
