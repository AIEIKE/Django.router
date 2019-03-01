from django.urls import URLResolver as _URLResolver
from django.utils.functional import cached_property
from django.core.exceptions import ImproperlyConfigured


class URLResolver(_URLResolver):

    @cached_property
    def url_patterns(self):
        router = getattr(self.urlconf_module, "router", None)
        if hasattr(router, 'urlpatterns'):
            patterns = router.urlpatterns
        else:
            patterns = getattr(self.urlconf_module,
                               "urlpatterns", self.urlconf_module)
        try:
            iter(patterns)
        except TypeError:
            msg = (
                "The included URLconf '{name}' does not appear to have any "
                "patterns in it. If you see valid patterns in the file then "
                "the issue is probably caused by a circular import."
            )
            raise ImproperlyConfigured(msg.format(name=self.urlconf_name))
        return patterns
