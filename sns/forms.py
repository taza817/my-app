from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post, Tag

#SignUp
class SignUpForm(UserCreationForm) :
    gender_choice = [('1','選択しない'),('2','男'),('3',"女"),('4','その他')]
    gender = forms.ChoiceField(required=False, label='ジェンダー', choices=gender_choice, widget=forms.Select)
    birth_date = forms.DateField(required=False, label='誕生日', widget=forms.DateInput(attrs={"type":"date"}))
    location = forms.CharField(max_length=20, required=False, label='居住地')
    intro = forms.CharField(max_length=400, required=False, label='自己紹介', widget=forms.Textarea)
    # account_image = forms.ImageField(upload_to="plofile_pics", blank=True)

    class Meta :
        model = User
        fields = ('email', 'password1', 'password2', 'username', 'first_name')


# Login
class LoginForm(AuthenticationForm) :
    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'


# Post
class PostForm(forms.ModelForm) :
    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        for field in self.fields.values() :
            field.widget.attrs['class'] = 'form-control'

    class Meta :
        model = Post
        fields = [ 'post_image', 'caption', 'post_tag']
        # exclude = ('post_tag',)