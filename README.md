# Django.router
提供装饰器分发路由功能

在工程urls文件下引入
```
from django.routers import path, include

urlpatterns = [
    path('', include('user.views')),
]
```
这样，在app下可以不用新建urls.py文件，直接在views.py文件里装饰器编写路由
```
from django.routers import Router
from django.http import HttpResponse
from django.views import View

router = Router()

@router.path('', name='index')
def index(request):
    return HttpResponse('index')


@router.path('login/', name='login')
class LoginView(View):
    def get(self, request):
        return HttpResponse('login')
```
