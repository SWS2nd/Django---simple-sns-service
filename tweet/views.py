from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from django.contrib.auth.decorators import login_required
# 태그 관련(django taggit 검색)
from django.views.generic import ListView, TemplateView

# Create your views here.

def home(request):
    # 유저가 로그인 되어 있는지(인증이 되어 있는지)
    # 아래 한줄로 확인 가능.
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')


def tweet(request):
    if request.method == 'GET':
        # 요청한 사용자가 인증되었는가? 를 user 변수에 저장.
        user = request.user.is_authenticated
        # 인증된 사용자가 있다면, 로그인 되어있다면,
        if user:
            # created_at으로 tweet이 생성된 시간을 정렬해서 출력해주는 order_by() 함수 사용
            # 역순으로 출력되도록 created_at 앞에 '-'를 붙여주었다.
            # 게시글을 작성하면 최신순으로 위에서부터 보여지도록 한다.
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            # all_tweet 라는 변수를 화면에 넘겨준다.
            return render(request, 'tweet/home.html', {'tweet': all_tweet})
        else:
            return redirect('/sign-in')

    elif request.method == 'POST':
        # 요청한 사용자를 user 변수에 저장.
        # 이미 로그인 되어있기 때문에(인증 되어있기 때문에) 다시 인증할 필요없음.
        user = request.user
        content = request.POST.get('my-content', '')
        # 여러 태그가 넘어오면 ',' 구분자로 구분하여 tags 변수에 담아준다.
        tags = request.POST.get('tag', '').split(',')

        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'error': '글은 공백일 수 없습니다.', 'tweet': all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            for tag in tags:
                # 공백 제거를 위해 .strip() 사용
                tag = tag.strip()
                # 태그가 있다면
                if tag != '':
                    # my_tweet 객체의 tags 필드에 tag value 값을 추가
                    my_tweet.tags.add(tag)
            my_tweet.save()
            # 기존은 아래 4줄이고 위 두줄이 수정한 내용
            # my_tweet = TweetModel()
            # my_tweet.author = user
            # my_tweet.content = request.POST.get('my-content', '')
            # my_tweet.save()
            return redirect('/tweet')


# 로그인된 경우에만 되도록.
@login_required
# id는 url로 넘어오는 게시글의 id 값
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')


# 해당 id 트윗과 댓글들을 읽어온다.
@login_required
def detail_tweet(request, id):
    selected_tweet = TweetModel.objects.get(id=id)
    # 해당 id 트윗에 달린 모든 댓글을 최신순으로 가져오기
    all_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request, 'tweet/tweet_detail.html', {'tweet':selected_tweet, 'comment':all_comment})

# 해당 id 트윗에 댓글을 작성한다.
@login_required
def write_comment(request, id):
    if request.method == 'POST':
        my_comment = TweetComment()
        # tweet, author, comment 필드 저장.
        # created_at, updated_at은 장고가 알아서.
        my_comment.tweet = TweetModel.objects.get(id=id)
        my_comment.author = request.user
        my_comment.comment = request.POST.get('comment', '')
        my_comment.save()
        return redirect('detail-tweet', id)

# 해당 id 댓글을 삭제한다
@login_required
# 여기서 받은 id는 comment의 id
def delete_comment(request, id):
    my_comment = TweetComment.objects.get(id=id)
    my_comment.delete()
    # comment 테이블의 tweet 필드가 FK로 tweet 테이블로 연결.
    # 해당 tweet 테이블의 id를 가져옴.
    tweet_id = my_comment.tweet.id
    # 해당 id 트윗으로 넘어가야 하므로 해당 트윗의 id로 redirect
    return redirect('detail-tweet', tweet_id)


# 태그 관련(django taggit 검색)
# tag_cloud_view.html을 보여주겠다는 내용.
class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'

# 태그 관련(django taggit 검색)
# 태그가 있다면 태그를 보여주겠다는 내용.
class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context