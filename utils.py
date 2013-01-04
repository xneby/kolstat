from django.core.urlresolvers import reverse
from django.utils.functional import lazy

lazy_reverse = lazy(reverse, str)
