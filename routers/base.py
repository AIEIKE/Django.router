from .conf import _path, RegexPattern, RoutePattern


class Router(object):

    urlpatterns = []

    def _path(self, route, kwargs=None, name=None, Pattern=None):
        def decorator(view):
            if hasattr(view, 'as_view'):
                pattern = _path(route, view.as_view(), kwargs, name, Pattern)
            else:
                pattern = _path(route, view, kwargs, name, Pattern)
            self.urlpatterns.append(pattern)
            return view
        return decorator

    def path(self, route, kwargs=None, name=None):
        return self._path(route, kwargs, name, RoutePattern)

    def re_path(self, route, kwargs=None, name=None):
        return self._path(route, kwargs, name, RegexPattern)

    
