from django import forms

# from django.contrib.postgres.fields import ArrayField
from . import widgets


class FlatJSONField(forms.JSONField):
    widget = widgets.FlatJSONWidget


class ArrayField(forms.JSONField):
    widget = widgets.DynamicArrayWidget

    def __init__(self, base_field, size=None, **kwargs):
        self.base_field = base_field
        self.size = size
        super().__init__(**kwargs)

    # def validate(self, value):
    #     super().validate(value)
    #     errors = []
    #     for index, item in enumerate(value):
    #         try:
    #             self.base_field.validate(item)
    #         except ValidationError as error:
    #             errors.append(
    #                 prefix_validation_error(
    #                     error,
    #                     prefix=self.error_messages["item_invalid"],
    #                     code="item_invalid",
    #                     params={"nth": index + 1},
    #                 )
    #             )
    #     if errors:
    #         raise ValidationError(errors)
