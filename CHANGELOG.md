
## 2023.7.18
优化更新个人主页、他人主页前端代码  

## 2023.7.19
微调网站前端代码，包括但不限于删除主页背景图片  
缩略图压缩width值由160修改为512，height也进行等比例缩放，在缩略图质量与体积间取得更进一步的平衡  

## 2023.7.20
死去的域名突然解析成功，现在可以通过 **[这里](http://www.aenstaraxnoel.fun/)** 访问(~~暂~~不支持海外访问)  
上传了新的网站logo并添加相关前端代码  
修复了网站logo在个人主页及他人主页显示异常的问题  
增加了帖子置顶功能(仅限站主、管理员)  

整合用户头衔为单个文件  
新建`_base.html`作为页面模板  
优化post页面体验  
添加语录功能  
优化主页布局  
点赞按钮等待响应期间禁用按钮  
点赞增加snackbar提示信息  
后端减少模板参数数量  
增加置顶提示  
增加公告  

## 2023.7.21
修复公告不分行的bug（忘了写row  
引入 FontAwesome 6 图标库  
置顶提示更改为FA图标