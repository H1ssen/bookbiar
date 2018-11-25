from django.contrib import admin
from . import models
admin.site.register(models.Author)

admin.site.register(models.Translator)
# Register your models here.
admin.site.register(models.Book)
admin.site.register(models.Categori)
admin.site.register(models.Carousel)
admin.site.register(models.Publisher)
admin.site.register(models.Banner)
admin.site.register(models.topCarousel)