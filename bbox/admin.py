from django.contrib import admin

from .models import Account
from .models import FeedingLog
from .models import SystemSettings
from .models import FoodBox
from .models import SystemLog


admin.site.register(Account)
admin.site.register(FeedingLog)
admin.site.register(SystemSettings)
admin.site.register(FoodBox)
admin.site.register(SystemLog)
