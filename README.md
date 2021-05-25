Django Search Categories Core
=============================

Reusable app for Django providing the core functionality for app product search categories.

---

WS Installation
---------------

#### Install
 ```shell
 pip install git+https://github.com/Natoora/django-search-categories-core.git@{version}
 # Where version can be a tag, a branch, or a commit.
 ```

#### Add to INSTALLED_APPS
 ```python
INSTALLED_APPS = [
   'search_categories_core',
]
 ```

#### WS Model
```python
from django.db import models
from search_categories_core.models import SearchCategoryCore
from search_categories_core.managers import SearchCategoryManager

class SearchCategory(SearchCategoryCore):
   sub_category = models.ForeignKey('products.SearchCategory', null=True, blank=True, on_delete=models.CASCADE)
   product_bases = models.ManyToManyField('products.ProductBase', blank=True)

   objects = SearchCategoryManager()

   def save(self, *args, **kwargs):
      self.update_hierarchy(new_position=self.hierarchy)
      super().save(*args, **kwargs)

   def update_hierarchy(self, new_position: int):
      """
      Insert category at new position and update hierarchy sequence.
      """
      if not self.pk:
         return
      old_position = SearchCategory.objects.get(id=self.id).hierarchy
      SearchCategory.objects.move(obj=self, old_pos=old_position, new_pos=new_position, save=False)
```

#### WS App Model

Add the model in WS that points at the corresponding app model. e.g. ws/backend/natooraapp/models/search_category.py

```python3
from django.db import models
from search_categories_core.models import SearchCategoryCore

class SearchCategory(SearchCategoryCore):
    """
    Category of products to search.
    """
    sub_category = models.ForeignKey(
        'natooraapp.SearchCategory',
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    products = models.ManyToManyField('natooraapp.Product', blank=True)

    class Meta:
        verbose_name = "Search Category"
        verbose_name_plural = "Search Categories"
        ordering = ["hierarchy"]
        managed = False
        db_table = 'search_categories_searchcategory'
```

#### Sync Task

Import and pass the models for the app you want to sync to the search service and set the destination app name (HD or
PRO)

```python
from sidekick.decorators import sidekick_task
from products.models import (
   Product as WsProduct,
   SearchCategory as WsSearchCategory
)
from natooraapp.models import (
   Product as AppProduct,
   SearchCategory as AppSearchCategory,
)
from natooraapp.settings import get_search_category_scp_destination
from search_categories_core.services import SearchCategorySyncService

@sidekick_task
def sync_search_categories():
    """
    Run sync to create/update search categories between WS and the app.
    """
    sync_service = SearchCategorySyncService(
        WsProdModel=WsProduct,
        WsCatModel=WsSearchCategory,
        AppProdModel=AppProduct,
        AppCatModel=AppSearchCategory,
        image_destination=get_search_category_scp_destination(),
        destination_app="HD"
    )
    sync_service.sync()
```

#### Migrate DB Changes

 ```shell
./manage.py makemigrations
./manage.py migrate
 ```

#### WS admin

```python
from products.models import SearchCategory
from search_categories_core.admin import WsSearchCategoryAdmin

@admin.register(SearchCategory)
class SearchCategoryAdmin(WsSearchCategoryAdmin):
    """
    SearchCategory model admin.
    """
    pass
```

---

App Installation
----------------

#### Install

 ```shell
 pip install git+https://github.com/Natoora/django-search-categories-core.git@{version}
 # Where version can be a tag, a branch, or a commit.
 ```

#### Add to INSTALLED_APPS

 ```python
INSTALLED_APPS = [
   'search_categories_core',
]
 ```

#### App Model

```python
from django.db import models
from search_categories_core.models import SearchCategoryCore

class SearchCategory(SearchCategoryCore):
    """
    Category of products to search.
    """
    sub_category = models.ForeignKey(
        'search_categories.SearchCategory',
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    products = models.ManyToManyField('products.Product', blank=True)
```

#### Migrate DB Changes

 ```shell
./manage.py makemigrations
./manage.py migrate
 ```

#### App admin

```python
from django.contrib import admin
from search_categories_core.admin import AppSearchCategoryAdmin
from search_categories.models import SearchCategory

@admin.register(SearchCategory)
class SearchCategoryAdmin(AppSearchCategoryAdmin):
    """
    SearchCategory model admin.
    """
    pass
```

---

Development
-----------

#### Clone the repo

```shell
git clone git@github.com:Natoora/django-search-categories-core.git
```

#### Install in target project in editable mode

 ```shell
pip install --editable /path/to/django-search-categories-core
 ```

#### Follow setup instructions as above.

---

Testing
-------

#### Install test requirements

 ```shell
 pip install -r requirements-dev.txt
 ```

#### Run tests

 ```
python manage.py test
 ```

---

Releasing
---------

#### Increment version number in setup.py

#### Commit and push changes.

#### Create release on GitHub with the version number.

#### Update the core requirements files in WS and the apps

 ```shell
 git+https://github.com/Natoora/django-search-categories-core.git@{version number}
 ```
