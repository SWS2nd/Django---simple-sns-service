# flask의 render_template 함수와 마찬가지로
# html 파일을 화면에 보여주는 역할을 하는 render 함수.
# 회원가입 완료 후 곧바로 로그인 url로 넘어가기 위한 rediect 함수.
from django.shortcuts import render, redirect
# 현재 app 내 models.py의 직접 작성한 UserModel 클래스를 가져옴.
from .models import UserModel
# 로그인 성공시 로그인 성공이라는 메시지를
# 화면에 출력하기 위해 HttpResponse 함수를 import.
from django.http import HttpResponse
# 사용자가 DB 안에 있는지 검사하는 함수.
from django.contrib.auth import get_user_model
# sha256 암호화 되어 db에 저장된 비밀번호와 사용자가 입력한 비밀번호를 비교하여
# 맞는지 검증을 위한 장고의 기능을 사용하기 위해 auth를 import
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')

    elif request.method == 'POST':
        # 뒤쪽의 None은 POST로 넘겨받은 데이터 중에 'username'이 없다면
        # None으로 처리하겠다는 의미.
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        # 회원가입시 비밀번호가 같아야 되는 부분을 작성.
        # 비밀번호와 비밀번호 확인이 같지 않다면,
        # GET에서 작성한 signup.html을 다시 보여줄 것이다.
        if password != password2:
            # 패스워드가 같지 않다고 알림
            return render(request, 'user/signup.html', {'error':'패스워드를 확인 해 주세요!'})
        else:
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error': '사용자 이름과 비밀번호는 필수 입력 값 입니다!'})
            else:
                # 사용자가 DB 안에 있는지 검사하는 함수인 get_user_model()을 사용하여 필터링.
                exist_user = get_user_model().objects.filter(username=username)
                # 회원가입시 my_user db에 동일한 username이 있다면 가입되지 않도록 한다.
                if exist_user:
                    return render(request, 'user/signup.html', {'error': '사용자가 이미 존재합니다.'})
                else:
                    # 원래라면 클래스에서 객체를 생성해서 해당 객체의 각 변수에
                    # 받아온 내용을 넣고 db에 저장하는 코드들이 필요할 것이다.
                    # 아래처럼 마치 클래스를 사용하듯이 작성후 저장까지 해줘야 하는데
                    # new_user = UserModel()
                    # new_user.username = username
                    # new_user.password = password
                    # new_user.bio = bio
                    # 이제 데이터베이스에 저장!
                    # new_user.save()

                    # 위의 긴 작업을 아래와 같이 단 한줄로 바꿔줄 수 있다.
                    # create_user() 함수는 상속받은 AbstractUser 클래스에서 제공해주는 함수이다. 이를 사용!
                    UserModel.objects.create_user(username=username, password=password, bio=bio)
                    # 회원가입 후 로그인 페이지가 보이도록
                    # 맨 위에 from django.shortcuts import render, redirect 추가해주고
                    # 로그인 url을 적어주면 됨.
                    return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            # urls.py에 정의한 name을 써도 되며, 상대, 절대 경로 모두 가능
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # 기존 db에 작성된 회원과 일치하는지 확인 작업.
        # 직접 작성한 UserModel()은 데이터베이스와 연결되어 있는 객체, 클래스라고 생각.
        # 그 객체 안의 username 필드의 값이 사용자로부터 입력 받은 username과 동일한 유저(objects)를 가져오고 싶다는 의미.
        # 만약 없을 경우 이 부분을 통과하지 못할 것이다.

        # me = UserModel.objects.get(username=username)
        # 위와 같이 UserModel을 불러오는게 아니라 인증 모델을 불러온다.
        # auth의 authenticate() 함수는 username과 암호화된 password까지 비교를 해주는 강력한 기능의 함수이다!
        me = auth.authenticate(request, username=username, password=password)

        # 불러온 유저 객체의 password 필드의 값이 사용자로부터 입력받은 password와 같다면,
        # if me.password == password:
        # 위와 같이 비밀번호를 비교하는게 아니라, 사용자가 있는지 없는지만 구분해주면 됨.
        if me is not None: # me가 있으면,
            # session(사용자 정보를 저장할 수 있는 공간)에 user를 넣을 것이다.
            # request.session['user'] = me.username
            # 위처럼 작성하지 않고, 장고가 알아서 관리할 수 있도록 auth.login() 함수를 사용.
            auth.login(request, me)
            # 로그인시 HttpResponse()를 사용하여 사용자의 username이 보이도록 하기.
            # return HttpResponse(me.username)
            # 이제 로그인시 제대로 home.html이 보여지도록 바꿔준다.
            return redirect('/')
        else:
            # 에러 로그를 보내주기 위해 render
            return render(request, 'user/signin.html', {'error': '유저이름 혹은 패스워드를 확인 해 주세요.'})


# from django.contrib.auth.decorators import login_required
# 사용자가 꼭 로그인이 되어있어야만 접근이 가능한 함수라고 정의해준것. 데코레이터!
@login_required
def logout(request):
    # 이 한줄이 정말 강력한 작업
    auth.logout(request)
    # 만약 장고를 사용하지 않았다면, 위와 같은 한줄이 아닌
    # 지금 request에 사용자가 있는지 없는지 세션에서 확인을 해야되고
    # 그 안에 값이 있다면 없애주는 작업들을 여러군데 작성해야 한다.
    return redirect('/')



# user/views.py

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    # 로그인한 사용자
    me = request.user
    # 내가 누른 사용자가 click_user가 됨.
    click_user = UserModel.objects.get(id=id)
    # 내가 누른 사용자를 팔로우 한 모든 사용자를 갖고 오는데 그 안에 내가 있다면,
    if me in click_user.followee.all():
        # 내가 누른 사용자를 팔로우 한 사용자 목록에서 나를 제외시킨다.(팔로우 해제)
        click_user.followee.remove(request.user)
    # 내가 누른 사용자의 팔로우 목록에 내가 없다면,
    else:
        # 내가 누른 사용자의 팔로우 목록에 나를 추가 시킨다.
        click_user.followee.add(request.user)
    return redirect('/user')