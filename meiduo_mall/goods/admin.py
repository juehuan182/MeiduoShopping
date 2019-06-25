from django.contrib import admin
from .models import Content, ContentCategory

# Register your models here.
admin.site.register(ContentCategory)
admin.site.register(Content)

