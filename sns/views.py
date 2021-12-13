from django.http import request, response
from django.views.generic.base import TemplateResponseMixin
from .forms import LoginForm ,SignUpForm, PostForm, QuestionForm, FollowForm, AnswerForm, PasswordChangeForm, ProfileEditForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Account, Question, Follow, Answer, QuestionTag
from django.contrib.auth.models import User
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count

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

# UserDelete
class OnlyYouMixin(UserPassesTestMixin) :
    raise_exception = True

    def test_func(self) :
        account = Account.objects.get(user=self.request.user)
        is_this_page_user = account.user.pk == self.kwargs['pk']
        is_this_page_account = account.pk == self.kwargs['pk']
        return is_this_page_user or is_this_page_account or account.user.is_superuser

class UserDelete(OnlyYouMixin, DeleteView) :
    model = User
    template_name = 'sns/user_confirm_delete.html'
    success_url = reverse_lazy('app_top')

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
        return context


# Login
class Login(LoginView) :
    form_class = LoginForm
    template_name = 'sns/login.html'

class Logout(LogoutView) :
    template_name = 'sns/logout.html'


# Setting
class AccountSetting(OnlyYouMixin, UpdateView) :
    model = User
    fields = ('email', 'username', 'first_name')
    template_name = 'sns/account_setting.html'
    
    def get_success_url(self) :
        pk = Account.objects.get(user=self.request.user).pk
        return reverse('mypage', kwargs={'pk': pk})
    
    def get_object(self) :
        return self.request.user

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
        return context

class PasswordChange(OnlyYouMixin, PasswordChangeView) :
    form_class = PasswordChangeForm
    template_name = 'sns/password_change.html'

    def get_success_url(self) :
        pk = Account.objects.get(user=self.request.user).pk
        return reverse('account_setting', kwargs={'pk':pk})


# ProfileEdit
class ProfileEdit(LoginRequiredMixin, OnlyYouMixin, UpdateView) :
    model = Account
    form_class = ProfileEditForm
    template_name = 'sns/profile_update_form.html'

    def get_object(self) :
        account = Account.objects.get(user=self.request.user)
        return account

    def get_success_url(self) :
        pk = Account.objects.get(user=self.request.user).pk
        return reverse('mypage', kwargs={'pk': pk})
    
    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
        return context


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
        Follow.objects.get_or_create(owner=owner, follow_target=follow_target)
        return redirect('mypage', pk)
    
    return render(request, 'sns/mypage.html', params)


def unfollow(request, pk) :
    params = {
        'form' : FollowForm(),
    }
    #アンフォローするユーザーの特定
    follow_user = get_object_or_404(Account, pk=pk)

    if (request.method == "POST") :
        owner = Account.objects.get(user=request.user)
        follow_target = follow_user
        Follow.objects.get(owner=owner, follow_target=follow_target).delete()
        return redirect('mypage', pk)
    
    return render(request, 'sns/mypage.html', params)



# Top
class AppTop(ListView) :
    model = Post
    template_name = 'sns/app_top.html'


class Top(LoginRequiredMixin, ListView) :
    model = Post
    template_name = 'sns/top.html'

    def get_queryset(self) :
        account = Account.objects.get(user=self.request.user)
        follow = Follow.objects.filter(owner = account)
        posts = Post.objects.filter(Q(user__in = [f.follow_target for f in follow]) | Q(user=account))
        return posts


    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
        return context


# Mypage
class Mypage(DetailView) :
    template_name = 'sns/mypage.html'
    model = Account

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
        try :
            context['follow_data'] = Follow.objects.get(
                owner=Account.objects.get(user=self.request.user), 
                follow_target=Account.objects.get(pk=self.kwargs['pk'])
                )
        except Follow.DoesNotExist :
            pass
        context['follow_list'] = Follow.objects.filter(owner=Account.objects.get(pk=self.kwargs['pk']))
        context['follower_list'] = Follow.objects.filter(follow_target=Account.objects.get(pk=self.kwargs['pk']))
        return context


# Post
class PostDetail(DetailView) :
    model = Post

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
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
        context['self_account'] = Account.objects.get(user=self.request.user)
        return context



