#user/models.py
from django.db import models
# 직접 만든 UserModel을 업그레이드 하기 위함.
from django.contrib.auth.models import AbstractUser
# Many-To-Many 필드를 작성하기 위해 settings를 import
from django.conf import settings


# Create your models here.
class UserModel(AbstractUser):
    # DB 테이블의 이름을 지정해 주는 정보
    # 즉, DB의 정보를 넣어 주는 역할을 하는 곳
    class Meta:
        db_table = "my_user"

    # 상태정보
    bio = models.CharField(max_length=500, blank=True)
    # 아래 문장을 해석하면,
    # settings.AUTH_USER_MODEL 장고의 기본 설정 안의 AUTH_USER_MODEL을 FK 처럼 참조할 것인데
    # 여기서 AUTH_USER_MODEL은 우리가 mySpartaSns의 settings.py 맨 밑에
    # AUTH_USER_MODEL = 'user.UserModel' 로 우리가 만든 모델로 사용한다고 정의해 주었다.
    # 따라서, 저 settings.AUTH_USER_MODEL의 의미는 우리가 만든 UserModel을 참조하겠다는 의미이다.
    # 또한 이제부터 내가 팔로우 한 사람들은 follow 필드로,
    # 나를 팔로우 한 사람들은 followee 필드로 불러올 수 있게 된다.
    # 정리하면,
    # UserModel.followee -> 유저 모델을 팔로우 한 사람들을 불러오기
    # UserModel.follow -> 내가 팔로우 한 사람들을 불러오기.
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')

    # 아래 내용들은 auth_user를 상속 받음으로서 중복되기에 지워준다.
    # username = models.CharField(max_length=20, null=False)
    # password = models.CharField(max_length=256, null=False)
    # 생성일
    # created_at = models.DateTimeField(auto_now_add=True)
    # 수정일
    # updated_at = models.DateTimeField(auto_now=True)