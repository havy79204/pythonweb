from itertools import chain
from  django . shortcuts  import  get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . models import  Followers, LikePost, Post, Profile
from django.db.models import Q
def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')

        try:
            # Tạo người dùng
            my_user = User.objects.create_user(fnm, emailid, pwd)
            my_user.save()

            # Tạo Profile cho người dùng nếu chưa có
            user_model = User.objects.get(username=fnm)
            profile_exists = Profile.objects.filter(user=user_model).exists()

            if not profile_exists:
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()

            # Đăng nhập người dùng sau khi tạo tài khoản
            login(request, my_user)
            return redirect('/')

        except :
            invalid = "User already exists"
            return render(request, 'signup.html', {'invalid': invalid})

    return render(request, 'signup.html')
     
        
        
        
        
    

def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        print(fnm, pwd)

        # Xác thực người dùng
        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            if userr.is_active:
                login(request, userr)
                return redirect('/')
            else:
                invalid = "Account is inactive"
        else:
            invalid = "Invalid Credentials"

        return render(request, 'loginn.html', {'invalid': invalid})

    # Nếu người dùng đã đăng nhập, điều hướng tới trang chủ
    elif request.user.is_authenticated:
        return redirect('/')

    return render(request, 'loginn.html')

@login_required(login_url='/loginn')
def logoutt(request):
    logout(request)
    return redirect('/loginn')



@login_required(login_url='/loginn')
def home(request):
    # Kiểm tra và lấy Profile cho người dùng hiện tại, nếu không có thì tạo mới
    profile, created = Profile.objects.get_or_create(user=request.user)

    following_users = Followers.objects.filter(follower=request.user.username).values_list('user', flat=True)
    post = Post.objects.filter(Q(user=request.user.username) | Q(user__in=following_users)).order_by('-created_at')

    context = {
        'post': post,
        'profile': profile,
    }
    return render(request, 'main.html', context)
    


@login_required(login_url='/loginn')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='/loginn')
def likes(request, id):
    if request.method == 'GET':
        username = request.user.username
        post = get_object_or_404(Post, id=id)

        # Kiểm tra nếu người dùng đã thích bài viết này
        like_filter = LikePost.objects.filter(post_id=id, username=username).first()

        if like_filter is None:
            # Thêm mới thích
            LikePost.objects.create(post_id=id, username=username)
            post.no_of_likes += 1
        else:
            # Xóa bỏ thích
            like_filter.delete()
            post.no_of_likes -= 1

        post.save()

        # Quay lại bài viết
        return redirect(f'/{id}#post-{id}')
    
@login_required(login_url='/loginn')
def explore(request):
    post=Post.objects.all().order_by('-created_at')
    profile = Profile.objects.get(user=request.user)

    context={
        'post':post,
        'profile':profile
        
    }
    return render(request, 'explore.html',context)
    
@login_required(login_url='/loginn')
@login_required(login_url='/loginn')
def profile(request, id_user):
    user_object = User.objects.get(username=id_user)
    profile = Profile.objects.get(user=request.user)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=id_user).order_by('-created_at')
    user_post_length = len(user_posts)

    # Kiểm tra xem người dùng đã theo dõi hay chưa
    follower = request.user.username
    user = id_user
    follow_unfollow = 'Unfollow' if Followers.objects.filter(follower=follower, user=user).exists() else 'Follow'
    
    user_followers = Followers.objects.filter(user=id_user).count()
    user_following = Followers.objects.filter(follower=id_user).count()

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'profile': profile,
        'follow_unfollow': follow_unfollow,
        'user_followers': user_followers,
        'user_following': user_following,
    }

    # Cập nhật profile người dùng khi có POST request
    if request.user.username == id_user and request.method == 'POST':
        image = request.FILES.get('image', user_profile.profileimg)
        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect(f'/profile/{id_user}')

    return render(request, 'profile.html', context)
@login_required(login_url='/loginn')
def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()

    return redirect('/profile/'+ request.user.username)


@login_required(login_url='/loginn')
def search_results(request):
    query = request.GET.get('q')

    # Tìm kiếm người dùng và bài viết
    users = Profile.objects.filter(user__username__icontains=query)
    posts = Post.objects.filter(caption__icontains=query)

    context = {
        'query': query,
        'users': users,
        'posts': posts,
    }

    return render(request, 'search_user.html', context)

def home_post(request,id):
    post=Post.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    context={
        'post':post,
        'profile':profile
    }
    return render(request, 'main.html',context)



@login_required(login_url='/loginn')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        # Kiểm tra xem người dùng đã theo dõi hay chưa
        follow_instance = Followers.objects.filter(follower=follower, user=user).first()
        if follow_instance:
            # Nếu đã theo dõi, xóa theo dõi
            follow_instance.delete()
        else:
            # Nếu chưa theo dõi, thêm mới
            Followers.objects.create(follower=follower, user=user)

        return redirect(f'/profile/{user}')

    return redirect('/')
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from userauth.models import Profile
