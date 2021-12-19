from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Post, Tag, Question, Follow, Answer, Account, Child

#SignUp
class SignUpForm(UserCreationForm) :
    gender_choice = [('1','選択しない'),('2','男'),('3',"女"),('4','その他')]
    gender = forms.ChoiceField(required=False, choices=gender_choice, widget=forms.Select)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type":"date"}))
    location = forms.CharField(max_length=20, required=False)
    intro = forms.CharField(required=False)

    class Meta :
        model = User
        fields = ('email', 'password1', 'password2', 'username', 'first_name')


# Login
class LoginForm(AuthenticationForm) :
    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

# Setting
class PasswordChangeForm(PasswordChangeForm) :
    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        for field in self.fields.values() :
            field.widget.attrs['class'] = 'form-control'

# ProfileEdit
class ProfileEditForm(forms.ModelForm) :
    class Meta :
        model = Account
        fields = ('account_image', 'intro', 'location', 'birth_date', 'gender')
        gender_choice = [('1','選択しない'),('2','男'),('3',"女"),('4','その他')]
        widgets = {
            'gender': forms.Select(choices=gender_choice),
            'birth_date' : forms.DateInput(attrs={"type":"date"}),
            }


# Add Child infomations
class ChildInfomationForm(forms.ModelForm) :
    class Meta :
        model = Child
        fields = ('name', 'gender', 'birth_date')
        gender_choice = [('1','選択しない'),('2','男'),('3',"女"),('4','その他')]
        widgets = {
            'gender': forms.Select(choices=gender_choice),
            'birth_date' : forms.DateInput(attrs={"type":"date"}),
            }


# Follow
class FollowForm(forms.Form) :
    class Meta :
        model = Follow
        fields = ('woner', 'follow_target')


# Post
class PostForm(forms.ModelForm) :
    class Meta :
        model = Post
        fields = ['post_image', 'caption']
        widgets = {'caption': forms.Textarea(attrs={'placeholder':'キャプション', 'onKeyUp':'ShowLength(value);'})}

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        for field in self.fields.values() :
            field.widget.attrs['class'] = 'form-control'



# Question
class QuestionForm(forms.ModelForm) :
    class Meta :
        model = Question
        fields = [ 'title', 'question_image', 'text' ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'タイトル（必須）'}),
            'text': forms.Textarea(attrs={'placeholder':'テキスト', 'onKeyUp':'ShowLength(value);'})
            }

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        for field in self.fields.values() :
            field.widget.attrs['class'] = 'form-control'


class AnswerForm(forms.ModelForm) :
    class Meta :
        model = Answer
        fields = ['name', 'text', 'answer_image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder':'ニックネーム'}),
            'text': forms.Textarea(attrs={'rows':4}),
            }

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        for field in self.fields.values() :
            field.widget.attrs['class'] = 'form-control'
    
    #保存処理
    def save_answer(self, question_id, commit=True) :
        answer = self.save(commit=False)
        answer.question = Question.objects.get(pk=question_id)
        if commit :
            answer.save()
        return answer
