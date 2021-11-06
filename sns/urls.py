from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name="post_list"),
    path('<int:pk>', views.PostDetail.as_view(), name="detail"),
    path('<int:pk>/update/', views.PostUpdate.as_view(), name="update"),
    path('create/', views.PostCreate.as_view(), name="create"),
    path('<int:pk>/delete/', views.PostDelete.as_view(), name="delete"),
]