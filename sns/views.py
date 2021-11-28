from django.http import request
from django.views.generic.base import TemplateResponseMixin
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
            intro = form.cleaned_data.get('intro')
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
        target_user = Account.objects.get(pk=pk)
        #自分のフォロー情報を取得,存在しなければ作成
        follow_info = Account.objects.get_or_create(user=self.request.user)
        #フォローテーブルに既にユーザーが存在するか
        if target_user in follow_info[0].following.all() :
            obj = follow_info[0].following.remove(target_user)
        else :
            obj = follow_info[0].following.add(target_user)
        return obj

class FollowMypage(FollowBase) :
    def get(self, request, *args, **kwargs) :
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk']
        return redirect('mypage', pk)



# Top
class Top(LoginRequiredMixin, ListView) :
    model = Post
    template_name = 'sns/top.html'

    def get_queryset(self) :
        #フォローリスト内にユーザーが含まれている場合のみクエリセット返す
        follow_info = Account.objects.get_or_create(user=self.request.user)
        following = follow_info[0].following.all()
        return Post.objects.filter(user__in=following).order_by('-post_date')

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['following'] = Account.objects.get_or_create(user=self.request.user)
        context['account_pk'] = Account.objects.get(user=self.request.user)
        return context


# Mypage
class Mypage(DetailView) :
    template_name = 'sns/mypage.html'
    model = Account

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['connection'] = Account.objects.get_or_create(user=self.request.user)
        context['account_pk'] = Account.objects.get(user=self.request.user)
        return context


# Post
class PostDetail(DetailView) :
    model = Post

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['account_pk'] = Account.objects.get(user=self.request.user)
        return context


class PostCreate(LoginRequiredMixin, CreateView) :
    form_class = PostForm
    success_url = reverse_lazy('top')
    template_name = 'sns/post_form.html'

    def form_valid(self, form) :
        form.instance.user = Account.objects.get(user=self.request.user)    #現在ログインしているユーザーを代入
        return super().form_valid(form)
    
    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['account_pk'] = Account.objects.get(user=self.request.user)
        return context



class PostUpdate(UpdateView) :
    template_name = 'sns/post_update_form.html'
    model = Post
    fields = ['caption', 'post_tag']

    def get_success_url(self) :
        return reverse('detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['account_pk'] = Account.objects.get(user=self.request.user)
        return context


class PostDelete(DeleteView) :
    model = Post

    def get_success_url(self, *args, **kwargs) :
        pk = self.get_object().user.pk
        success_url = reverse_lazy('mypage', kwargs={'pk': pk})   #accountのpk渡す
        return success_url
    
    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['account_pk'] = Account.objects.get(user=self.request.user)
        return context



# Good
class GoodBase(LoginRequiredMixin, View) :
    def get(self, request, *args, **kwargs) :
        #記事の特定
        pk = self.kwargs['pk']
        related_post = Post.objects.get(pk=pk)

        if self.request.user in related_post.good.all() :
            obj = related_post.good.remove(self.request.user)
        else :
            obj = related_post.good.add(self.request.user)
        return obj

class GoodTop(GoodBase) :
    def get(self, request, *args, **kwargs) :
        super().get(request, *args, **kwargs)
        return redirect('top')                 #その場にとどまるにはjs

class GoodDetail(GoodBase) :
    def get(self, request, *args, **kwargs) :
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk']
        return redirect('detail', pk)


