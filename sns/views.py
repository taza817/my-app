from .forms import LoginForm ,SignUpForm, PostForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from .models import Post, Account
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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
        user.refresh_from_db()
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

# Top
class Top(ListView) :
    model = Post
    template_name = 'sns/top.html'
    # # paginate_by = 10
    # def get_queryset(self) :
    #     '''フォローリスト内にユーザーが含まれている場合のみクエリセット返す'''
    #     connection = Connection.objects.get_or_create(user=self.request.user)
    #     following = connection[0].following.all()
    #     return Post.objects.filter(user__in=following)     #フォローしていればオブジェクトを返す


# Post
class PostList(ListView) :
    model = Post


class PostDetail(DetailView) :
    model = Post


class PostCreate(LoginRequiredMixin, CreateView) :
    form_class = PostForm
    success_url = reverse_lazy('top')
    template_name = 'sns/post_form.html'

    def form_valid(self, form) :
        form.instance.user_id = self.request.user     #現在ログインしているユーザーを代入
        return super().form_valid(form)



class PostUpdate(UpdateView) :
    template_name = 'sns/post_update_form.html'
    model = Post
    fields = ['caption']

    def get_success_url(self) :
        return reverse('detail', kwargs={'pk': self.object.pk})

class PostDelete(DeleteView) :
    model = Post
    success_url = reverse_lazy('post_list')



