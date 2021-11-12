# from django.urls import path
# from . import views

# urlpatterns = [
#     path('signup/', views.Signup.as_view(), name="signup"),
#     path('login/', views.Login.as_view(), name="login"),
#     path('logout/' ,views.Logout.as_view(), name="logout"),
#     path('', views.Top.as_view(), name="Top"),
#     path(<username>/, views.Mypage.as_view(), name="mypage")
#     path('<slug:slug>', views.PostDetail.as_view(), name="detail"),
#     path('<int:pk>/update/', views.PostUpdate.as_view(), name="update"),
#     path('user<int:pk>/create/', views.PostCreate.as_view(), name="create"),
#     path('<int:pk>/delete/', views.PostDelete.as_view(), name="delete"),
# ]