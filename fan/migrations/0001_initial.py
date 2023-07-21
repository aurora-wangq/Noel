# Generated by Django 4.2.1 on 2023-07-21 06:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nike_name', models.CharField(blank=True, default='', max_length=23, verbose_name='昵称')),
                ('desc', models.TextField(blank=True, default='', max_length=100, null=True, verbose_name='个人简介')),
                ('sign', models.CharField(blank=True, default='', max_length=25, null=True, verbose_name='个性签名')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('address', models.CharField(blank=True, default='', max_length=100, verbose_name='地址')),
                ('title', models.CharField(blank=True, default='善良的网友', max_length=100, verbose_name='头衔')),
                ('img', models.ImageField(blank=True, default='/default/txdefault.jpg', upload_to='profile_images', verbose_name='头像')),
                ('back_img', models.ImageField(blank=True, default='/default/backimg.jpg', null=True, upload_to='user_page_backimg', verbose_name='个人主页背景')),
                ('title_level', models.IntegerField(default=4, verbose_name='头衔类别,1站主,2管理员,3特殊,4普通')),
                ('notice', models.TextField(blank=True, default='', max_length=1000, null=True, verbose_name='发布公告')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('post_content', models.CharField(blank=True, max_length=10000, verbose_name='帖子内容')),
                ('post_img1', models.ImageField(blank=True, null=True, upload_to='post_images', verbose_name='帖子图片1')),
                ('show_view', models.BooleanField(default=False, verbose_name='预览图是否模糊')),
                ('pinned', models.BooleanField(default=False, verbose_name='是否顶置')),
                ('owner_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fan.userprofile')),
                ('post_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='文章作者', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NovelTraveler',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, max_length=999, verbose_name='小说标题')),
                ('content', models.TextField(blank=True, max_length=99999999, verbose_name='小说内容')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('notice', models.TextField(blank=True, max_length=300, verbose_name='公告内容')),
                ('creater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='公告发布者', to='fan.userprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='公告拥有者', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fan.post', verbose_name='赞所属文章')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='点赞者')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=500, null=True, verbose_name='评论内容')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fan.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fan.userprofile')),
            ],
        ),
    ]
