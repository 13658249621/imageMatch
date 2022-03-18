from django.urls import path, include

from . import view

urlpatterns = [
    path('/', view.hello),
    path('hello/', view.hello),
    path('upfiles/', include('upfile.urls')),
]
'''
path() 函数:
path(route, view, kwargs=None, name=None)
   1. route: 字符串，表示 URL 规则，与之匹配的 URL 会执行对应的第二个参数 view。
   2. view: 用于执行与正则表达式匹配的 URL 请求。
   3. kwargs: 视图使用的字典类型的参数。
   4. name: 用来反向获取 URL。
'''
