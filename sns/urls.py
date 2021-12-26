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
    path('mypage/<int:pk>/edit/child_info/', views.AddChildInfomation.as_view(), name="add_child_infomation"),
    path('mypage/child_info/<int:pk>/delete/', views.DeleteChildInfomation.as_view(), name="delete_child_infomation"),
    path('mypage/<int:pk>/setting/', views.AccountSetting.as_view(), name="account_setting"),
    path('mypage/<int:pk>/setting/password_change/', views.PasswordChange.as_view(), name="password_change"),
    path('mypage/<int:pk>/setting/user_delete/', views.UserDelete.as_view(), name="user_delete"),
    path('post/<int:pk>/', views.PostDetail.as_view(), name="detail"),
    path('post/<int:pk>/update/', views.PostUpdate.as_view(), name="update"),
    path('post/create/', views.PostCreate.as_view(), name="create"),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name="delete"),
    path('search/post/tag/<int:pk>/', views.PostList_linking_tag.as_view(), name="postlist_linking_tag"),
    path('search/post/', views.PostSearch.as_view(), name="post_search"),
    path('search/user/', views.AccountSearch.as_view(), name="account_search"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('good_top/<int:pk>/', views.GoodTop.as_view(), name="good_top"),
    path('good_top_remove/<int:pk>/', views.GoodTop_remove.as_view(), name="good_top_remove"),
    path('good_detail/<int:pk>/', views.GoodDetail.as_view(), name="good_detail"),
    path('good_detail_remove/<int:pk>/', views.GoodDetail_remove.as_view(), name="good_detail_remove"),
    path('good_post_search/<int:pk>/', views.GoodPostSearch.as_view(), name="good_post_search"),
    path('good_post_search_remove/<int:pk>/', views.GoodPostSearch_remove.as_view(), name="good_post_search_remove"),
    # path('good_post_linkingtag/<int:pk>/', views.GoodPost_linkingtag.as_view(), name="good_post_linkingtag"),
    # path('good_post_linkingtag_remove/<int:pk>/', views.GoodPost_linkingtag_remove.as_view(), name="good_post_linkingtag_remove"),
    path('follow/<int:pk>/', views.follow, name="follow"),
    path('unfollow/<int:pk>/', views.unfollow, name="unfollow"),
    path('soudan/', views.QuestionTop.as_view(), name="question_top"),
    path('soudan/tag/<int:pk>/', views.QuestionList_linking_tag.as_view(), name="questionlist_linking_tag"),
    path('soudan/mypost/<int:pk>/', views.MyQuestion.as_view(), name="my_question"),
    path('soudan/create/', views.QuestionCreate.as_view(), name="question_create"),
    path('soudan/<int:pk>/', views.QuestionDetail.as_view(), name="question_detail"),
    path('soudan/<int:pk>/update/', views.QuestionUpdate.as_view(), name="question_update"),
    path('soudan/<int:pk>/delete/', views.QuestionDelete.as_view(), name="question_delete"),
    path('good_soudan/<int:pk>/', views.QuestionGood.as_view(), name="question_good"),
    path('good_soudan_remove/<int:pk>/', views.QuestionGood_remove.as_view(), name="question_good_remove"),
    path('soudan/answer/<int:pk>/update/', views.AnswerUpdate.as_view(), name="answer_update"),
    path('soudan/answer/<int:pk>/delete/', views.AnswerDelete.as_view(), name="answer_delete"),
    path('good_answer/<int:pk>/', views.AnswerGood.as_view(), name="answer_good"),
    path('good_answer_remove/<int:pk>/', views.AnswerGood_remove.as_view(), name="answer_good_remove"),
]

if settings.DEBUG:
    urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)
