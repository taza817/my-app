from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm

class UserCreateForm(UserCreationForm) :
    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'   #bootstrapのためのクラス
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
    
    class Meta :   #インスタンス生成時の挙動？
      model = User
      template_name = 'sns/create_account_form.html'
      fields = ("email", "password1", "password2", "username", "first_name")



class LoginForm(AuthenticationForm) :
    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'