class PostUpdate(UpdateView) :
    template_name = 'sns/post_update_form.html'
    model = Post
    form_class = PostForm

    def get_success_url(self) :
        return reverse('detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
        return context


class PostDelete(DeleteView) :
    model = Post

    def get_success_url(self, *args, **kwargs) :
        pk = self.get_object().user.pk
        success_url = reverse_lazy('mypage', kwargs={'pk': pk})
        return success_url
    
    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
        return context


# PostSearch
class PostSearch(ListView) :
    model = Post
    template_name = 'sns/post_search.html'

    def get_queryset(self) :
        q_word = self.request.GET.get('query')
        if q_word :
            posts = Post.objects.filter(Q(caption__icontains=q_word))
        else :
            posts = Post.objects.order_by('?')[:10]   #デフォルトで表示する投稿 ランダムに10件
        return posts
    
    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
        return context


# AccountSearch
class AccountSearch(ListView) :
    model = Account
    template_name = 'sns/account_search.html'

    def get_queryset(self) :
        q_word = self.request.GET.get('query')
        if q_word :
            user = User.objects.filter(Q(username__icontains=q_word) | Q(first_name__icontains=q_word))
            account = Account.objects.filter(Q(user__in=user) | Q(intro__icontains=q_word) | Q(location__icontains=q_word))
        else :
            account = Account.objects.order_by('?')[:10]
        return account
    
    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
        return context


# Good
class GoodBase(LoginRequiredMixin, View) :
    def add(self, request, *args, **kwargs) :
        #記事の特定
        pk = self.kwargs['pk']
        related_post = Post.objects.get(pk=pk)
        object = related_post.good.add(self.request.user)
        return object
    
    def remove(self, request, *args, **kwargs) :
        #記事の特定
        pk = self.kwargs['pk']
        related_post = Post.objects.get(pk=pk)
        object = related_post.good.remove(self.request.user)
        return object


class GoodTop(GoodBase) :
    def get(self, request, *args, **kwargs) :
        super().add(request, *args, **kwargs)
        return redirect('top')                 #その場にとどまるにはjs

class GoodTop_remove(GoodBase) :
    def get(self, request, *args, **kwargs) :
        super().remove(request, *args, **kwargs)
        return redirect('top')

class GoodDetail(GoodBase) :
    def get(self, request, *args, **kwargs) :
        super().add(request, *args, **kwargs)
        pk = self.kwargs['pk']
        return redirect('detail', pk)

class GoodDetail_remove(GoodBase) :
    def get(self, request, *args, **kwargs) :
        super().remove(request, *args, **kwargs)
        pk = self.kwargs['pk']
        return redirect('detail', pk)



# Question
class QuestionTop(ListView) :     #みんなの投稿
    model = Question
    template_name = 'sns/question_top.html'

    def get_queryset(self) :
        q_word = self.request.GET.get('query')
        if q_word :
            questions = Question.objects.filter(Q(title__icontains=q_word) | Q(text__icontains=q_word))
        else :
            questions = Question.objects.order_by('?')[:10]
        return questions

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
        context['tag_rank'] = QuestionTag.objects.all().order_by('-tag_count')[0:10]
        return context


class QuestionCreate(CreateView) :
    form_class = QuestionForm
    template_name = 'sns/question_form.html'

    def get_success_url(self) :
        account = Account.objects.get(user=self.request.user)
        return reverse('my_question', account.pk)

    def form_valid(self, form) :
        # super().form_valid(form)
        question = Question(
            user = Account.objects.get(user=self.request.user),    #現在ログインしているユーザーを代入
            title = form.cleaned_data["title"],
            q_image = form.cleaned_data["q_image"],
            text = form.cleaned_data["text"]
        )
        question.save()

        words = form.cleaned_data["text"].split()
        for word in words :
            if word[0] == "#" :
                if QuestionTag.objects.filter(name=word[1:]).exists() :
                    tag = QuestionTag.objects.get(name=word[1:])
                else :
                    tag = QuestionTag.objects.create(name=word[1:])
                tag.tag_count += 1
                tag.save()
                question.question_tag.add(tag)

        account = Account.objects.get(user=self.request.user)
        return redirect('my_question', account.pk)

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
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
        context['answer_list'] = Answer.objects.filter(question_id=pk).annotate(Count('a_good')).order_by('-a_good__count')   #イイネの多い順にソート
        context['self_account'] = Account.objects.get(user=self.request.user)
        return context


class QuestionUpdate(UpdateView) :
    template_name = 'sns/question_update_form.html'
    model = Question
    form_class = QuestionForm

    def get_success_url(self) :
        return reverse('q_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
        return context


class QuestionDelete(DeleteView) :
    model = Question

    def get_success_url(self, *args, **kwargs) :
        pk = self.get_object().user.pk
        success_url = reverse_lazy('my_question', kwargs={'pk': pk})
        return success_url
    
    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
        return context


class MyQuestion(DetailView) :
    model = Account
    template_name = 'sns/question_mypage.html'

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
        return context


# QuestionGood
class QuestionGoodBase(LoginRequiredMixin, View) :
    def add(self, request, *args, **kwargs) :
        #投稿の特定
        pk = self.kwargs['pk']
        target_question = Question.objects.get(pk=pk)
        account = Account.objects.get(user=self.request.user)
        object = target_question.question_good.add(account)
        return object
    
    def remove(self, request, *args, **kwargs) :
        #投稿の特定
        pk = self.kwargs['pk']
        target_question = Question.objects.get(pk=pk)
        account = Account.objects.get(user=self.request.user)
        object = target_question.question_good.remove(account)
        return object

class QuestionGood(QuestionGoodBase) :
    def get(self, request, *args, **kwargs) :
        super().add(request, *args, **kwargs)
        pk = self.kwargs['pk']
        return redirect('question_detail', pk)

class QuestionGood_remove(QuestionGoodBase) :
    def get(self, request, *args, **kwargs) :
        super().remove(request, *args, **kwargs)
        pk = self.kwargs['pk']
        return redirect('question_detail', pk)


# Answer
class AnswerUpdate(UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'sns/answer_update.html'

    def get_success_url(self) :
        question_pk = Answer.objects.get(pk=self.object.pk).question.pk
        return reverse('question_detail', kwargs={'pk': question_pk})   #Questionのpk

    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        question_pk = Answer.objects.get(pk=self.object.pk).question.pk
        context['question'] = Question.objects.get(pk=question_pk)
        context['self_account'] = Account.objects.get(user=self.request.user)
        return context


class AnswerDelete(DeleteView) :
    model = Answer

    def get_success_url(self) :
        question_pk = Answer.objects.get(pk=self.object.pk).question.pk
        return reverse('question_detail', kwargs={'pk': question_pk})
    
    def get_context_data(self, *args, **kwargs) :
        context = super().get_context_data(*args, **kwargs)
        context['self_account'] = Account.objects.get(user=self.request.user)
        return context


class AnswerGoodBase(LoginRequiredMixin, View) :
    def add(self, request, *args, **kwargs) :
        #投稿の特定
        pk = self.kwargs['pk']
        target_answer = Answer.objects.get(pk=pk)
        account = Account.objects.get(user=self.request.user)
        object = target_answer.answer_good.add(account)
        return object

    def remove(self, request, *args, **kwargs) :
        #投稿の特定
        pk = self.kwargs['pk']
        target_answer = Answer.objects.get(pk=pk)
        account = Account.objects.get(user=self.request.user)
        object = target_answer.answer_good.remove(account)
        return object

class AnswerGood(AnswerGoodBase) :
    def get(self, request, *args, **kwargs) :
        super().add(request, *args, **kwargs)
        question_pk = Answer.objects.get(pk=self.kwargs['pk']).question.pk
        return redirect('question_detail', question_pk)                #その場にとどまるにはjs

class AnswerGood_remove(AnswerGoodBase) :
    def get(self, request, *args, **kwargs) :
        super().remove(request, *args, **kwargs)
        question_pk = Answer.objects.get(pk=self.kwargs['pk']).question.pk
        return redirect('question_detail', question_pk)                #その場にとどまるにはjs