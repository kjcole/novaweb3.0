from django.contrib import admin
from forums.models import Category, Thread, Post, Document

admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Document)
