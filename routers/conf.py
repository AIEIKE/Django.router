from functools import partial
from importlib import import_module
from django.core.exceptions import ImproperlyConfigured
from django.urls.resolvers import (
    LocalePrefixPattern, RegexPattern, RoutePattern, URLPattern,
)
from .resolvers import URLResolver


def include(arg, namespace=None):
    app_name = None
    if isinstance(arg, tuple):
        try:
            urlconf_module, app_name = arg
        except ValueError:
            if namespace:
                raise ImproperlyConfigured(
                    'Cannot override the namespace for a dynamic module that '
                    'provides a namespace.'
                )
            raise ImproperlyConfigured(
                'Passing a %d-tuple to include() is not supported. Pass a '
                '2-tuple containing the list of patterns and app_name, and '
                'provide the namespace argument to include() instead.' % len(arg)
            )
    else:
        urlconf_module = arg

    if isinstance(urlconf_module, str):
        urlconf_module = import_module(urlconf_module)
    module_name = urlconf_module.__name__
    if '.views' in module_name:
        if namespace is None:
            namespace = module_name.split('.')[0]
        app_name = namespace
    else:
        patterns = getattr(urlconf_module, 'urlpatterns', urlconf_module)
        app_name = getattr(urlconf_module, 'app_name', app_name)
        if namespace and not app_name:
            raise ImproperlyConfigured(
                'Specifying a namespace in include() without providing an app_name '
                'is not supported. Set the app_name attribute in the included '
                'module, or pass a 2-tuple containing the list of patterns and '
                'app_name instead.',
            )
        namespace = namespace or app_name

        if isinstance(patterns, (list, tuple)):
            for url_pattern in patterns:
                pattern = getattr(url_pattern, 'pattern', None)
                if isinstance(pattern, LocalePrefixPattern):
                    raise ImproperlyConfigured(
                        'Using i18n_patterns in an included URLconf is not allowed.'
                    )
    return (urlconf_module, app_name, namespace)


def _path(route, view, kwargs=None, name=None, Pattern=None):
    if isinstance(view, (list, tuple)):
        pattern = Pattern(route, is_endpoint=False)
        urlconf_module, app_name, namespace = view
        return URLResolver(
            pattern,
            urlconf_module,
            kwargs,
            app_name=app_name,
            namespace=namespace,
        )
    elif callable(view):
        pattern = Pattern(route, name=name, is_endpoint=True)
        return URLPattern(pattern, view, kwargs, name)
    else:
        raise TypeError(
            'view must be a callable or a list/tuple in the case of include().')


path = partial(_path, Pattern=RoutePattern)
re_path = partial(_path, Pattern=RegexPattern)
