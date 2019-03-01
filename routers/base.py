from .conf import path, re_path
from django.views import View


class Router:

    urlpatterns = []

    def path(self, route, kwargs=None, name=None):

        def decorator(view):
            if isinstance(view, View):
                view = view.as_view()
            pattern = path(route, view, kwargs, name)
            self.urlpatterns.append(pattern)
            return view

        return decorator

    def re_path(self, route, kwargs=None, name=None):

        def decorator(view):
            if isinstance(view, View):
                view = view.as_view()
            pattern = re_path(route, view, kwargs, name)
            self.urlpatterns.append(pattern)
            return view

        return decorator
