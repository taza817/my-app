from django.urls import path
from . import views
from django.conf import settings
# from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns


urlpatterns = [
    path('', views.AppTop.as_view(), name="app_top"),
    path('top/', views.Top.as_view(), name="top"),
    path('mypage/<int:pk>/', views.Mypage.as_view(), name="mypage"),
    path('mypage/<int:pk>/edit/', views.ProfileEdit.as_view(), name="profile_update"),
    path('mypage/<int:pk>/setting/', views.AccountSetting.as_view(), name="account_setting"),
    path('mypage/<int:pk>/setting/password_change/', views.PasswordChange.as_view(), name="password_change"),
    path('mypage/<int:pk>/setting/user_delete/', views.UserDelete.as_view(), name="user_delete"),
    path('post/<int:pk>/', views.PostDetail.as_view(), name="detail"),
    path('post/<int:pk>/update/', views.PostUpdate.as_view(), name="update"),
    path('post/create/', views.PostCreate.as_view(), name="create"),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name="delete"),
    path('post/search/', views.PostSearch.as_view(), name="post_search"),
    path('user_search/', views.AccountSearch.as_view(), name="account_search"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('good_top/<int:pk>/', views.GoodTop.as_view(), name="good_top"),
    path('good_detail/<int:pk>/', views.GoodDetail.as_view(), name="good_detail"),
    path('follow/<int:pk>/', views.follow, name="follow"),
    path('unfollow/<int:pk>/', views.unfollow, name="unfollow"),
    path('soudan/', views.QuestionTop.as_view(), name="q_top"),
    path('soudan/mypost/<int:pk>/', views.MyQuestion.as_view(), name="my_question"),
    path('soudan/create/', views.QuestionCreate.as_view(), name="q_create"),
    path('soudan/<int:pk>/', views.QuestionDetail.as_view(), name="q_detail"),
    path('soudan/<int:pk>/update/', views.QuestionUpdate.as_view(), name="q_update"),
    path('soudan/<int:pk>/delete/', views.QuestionDelete.as_view(), name="q_delete"),
    path('good_soudan/<int:pk>/', views.Qgood.as_view(), name="q_good"),
    path('answer/<int:pk>/update/', views.AnswerUpdate.as_view(), name="answer_update"),
    path('answer/<int:pk>/delete/', views.AnswerDelete.as_view(), name="answer_delete"),
    path('good_answer/<int:pk>/', views.Agood.as_view(), name="a_good"),
]

if settings.DEBUG:
    urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)
