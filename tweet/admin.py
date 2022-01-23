from django.contrib import admin
from .models import TweetModel

# Register your models here.
# 이 코드가 나의 TweetModel Admin에 추가 해 줍니다
admin.site.register(TweetModel)