from functools import partial
from .conf import path, re_path
from django.urls.resolvers import RegexPattern, RoutePattern


class Router:

    urlpatterns = []

    def path(self, route, kwargs=None, name=None):

        def decorator(view):
            pattern = path(route, view, kwargs, name)
            self.urlpatterns.append(pattern)
            return view

        return decorator

    def re_path(self, route, kwargs=None, name=None):

        def decorator(view):
            pattern = re_path(route, view, kwargs, name)
            self.urlpatterns.append(pattern)
            return view

        return decorator
