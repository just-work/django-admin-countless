Django-admin-countless
======================

Django-Admin-Countless provides a mixin for Django admin to eliminate count 
queries.

[![Build Status](https://travis-ci.org/just-work/django-admin-countless.svg?branch=master)](https://travis-ci.org/just-work/django-admin-countless)
[![codecov](https://codecov.io/gh/just-work/django-admin-countless/branch/master/graph/badge.svg)](https://codecov.io/gh/just-work/django-admin-countless)
[![PyPI version](https://badge.fury.io/py/django-admin-countless.svg)](https://badge.fury.io/py/django-admin-countless)

Installation
------------

```shell script
pip install django-admin-countless
```

Usage
-----

Full example located at `testproject.testapp.admin`

```python
from django.contrib import admin

from countless_admin import CountlessAdminMixin
from test_project.test_app.models import MyModel


@admin.register(MyModel)
class MyModelAdmin(CountlessAdminMixin, admin.ModelAdmin):
    pass
```

