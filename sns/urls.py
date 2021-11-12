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
#     path('create/', views.PostCreate.as_view(), name="create"),
#     path('<int:pk>/delete/', views.PostDelete.as_view(), name="delete"),
#     path('good_top/<slug:slug>', views.GoodTop.as_view(), name='good_top'),
#     path('good_detail/<slug:slug>', views.GoodDetail.as_view(), name='good_detail'),
#     path('follow_userpage/<username>', views.FollowPage.as_view(), name='follow_userpage'),
#     path('follow_detail/<slug:slug>, views.FollowDetail.as_vies(), name='follow_detail'),
# ]