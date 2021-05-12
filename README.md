Django Search Categories Core
=============================

Reusable app for Django providing the core functionality for app product search categories.

Client Installation
-------------------

1. Install with pip:

    ```
    pip install git+https://github.com/Natoora/django-search-categories-core.git@{version}

    # Where version can be a tag, a branch, or a commit.
    ```

2. Add "search_categories_core" to your INSTALLED_APPS setting like this:

    ```
    INSTALLED_APPS = [
        ...
        'search_categories_core',
    ]
    ```

Development
-----------
1. Clone the repo.

2. On the target project run:
    ```
    (venv) $ pip install --editable /path/to/django-search-categories-core
    ```

3. Run setup instructions as above.

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

Releasing
---------

1. Increment version number in setup.py

2. Commit and push changes.

3. Create release on GitHub with the version number.

4. The release can then be installed into Django projects like this:
    ```
    git+https://github.com/Natoora/django-search-categories-core.git@{version number}
    ```
