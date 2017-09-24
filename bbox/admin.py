from django.contrib import admin

from .models import Account
from .models import FeedingLog
from .models import SystemSetting
from .models import FoodBox
from .models import SystemLog
from .models import Card

admin.site.register(Account)
admin.site.register(FeedingLog)
admin.site.register(SystemSetting)
admin.site.register(FoodBox)
admin.site.register(SystemLog)
admin.site.register(Card)
