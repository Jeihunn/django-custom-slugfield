import uuid

from django.db import models
from django.core import checks
from django.core.exceptions import FieldDoesNotExist
from django.utils.text import slugify


class CustomSlugField(models.SlugField):
    """
    Custom Django SlugField with additional features for automatic slug generation.
    """

    DEFAULT_SYMBOL_MAPPING = (
        # Azerbaijani alphabet
        ("ç", "c"),
        ("Ç", "C"),
        ("ə", "e"),
        ("Ə", "E"),
        ("ğ", "g"),
        ("Ğ", "G"),
        ("ı", "i"),
        ("İ", "I"),
        ("ö", "o"),
        ("Ö", "O"),
        ("ş", "s"),
        ("Ş", "S"),
        ("ü", "u"),
        ("Ü", "U"),
    )

    def __init__(self, source_field: str = None,  overwrite: bool = False, symbol_mapping: list = None, allow_manual: bool = False, *args, **kwargs):
        """
        Initialize the custom slug field with optional parameters.

        :param source_field: The name of the field in the model to generate
                             the slug from. This should be a string
                             representing a field name in the model.
        :param overwrite: If True, the slug will be overwritten each time the
                          model is saved. Default is False.
        :param symbol_mapping: A custom symbol mapping for slug generation.
                               If "default" is specified, the DEFAULT_SYMBOL_MAPPING
                               will be used.
        :param allow_manual: If True, manual input for the slug is allowed.
                             When this is True, source_field, overwrite, and
                             symbol_mapping settings will be ineffective.
                             Default is False.
        """
        self.source_field = source_field
        self.overwrite = overwrite
        self.symbol_mapping = self.DEFAULT_SYMBOL_MAPPING if symbol_mapping == "default" else symbol_mapping
        self.allow_manual = allow_manual
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        Generate or overwrite the slug before saving the model instance.
        """
        if (not getattr(model_instance, self.attname) or self.overwrite) and self.source_field and not self.allow_manual:
            source_value = getattr(model_instance, self.source_field)

            if self.symbol_mapping:
                # Replace symbols based on symbol mapping
                source_value = self.replace_symbols(source_value)

            slug_value = self.generate_slug(source_value, model_instance)
            setattr(model_instance, self.attname, slug_value)

        return super().pre_save(model_instance, add)

    def replace_symbols(self, source_value):
        """
        Replace symbols in the source value with corresponding replacements.
        """
        if source_value is None:
            return ""

        for symbol, replacement in self.symbol_mapping:
            source_value = source_value.replace(symbol, replacement)

        return source_value

    def generate_slug(self, source_value, model_instance):
        """
        Generate a slug from the source value or fallback to UUID if empty.
        """

        # Generate a slug from the source value using the configured allow_unicode setting
        slug_value = slugify(source_value, allow_unicode=self.allow_unicode)

        # Generate a unique slug from the source value
        if self.unique:
            unique_slug = slug_value
            counter = 1

            # Create a unique slug with a single database query
            while model_instance.__class__.objects.filter(**{self.attname: unique_slug}).exclude(pk=model_instance.pk).exists():
                unique_slug = f"{slug_value}-{counter}"
                counter += 1

            slug_value = unique_slug

        # If a valid slug is generated, return it; otherwise, fallback to a UUID
        return slug_value or slugify(str(uuid.uuid4()))

    def check(self, **kwargs):
        """
        Perform additional checks and return a list of warnings and errors.
        """
        return [
            *super().check(**kwargs),
            *self._check_allow_manual(),
            *self._check_symbol_mapping(),
            *self._check_source_field(),
        ]

    def _check_allow_manual(self):
        """
        Check if allow_manual is True and other relevant properties are set, then raise a warning.
        """
        if self.allow_manual and (self.source_field or self.overwrite or self.symbol_mapping):
            return [
                checks.Warning(
                    "allow_manual is True, so source_field, overwrite, and symbol_mapping are ineffective.",
                    obj=self,
                    id="fields.W001",
                )
            ]
        return []

    def _check_symbol_mapping(self):
        """
        Check if symbol_mapping is correctly formatted as a list of tuples with two elements each.
        """
        if self.symbol_mapping is not None:
            if not all(isinstance(item, tuple) and len(item) == 2 for item in self.symbol_mapping):
                return [
                    checks.Error(
                        "symbol_mapping should contain tuples with exactly two elements for each item.",
                        hint="Each tuple should be in the form (symbol, replacement). Example: [('ç', 'c'), ('ö', 'o'), ('@', 'at')]",
                        obj=self,
                        id="fields.E001",
                    )
                ]
        return []

    def _check_source_field(self):
        """
        Check if source_field is a valid field name in the model and is of type CharField or TextField.
        """
        if self.source_field:
            try:
                field = self.model._meta.get_field(self.source_field)
                if not isinstance(field, models.CharField) and not isinstance(field, models.TextField):
                    return [
                        checks.Error(
                            "source_field must be a CharField or TextField.",
                            obj=self,
                            id="fields.E002",
                        )
                    ]
            except FieldDoesNotExist:
                return [
                    checks.Error(
                        "source_field must be a valid field name in the model.",
                        obj=self,
                        id="fields.E003",
                    )
                ]
        return []

    def deconstruct(self):
        """
        Deconstruct the custom field into a serializable format for migrations.
        """
        name, path, args, kwargs = super().deconstruct()
        # Include custom parameters only if they are specified
        if self.source_field is not None:
            kwargs["source_field"] = self.source_field
        if self.overwrite:
            kwargs["overwrite"] = self.overwrite
        if self.symbol_mapping is not None and self.symbol_mapping != self.DEFAULT_SYMBOL_MAPPING:
            kwargs["symbol_mapping"] = self.symbol_mapping
        if self.allow_manual:
            kwargs["allow_manual"] = self.allow_manual
        return name, path, args, kwargs