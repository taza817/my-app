from django.urls import path
from . import views
from django.conf import settings
# from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns


urlpatterns = [
    path('', views.Top.as_view(), name="top"),
    path('mypage/<int:pk>/', views.Mypage.as_view(), name="mypage"),
    path('post/<int:pk>/', views.PostDetail.as_view(), name="detail"),
    path('post/<int:pk>/update/', views.PostUpdate.as_view(), name="update"),
    path('post/create/', views.PostCreate.as_view(), name="create"),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name="delete"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('good_top/<int:pk>/', views.GoodTop.as_view(), name="good_top"),
    path('good_detail/<int:pk>/', views.GoodDetail.as_view(), name="good_detail"),
    path('follow_mypage/<int:pk>/', views.FollowMypage.as_view(), name="follow_mypage"),
]

if settings.DEBUG:
    urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)
