from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile, Post
from .forms import PostForm, CreateUserForm

def visitor_ip_address(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required(login_url='socialNetWork:login')
def dashboard(request):
    ip_address = visitor_ip_address(request)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("like")
        if action:
            post = Post.objects.get(pk=data.get('post_id'))

            if action == "like":
                post.liked.add(current_user_profile)
                post.save()
            elif action == "dislike":
                post.liked.remove(current_user_profile)
            post.save()
        else:
            form = PostForm(request.POST or None)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect("socialNetWork:dashboard")
    form = PostForm()
    return render(request, "dashboard.html", {"form": form})

@login_required(login_url='socialNetWork:login')
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "profile_list.html", {"profiles": profiles})

@login_required(login_url='socialNetWork:login')
def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "profile.html", {"profile": profile})

def register(request):
    if request.user.is_authenticed:
        return redirect('socialNetWork:dashboard')
    else:
        form = CreateUserForm()
        if request.method=="POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Profile was created for '+ user)
                return redirect('socialNetWork:login')

        context = {'form': form}
        return render(request, "register.html", context)

@login_required(login_url='socialNetWork:login')
def logout_user(request):
    logout(request)
    return redirect('socialNetWork:login')

def login(request):
    if request.user.is_authenticated:
        return redirect('socialNetWork:dashboard')
    else:
        if request.method =='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                django_login(request, user)
                return redirect('socialNetWork:dashboard')
            else:
                messages.info(request, 'Username or password is incorrect')
                return render(request, 'login.html')
        context = {}
        return render(request, "login.html", context)

