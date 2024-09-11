from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.utils import prefix_validation_error
from django.contrib.postgres.validators import ArrayMaxLengthValidator
from django.core import checks, exceptions
from django.core.validators import (
    MaxLengthValidator,
)
from django.db.models import JSONField
from django.utils.translation import ngettext_lazy

from .forms import fields


class ArrayMaxLengthValidator(MaxLengthValidator):
    message = ngettext_lazy(
        "List contains %(show_value)d item, it should contain no more than " "%(limit_value)d.",
        "List contains %(show_value)d items, it should contain no more than " "%(limit_value)d.",
        "show_value",
    )


class ArrayField(JSONField):
    def __init__(self, base_field, size=None, **kwargs):
        self.base_field = base_field
        self.db_collation = getattr(self.base_field, "db_collation", None)
        self.size = size
        if self.size:
            self.default_validators = [
                *self.default_validators,
                ArrayMaxLengthValidator(self.size),
            ]
        # For performance, only add a from_db_value() method if the base field
        # implements it.
        if hasattr(self.base_field, "from_db_value"):
            self.from_db_value = self._from_db_value
        super().__init__(**kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)

        for index, part in enumerate(value):
            try:
                self.base_field.validate(part, model_instance)
            except exceptions.ValidationError as error:
                raise prefix_validation_error(
                    error,
                    prefix=self.error_messages["item_invalid"],
                    code="item_invalid",
                    params={"nth": index + 1},
                )
        if isinstance(self.base_field, ArrayField):
            if len({len(i) for i in value}) > 1:
                raise exceptions.ValidationError(
                    self.error_messages["nested_array_mismatch"],
                    code="nested_array_mismatch",
                )

    def run_validators(self, value):
        super().run_validators(value)
        for index, part in enumerate(value):
            try:
                self.base_field.run_validators(part)
            except exceptions.ValidationError as error:
                raise prefix_validation_error(
                    error,
                    prefix=self.error_messages["item_invalid"],
                    code="item_invalid",
                    params={"nth": index + 1},
                )

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if path == "django.contrib.postgres.fields.array.ArrayField":
            path = "django.contrib.postgres.fields.ArrayField"
        kwargs.update(
            {
                "base_field": self.base_field.clone(),
                "size": self.size,
            }
        )
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "form_class": fields.ArrayField,
                "base_field": self.base_field.formfield(),
                "max_length": self.size,
                # "encoder": self.encoder,
                # "decoder": self.decoder,
                # **kwargs,
            }
        )

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        if self.base_field.remote_field:
            errors.append(
                checks.Error(
                    "Base field for array cannot be a related field.",
                    obj=self,
                    id="postgres.E002",
                )
            )
        else:
            # Remove the field name checks as they are not needed here.
            base_checks = self.base_field.check()
            if base_checks:
                error_messages = "\n    ".join(
                    "%s (%s)" % (base_check.msg, base_check.id)
                    for base_check in base_checks
                    if isinstance(base_check, checks.Error)
                )
                if error_messages:
                    errors.append(
                        checks.Error(
                            "Base field for array has errors:\n    %s" % error_messages,
                            obj=self,
                            id="postgres.E001",
                        )
                    )
                warning_messages = "\n    ".join(
                    "%s (%s)" % (base_check.msg, base_check.id)
                    for base_check in base_checks
                    if isinstance(base_check, checks.Warning)
                )
                if warning_messages:
                    errors.append(
                        checks.Warning(
                            "Base field for array has warnings:\n    %s" % warning_messages,
                            obj=self,
                            id="postgres.W004",
                        )
                    )
        return errors
