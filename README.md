Django Search Categories Core
=============================

Reusable app for Django providing the core functionality for app product search categories.

Client Installation
-------------------

1. Install with pip:

 ```shell
 pip install git+https://github.com/Natoora/django-search-categories-core.git@{version}

 # Where version can be a tag, a branch, or a commit.
 ```

2. Add "search_categories_core" to your INSTALLED_APPS setting like this:

 ```python
INSTALLED_APPS = [
   'search_categories_core',
]
 ```

3. Setup WS model

- The section below the "optional" comment provides the logic so that the hierarchy stays in sequence automatically.

```python
from django.db import models
from search_categories_core.models import SearchCategoryCore
from search_categories_core.managers import SearchCategoryManager


class SearchCategory(SearchCategoryCore):
   sub_category = models.ForeignKey('products.SearchCategory', null=True, blank=True, on_delete=models.CASCADE)
   product_bases = models.ManyToManyField('products.ProductBase', blank=True)

   """
   BELOW IS OPTIONAL
   """

   objects = SearchCategoryManager()

   def save(self, *args, **kwargs):
      self.synchronised = False
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

4. Setup the model in the app backend

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

5. Setup the corresponding app model in WS to connect to it

```python
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
      managed = False
      db_table = 'search_categories_searchcategory'
```

6. Setup the sync task, passing in the relevant model classes

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
      WsProduct=WsProduct,
      WsCategory=WsSearchCategory,
      AppProduct=AppProduct,
      AppCategory=AppSearchCategory,
      image_scp_destination=get_search_category_scp_destination()
   )
   sync_service.sync()
```

---

Development
-----------

1. Clone the repo.

2. On the target project run:
    ```
    (venv) $ pip install --editable /path/to/django-search-categories-core
    ```

3. Run setup instructions as above.

---

Testing
-------

1. Install test requirements
    ```
    pip install -r requirements/requirements-testing.txt
    ```

2. Run test script:
    ```
    (venv) $ python runtests.py
    ```

---

Releasing
---------

1. Increment version number in setup.py

2. Commit and push changes.

3. Create release on GitHub with the version number.

4. The release can then be installed into Django projects like this:
    ```
    git+https://github.com/Natoora/django-search-categories-core.git@{version number}
    ```
