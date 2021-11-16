from django.urls import path
from . import views


urlpatterns = [
    path('', views.Top.as_view(), name="top"),
    path('mypage/<username>/', views.Mypage.as_view(), name="mypage"),
    path('post/<int:pk>/', views.PostDetail.as_view(), name="detail"),
    path('post/<int:pk>/update/', views.PostUpdate.as_view(), name="update"),
    path('post/create/', views.PostCreate.as_view(), name="create"),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name="delete"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('follow_top/<int:pk>/', views.FollowTop.as_view(), name="follow_top"),
    path('follow_mypage/<username>/', views.FollowMypage.as_view(), name="follow_mypage"),
    path('good_top/<int:pk>', views.GoodTop.as_view(), name="good_top"),
    path('good_detail/<int:pk>', views.GoodDetail.as_view(), name="good_detail"),
]