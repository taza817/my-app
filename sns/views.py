from .forms import LoginForm ,SignUpForm, PostForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from .models import Post, Account
from django.contrib.auth.models import User
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# SignUp
class SignUp(CreateView) :
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'sns/signup_form.html'
    
    def form_valid(self, form) :     # バリデーションがうまくいったとき
        ret_val = super().form_valid(form)
        user = self.object
        Account.objects.create(     #フォームに入力した値でオブジェクト（レコード）を作成
            user = user,
            gender = form.cleaned_data.get('gender'),
            birth_date = form.cleaned_data.get('birth_date'),
            location = form.cleaned_data.get('location'),
            # intro = form.cleaned_data.get('intro')
        )
        return ret_val


# Login
class Login(LoginView) :
    form_class = LoginForm
    template_name = 'sns/login.html'

class Logout(LogoutView) :
    template_name = 'sns/logout.html'


# Follow
class FollowBase(LoginRequiredMixin, View) :
    def get(self, request, *args, **kwargs) :
        #フォローするユーザーの特定
        pk = self.kwargs['pk']
        print(pk)
        target_user = Account.objects.get(pk=pk)
        print(target_user)
        #自分のフォロー情報を取得,存在しなければ作成
        follow_info = Account.objects.get_or_create(user=self.request.user)
        print(follow_info)
        #フォローテーブルに既にユーザーが存在するか
        if target_user in follow_info[0].following.all() :
            obj = follow_info[0].following.remove(target_user)
        else :
            obj = follow_info[0].following.add(target_user)
        print(obj)
        return obj

class FollowMypage(FollowBase) :
    def get(self, request, *args, **kwargs) :
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk']
        print(pk)
        return redirect('mypage', pk)



# Top
class Top(LoginRequiredMixin, ListView) :
    model = Post
    template_name = 'sns/top.html'

    def get_queryset(self) :
        #フォローリスト内にユーザーが含まれている場合のみクエリセット返す
        follow_info = Account.objects.get_or_create(user=self.request.user)
        following = follow_info[0].following.all()
        # return Post.objects.all().order_by('-post_date')
        return Post.objects.filter(user__in=following).order_by('-post_date')

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['following'] = Account.objects.get_or_create(user=self.request.user)
        return context


# Mypage
class Mypage(DetailView) :
    template_name = 'sns/mypage.html'
    model = Account

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['connection'] = Account.objects.get_or_create(user=self.request.user)
        return context


# Post
class PostDetail(DetailView) :
    model = Post


class PostCreate(LoginRequiredMixin, CreateView) :
    form_class = PostForm
    success_url = reverse_lazy('top')
    template_name = 'sns/post_form.html'

    def form_valid(self, form) :
        form.instance.user = Account.objects.get(user=self.request.user)    #現在ログインしているユーザーを代入
        return super().form_valid(form)



class PostUpdate(UpdateView) :
    template_name = 'sns/post_update_form.html'
    model = Post
    fields = ['caption']

    def get_success_url(self) :
        return reverse('detail', kwargs={'pk': self.object.pk})

class PostDelete(DeleteView) :
    model = Post
    success_url = reverse_lazy('top')



