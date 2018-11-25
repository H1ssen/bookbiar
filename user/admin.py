from django.contrib import admin
from .models import UserProfile,cardItem,card,Address
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(cardItem)
admin.site.register(Address)
admin.site.register(card)

