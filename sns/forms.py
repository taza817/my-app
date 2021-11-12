# from django import forms
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.contrib.auth import get_user_model   #ユーザーモデルを取得する
# from .models import Account

# User = Account.objects.get(id=1)

# ''' LoginForm '''
# class LoginForm(AuthenticationForm) :
#     def __init__(self, *args, **kwargs) :
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values() :
#             field.widget.attrs['class'] = 'form-control'
#             field.widget.attrs['placeholder'] = field.label    #placeholderにフィールドのラベルを入れる


# ''' SignupForm '''
# class SignupForm(UserCreationForm) :
        
#     class Meta :
#         model = User
#         fields = ('User.user.email', 'User.user.password1', 'User.user.password2', 'User.user.username', 'User.user.first_name', )
        
#     def __init__(self, *args, **kwargs) :
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values() :
#             field.widget.attrs['class'] = 'form-control'
#             field.widget.attrs['required'] = ''    #全項目を入力必須に


# ''' PostCreateForm '''
# class PostForm(forms.ModelForm) :
#     def __init__(self, *args, **kwargs) :
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values() :
#             field.widget.attrs['class'] = 'form-control'
        
#     class Meta :
#         model = Post
#         fields = ('caption')    #あとでファイルとタグを追加

        