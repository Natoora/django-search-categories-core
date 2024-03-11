from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="search_categories_core",
    version="1.1.15",
    author="Ed Chapman",
    author_email="ed@natoora.com",
    description="Core functionality for the mobile app product search categories.",
    long_description=long_description,
    url="https://github.com/Natoora/django-search-categories-core",
    packages=find_packages(exclude=['tests*']),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires='>=3.6',
    install_requires=[
        "Django>=3.2",
        "djangorestframework>=3",
        "Pillow>=8.3"
    ]
)
