from django.contrib import admin
from .models import UserModel

# Register your models here.
# 이 코드가 나의 UserModel을 Admin에 추가 해 줍니다
admin.site.register(UserModel)