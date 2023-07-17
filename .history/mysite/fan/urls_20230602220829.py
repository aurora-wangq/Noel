from django.urls import path
from . import views

app_name = 'fan'   # 定义一个命名空间，用来区分不同应用之间的链接地址
urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.home_view, name='home'),
    path('register/',views.register_view, name='register'),
    path('edit/',views.editarticle_view, name='edit'),
    path('editava/',views.editavatar_view, name='editava'),
    path('post/<int:post_id>',views.post_detail_view, name='post_detail'),
]