from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.Signup.as_view(), name="signup"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/' ,views.Logout.as_view(), name="logout"),
    path('', views.PostList.as_view(), name="post_list"),
    path('<int:pk>', views.PostDetail.as_view(), name="detail"),
    path('<int:pk>/update/', views.PostUpdate.as_view(), name="update"),
    path('create/', views.PostCreate.as_view(), name="create"),
    path('<int:pk>/delete/', views.PostDelete.as_view(), name="delete"),
]