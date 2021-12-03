from django.http import request, response
from django.views.generic.base import TemplateResponseMixin
from .forms import LoginForm ,SignUpForm, PostForm, QuestionForm, FollowForm, AnswerForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Account, Question, Follow, Answer
from django.contrib.auth.models import User
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
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
def follow(request, pk) :
    params = {
        'form' : FollowForm(),
    }
    #フォローするユーザーの特定
    follow_user = get_object_or_404(Account, pk=pk)

    if (request.method == "POST") :
        owner = Account.objects.get(user=request.user)
        follow_target = follow_user
        follow = Follow(owner=owner, follow_target=follow_target)
        follow_model = Follow.objects.all()
        if follow in follow_model:
            follow.delete()
        else :
            follow.save()
        return redirect('mypage', pk)
    
    return render(request, 'sns/mypage.html', params)

# class FollowBase(LoginRequiredMixin, View) :
#     def get(self, request, *args, **kwargs) :
#         #フォローするユーザーの特定
#         pk = self.kwargs['pk']
#         target_user = Account.objects.get(pk=pk)
#         #自分のフォロー情報を取得,存在しなければ作成
#         follow_info = Account.objects.get_or_create(user=self.request.user)
#         #フォローテーブルに既にユーザーが存在するか
#         if target_user in follow_info[0].following.all() :
#             obj = follow_info[0].following.remove(target_user)
#         else :
#             obj = follow_info[0].following.add(target_user)
#         return obj

# class FollowMypage(FollowBase) :
#     def get(self, request, *args, **kwargs) :
#         super().get(request, *args, **kwargs)
#         pk = self.kwargs['pk']
#         return redirect('mypage', pk)

# Top
class Top(LoginRequiredMixin, ListView) :
    model = Post
    template_name = 'sns/top.html'

    def get_queryset(self) :
        account = Account.objects.get(user=self.request.user)
        follow = Follow.objects.filter(owner = account)
        posts = Post.objects.filter(
            user__in = [f.follow_target for f in follow]
        )
        params = {
            'data' : posts,
        }
        return posts

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
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
    template_name = 'sns/post_form.html'

    def get_success_url(self) :
        return reverse('detail', kwargs={'pk': self.object.pk})

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
        success_url = reverse_lazy('mypage', kwargs={'pk': pk})
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


# Question
class QuestionTop(ListView) :     #みんなの投稿
    model = Question
    template_name = 'sns/question_top.html'

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['account_pk'] = Account.objects.get(user=self.request.user)
        return context


class QuestionCreate(CreateView) :
    form_class = QuestionForm
    template_name = 'sns/question_form.html'

    def get_success_url(self) :
        return reverse('q_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form) :
        form.instance.user = Account.objects.get(user=self.request.user)    #現在ログインしているユーザーを代入
        return super().form_valid(form)
    
    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['account_pk'] = Account.objects.get(user=self.request.user)
        return context


class QuestionDetail(CreateView) :     #AnswerCreate
    form_class = AnswerForm
    template_name = 'sns/question_detail.html'

    def form_valid(self, form) :
        form.instance.user = Account.objects.get(user=self.request.user)
        form.save_answer(self.kwargs.get('pk'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('q_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, *args, **kwargs) :
        pk = self.kwargs['pk']
        context = super().get_context_data(*args, **kwargs)
        context['question'] = Question.objects.get(pk=pk)
        context['answer_list'] = Answer.objects.filter(question_id=pk).order_by('-a_good')   #イイネの多い順にソート
        context['account_pk'] = Account.objects.get(user=self.request.user)
        return context


class QuestionUpdate(UpdateView) :
    template_name = 'sns/q_update_form.html'
    model = Question
    fields = ['title', 'text', 'q_image']

    def get_success_url(self) :
        return reverse('q_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['account_pk'] = Account.objects.get(user=self.request.user)
        return context


class QuestionDelete(DeleteView) :
    model = Question

    def get_success_url(self, *args, **kwargs) :
        pk = self.get_object().user.pk
        success_url = reverse_lazy('my_question', kwargs={'pk': pk})
        return success_url
    
    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['account_pk'] = Account.objects.get(user=self.request.user)
        return context


class MyQuestion(DetailView) :
    model = Account
    template_name = 'sns/q_mypage.html'

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['account_pk'] = Account.objects.get(user=self.request.user)
        return context

# QuestionGood
class QgoodBase(LoginRequiredMixin, View) :
    def get(self, request, *args, **kwargs) :
        #投稿の特定
        pk = self.kwargs['pk']
        target_question = Question.objects.get(pk=pk)
        account = Account.objects.get(user=self.request.user)

        if account in target_question.q_good.all() :
            obj = target_question.q_good.remove(account)
        else :
            obj = target_question.q_good.add(account)
        return obj

class Qgood(QgoodBase) :
    def get(self, request, *args, **kwargs) :
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk']
        return redirect('q_detail', pk)


# Answer
class AnswerUpdate(UpdateView):
    model = Answer
    template_name = 'sns/answer_update.html'
    fields = ['text', 'a_image']

    def get_success_url(self) :
        question_pk = Answer.objects.get(pk=self.object.pk).question.pk
        return reverse('q_detail', kwargs={'pk': question_pk})   #Questionのpk

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        question_pk = Answer.objects.get(pk=self.object.pk).question.pk
        context['question'] = Question.objects.get(pk=question_pk)
        context['account_pk'] = Account.objects.get(user=self.request.user)
        return context


class AnswerDelete(DeleteView) :
    model = Answer

    def get_success_url(self) :
        question_pk = Answer.objects.get(pk=self.object.pk).question.pk
        return reverse('q_detail', kwargs={'pk': question_pk})
    
    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['account_pk'] = Account.objects.get(user=self.request.user)
        return context


class AgoodBase(LoginRequiredMixin, View) :
    def get(self, request, *args, **kwargs) :
        #投稿の特定
        pk = self.kwargs['pk']
        print(pk)
        target_answer = Answer.objects.get(pk=pk)
        account = Account.objects.get(user=self.request.user)

        if account in target_answer.a_good.all() :
            obj = target_answer.a_good.remove(account)
        else :
            obj = target_answer.a_good.add(account)
        return obj

class Agood(AgoodBase) :
    def get(self, request, *args, **kwargs) :
        super().get(request, *args, **kwargs)
        # pk = self.kwargs['pk']
        question_pk = Answer.objects.get(pk=self.kwargs['pk']).question.pk
        return redirect('q_detail', question_pk)                #その場にとどまるにはjs