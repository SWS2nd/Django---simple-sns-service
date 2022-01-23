# tweet/models.py
from django.db import models
# user app에 있는 UserModel을 갖고 와서 사용하겠다는 의미.(ForeignKey에서 사용할 예정)
from user.models import UserModel
# 우리 글에 태그를 넣을 수 있게 해주는 매니저.
from taggit.managers import TaggableManager


# 트윗을 관리하는 tweet 테이블용
class TweetModel(models.Model):
    # DB 정보를 넣어주는 클래스
    class Meta:
        # 해당 db_table 명은 tweet로 할 것이다.
        db_table = "tweet"

    # author 변수엔 UserModel의 모든 필드를 갖고 올 것이라는 얘기.
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    # 태그 관련
    # blank=True 옵션은 비어있어도 괜찮다는 의미.(비었어도 오류 안남)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 트윗의 코멘트들을 관리하는 comment 테이블용
class TweetComment(models.Model):
    class Meta:
        db_table = "comment"
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)