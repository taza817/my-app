from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import UserCreateForm, LoginForm
from .models import Post
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

# Create your views here.



#CreateAccount
class Create_account(CreateView) :
    def post(self, request, *args, **kwargs) :
        form = UserCreateForm(data=request.POST)     #mothod=POSTのデータをフォームに保存
        if form.is_valid() :
            #受け取ったデータをDBに保存
            form.save()
            #フォームから値を取得し，データ型に応じて整形
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            username = form.cleaned_data.get('username')
            last_name = form.cleaned_data.get('last_name')
            #ユーザー認証
            user = authenticate(username=username, password=password)
            #ログイン
            login(request, user)
            return redirect('/login/')   #成功後のurl
        return render(request, 'sns/create_account_form.html', {'form': form})
    
    def get(self, request, *args, **kwargs) :
        form = UserCreateForm(request.POST)     #フォームを作成
        return render(request, 'sns/create_account_form.html', {'form': form})     #テンプレートに描画


#Login
class Account_login(View) :
    def post(self, request, *args, **kwargs) :
        form = LoginForm(data=request.POST)
        if form.is_valid() :
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('/')
        return render(request, 'sns/login.html', {'form': form})
    
    def get(self, request, *args, **kwargs) :
        form = LoginForm(request.POST)
        return render(request, 'sns/login.html', {'form': form})


# @login_required 


# Post
class PostList(ListView) :
    model = Post


class PostDetail(DetailView) :
    model = Post


class PostCreate(CreateView) :
    model = Post
    fields = ['caption']
    success_url = reverse_lazy('post_list')


class PostUpdate(UpdateView) :
    template_name = 'sns/post_update_form.html'
    model = Post
    fields = ['caption']

    def get_success_url(self) :
        return reverse('detail', kwargs={'pk': self.object.pk})

class PostDelete(DeleteView) :
    model = Post
    success_url = reverse_lazy('post_list')

