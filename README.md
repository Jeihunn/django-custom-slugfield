# Django CustomSlugField

CustomSlugField is an enhanced Django field that extends the built-in `SlugField` to provide advanced slug generation capabilities. Designed to streamline the process of creating SEO-friendly and human-readable URLs, this custom field offers several key features that make it more versatile and powerful than the standard `SlugField`.

## ✨ Features

- **Automatic Slug Generation**: Generates slugs automatically based on a specified source field in the model.
- **Custom Symbol Mapping**: Allows customization of symbol mappings for slug generation, supporting various alphabets and symbols.
- **Overwrite Option**: Provides an option to overwrite the slug on each save.
- **Manual Input Control**: Supports manual input control for the slug when needed.
- **Unique Slug Generation**: Ensures each slug is unique within the model instance.

By integrating CustomSlugField, you can enhance the usability and SEO performance of your Django applications, while also simplifying the management of slugs in your models.

## 🛠️ Usage

1. Add the field to your project:
    To use the CustomSlugField class provided by the django-custom-slug-field repo, you need to add it to a file in your project. You can name this file anything you like, for example, `services/fields.py`:

    ```python
    import uuid

    from django.db import models
    from django.core import checks
    from django.core.exceptions import FieldDoesNotExist
    from django.utils.text import slugify
    from django.utils.translation import gettext_lazy as _

    class CustomSlugField(models.SlugField):
        # ... (Paste the CustomSlugField class code here)
    ```

2. Use the field in your model:

    ```python
    from django.db import models
    from services.fields import CustomSlugField 

    class MyModel(models.Model):
        title = models.CharField(max_length=255)
        slug = CustomSlugField(
            source_field="title",
            symbol_mapping="default",
            unique=True,
            editable=False,
        )
    ```

3. Setting Up in Django Admin:
    To utilize CustomSlugField in the Django admin interface, include it in your `admin.py` file for the respective app. Here’s an example of how you can register `MyModel` with the CustomSlugField in the admin interface:

    ```python
    from django.contrib import admin
    from .models import MyModel

    @admin.register(models.MyModel)
    class MyModelAdmin(admin.ModelAdmin):
        list_display = ("title", "slug")
        readonly_fields = ("slug",)
    ```

## 🔧 Additional Options

- `source_field` (*str*): The name of the model field to use as the source for slug generation. This field should be a CharField or TextField.
- `overwrite` (*bool*): If True, the slug will be regenerated and overwritten each time the model instance is saved. Defaults to False.
- `symbol_mapping` (*list, optional*): A list of tuples defining custom symbol replacements for slug generation. Each tuple should be in the form (symbol, replacement). If "default" is specified, a predefined mapping for common Azerbaijani characters will be used.
- `allow_manual` (*bool*): If True, the slug field will accept manual input. When set to True, the source_field, overwrite, and symbol_mapping options will have no effect. Defaults to False.

## 💡 Example with Symbol Mapping

```python
from django.db import models
from .fields import CustomSlugField 

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = CustomSlugField(
        source_field='name', 
        symbol_mapping=[
            ('@', 'at'), 
            ('#', 'hash'),
        ],
        unique=True, 
        editable=False
    )
```

In this example, a product with the name "**Cool Product @ #1**" will have the slug "***cool-product-at-hash1***".

## 🎥 Video Tutorial

For a detailed explanation of using CustomSlugField in your Django projects, check out my video tutorial:

[![CustomSlugField Tutorial](https://img.youtube.com/vi/YOUR_VIDEO_ID_HERE/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE)

In this video, you'll learn:

- How to integrate CustomSlugField into your Django models.
- Customization options such as symbol mapping and manual input control.
- Best practices for optimizing SEO-friendly URLs with CustomSlugField.

## 📚 Medium Article

For an extensive overview of CustomSlugField and practical usage tips, explore my Medium article:
[Creating a Custom Slug Field in Django: Implementation and Usage of CustomSlugField](https://medium.com/@jeihunpiriyev/django-da-xüsusi-slug-sahəsi-yaratmaq-customslugfield-in-tətbiqi-və-i̇stifadəsi-c2aeb3461374)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! If you find any issues or have suggestions, feel free to open an issue or submit a pull request on GitHub.
