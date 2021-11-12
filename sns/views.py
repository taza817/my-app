# from django.shortcuts import render, redirect
# # from django.contrib.auth.models import User
# # from django.contrib.auth import login, authenticate
# from .forms import LoginForm, SignupForm, PostForm
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.views import LoginView, LogoutView
# from .models import Post
# from django.views import generic
# from .mixins import OnlyYouMixin
# from django.urls import reverse, reverse_lazy

# # Create your views here.

# # TopPage
# class TopView(generic.TemplateView) :
#     template_name = 'sns/top.html'

# # SignupPage
# class Signup(generic.CreateView) :
#     template_name = 'sns/signup_form.html'
#     form_class = SignupForm
    
#     def form_valid(self, form) :
#         user = form.save()    #formの情報を保存
#         return redirect('/')
    
#     # データ送信
#     def get_context_data(self, **kwargs) :
#         context = super().get_context_data(**kwargs)
#         context["process_name"] = "サインアップ"
#         return context


# # #CreateAccount
# # class Signup(generic.CreateView) :
# #     def post(self, request, *args, **kwargs) :
# #         form = SignupForm(data=request.POST)     #mothod=POSTのデータをフォームに保存
# #         if form.is_valid() :
# #             #受け取ったデータをDBに保存
# #             form.save()
# #             #フォームから値を取得し，データ型に応じて整形
# #             email = form.cleaned_data.get('email')
# #             password = form.cleaned_data.get('password1')
# #             username = form.cleaned_data.get('username')
# #             first_name = form.cleaned_data.get('first_name')
# #             #ユーザー認証
# #             user = authenticate(username=username, password=password)
# #             #ログイン
# #             login(request, user)
# #             return redirect('/login/')   #成功後のurl
# #         return render(request, 'sns/signup_form.html', {'form': form})
    
# #     def get(self, request, *args, **kwargs) :
# #         form = SignupForm(request.POST)     #フォームを作成
# #         return render(request, 'sns/signup_form.html', {'form': form})     #テンプレートに描画


# # LoginPage
# class Login(LoginView) :
#     form_class = LoginForm
#     template_name = 'sns/login.html'

# class Logout(LogoutView) :
#     template_name = 'sns/logout_done.html'


# # #Login
# # class Login(generic.View) :
# #     def post(self, request, *args, **kwargs) :
# #         form = LoginForm(data=request.POST)
# #         if form.is_valid() :
# #             username = form.cleaned_data.get('username')
# #             user = User.objects.get(username=username)
# #             login(request, user)
# #             return redirect('/')
# #         return render(request, 'sns/login.html', {'form': form})
    
# #     def get(self, request, *args, **kwargs) :
# #         form = LoginForm(request.POST)
# #         return render(request, 'sns/login.html', {'form': form})


# # @login_required 


# # Top タイムラインとしてフォローしているユーザーの投稿を表示したい
# class Top(generic.ListView) :
#     queryset = Post.objects.filter(user_followers=user)   #フォローしてるユーザーのアイテム一覧取得
#     template_name = 'sns/top.html'
#     paginate_by = 10


# #マイページに表示する自分の投稿リスト
# class Mypage(generic.ListView) :
#     queryset = Post.objects.filter(user=self.request.user)  #自分の投稿だけ
#     template_name = 'sns/mypage.html'


# class PostCreate(OnlyYouMixin, generic.CreateView) :
#     #template_name = 'sns/post_form.html'
#     form_class = PostForm

#     def form_valid(self, form) :
#         self.instance.user = self.request.user     #現在ログインしているユーザーを代入
#         return super().form.valid(form)
      
#     def get_success_url(self) :
#         return resolve_url('Top')


# class PostDetail(generic.DetailView) :
#     model = Post




# class PostUpdate(generic.UpdateView) :
#     template_name = 'sns/post_update_form.html'
#     model = Post
#     fields = ['caption']

#     def get_success_url(self) :
#         return reverse('detail', kwargs={'pk': self.object.pk})

# class PostDelete(generic.DeleteView) :
#     model = Post
#     success_url = reverse_lazy('Top')

