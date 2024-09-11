import json

from django import forms
from django.forms import Widget
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils.safestring import mark_safe


class BaseFlatJSONWidget(Widget):
    """
    A widget that displays key/value pairs from JSON as a list of text input
    box pairs and back again.
    """

    template_name = "jsonfield_toolkit/widgets/attributes.html"
    row_template = "jsonfield_toolkit/widgets/{style}_attributes_row.html"
    style = "bootstrap5"

    @property
    def media(self):
        js = ["literature/js/key-value-widget.js"]
        return forms.Media(js=js)

    # Heavily modified from a code snippet by Huy Nguyen:
    # https://www.huyng.com/posts/django-custom-form-widget-for-dictionary-and-tuple-key-value-pairs
    def __init__(self, *args, **kwargs):
        """
        Supports additional kwargs: `key_attr`, `val_attr`, `sorted`.
        """
        self.key_attrs = kwargs.pop("key_attrs", {})
        self.val_attrs = kwargs.pop("val_attrs", {})
        self.sorted = sorted if kwargs.pop("sorted", True) else lambda x: x
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        if not value:
            value = "{}"

        if attrs is None:
            attrs = {}

        context = super().get_context(name, value, attrs)

        context["content"] = ""

        # value = ast.literal_eval(value)
        if value and isinstance(value, dict) and len(value) > 0:
            for key in self.sorted(value):
                context["content"] += render_to_string(
                    self.row_template.format(style=self.style),
                    context={
                        "key": escape(key),
                        "value": escape(value[key]),
                        "field_name": name,
                        "key_attrs": flatatt(self.key_attrs),
                        "val_attrs": flatatt(self.val_attrs),
                    },
                )
        context["content"] = mark_safe(context["content"])
        return context

    def value_from_datadict(self, data, files, name):
        """
        Returns the dict-representation of the key-value pairs
        sent in the POST parameters

        :param data: (dict) request.POST or request.GET parameters.
        :param files: (list) request.FILES
        :param name: (str) the name of the field associated with this widget.
        """
        key_field = f"attributes_key[{name}]"
        val_field = f"attributes_value[{name}]"
        if key_field in data and val_field in data:
            keys = data.getlist(key_field)
            values = data.getlist(val_field)
            return dict([item for item in zip(keys, values) if item[0] != ""])
        return {}

    def value_omitted_from_data(self, data, files, name):
        return False


class FlatJSONWidget(BaseFlatJSONWidget):
    template_name = "jsonfield_toolkit/widgets/attributes.html"
    row_template = "jsonfield_toolkit/widgets/{style}_attributes_row.html"
    style = "bootstrap5"

    @property
    def media(self):
        js = ["literature/js/key-value-widget.js"]
        return forms.Media(js=js)

    # Heavily modified from a code snippet by Huy Nguyen:
    # https://www.huyng.com/posts/django-custom-form-widget-for-dictionary-and-tuple-key-value-pairs
    def __init__(self, *args, **kwargs):
        """
        Supports additional kwargs: `key_attr`, `val_attr`, `sorted`.
        """
        self.key_attrs = kwargs.pop("key_attrs", {})
        self.val_attrs = kwargs.pop("val_attrs", {})
        self.sorted = sorted if kwargs.pop("sorted", True) else lambda x: x
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        if not value:
            value = "{}"

        if attrs is None:
            attrs = {}

        context = super().get_context(name, value, attrs)

        context["content"] = ""

        # value = ast.literal_eval(value)
        if value and isinstance(value, dict) and len(value) > 0:
            for key in self.sorted(value):
                context["content"] += render_to_string(
                    self.row_template.format(style=self.style),
                    context={
                        "key": escape(key),
                        "value": escape(value[key]),
                        "field_name": name,
                        "key_attrs": flatatt(self.key_attrs),
                        "val_attrs": flatatt(self.val_attrs),
                    },
                )
        context["content"] = mark_safe(context["content"])
        return context

    def value_from_datadict(self, data, files, name):
        """
        Returns the dict-representation of the key-value pairs
        sent in the POST parameters

        :param data: (dict) request.POST or request.GET parameters.
        :param files: (list) request.FILES
        :param name: (str) the name of the field associated with this widget.
        """
        key_field = f"attributes_key[{name}]"
        val_field = f"attributes_value[{name}]"
        if key_field in data and val_field in data:
            keys = data.getlist(key_field)
            values = data.getlist(val_field)
            return dict([item for item in zip(keys, values) if item[0] != ""])
        return {}

    def value_omitted_from_data(self, data, files, name):
        return False


class ArrayWidget(Widget):
    template_name = "jsonfield_toolkit/widgets/array_field.html"
    base_widget: Widget = None

    @property
    def media(self):
        js = ["jsonfield_toolkit/js/array-widget.js"]
        return forms.Media(js=js)

    def __init__(self, base_widget=None, *args, **kwargs):
        self.base_widget = base_widget or forms.TextInput
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        value = json.loads(value) if isinstance(value, str) else value

        if not value:
            value = []

        context["hidden_widget"] = self.base_widget().render(name, value)
        bound_widgets = []
        for i, item in enumerate(value):
            item_name = f"{name}_{i}"
            bound_widgets.append(self.base_widget().render(item_name, item))
        context["bound_widgets"] = bound_widgets
        return context

    # def render(self, name, value, attrs=None, renderer=None):
    #     context = self.get_context(name, value, attrs)
    #     return mark_safe(render_to_string(self.template_name, context))

    def value_from_datadict(self, data, files, name):
        """
        Returns the dict-representation of the key-value pairs
        sent in the POST parameters

        :param data: (dict) request.POST or request.GET parameters.
        :param files: (list) request.FILES
        :param name: (str) the name of the field associated with this widget.
        """
        row = f"attributes_value[{name}]"
        if key_field in data and val_field in data:
            keys = data.getlist(key_field)
            values = data.getlist(val_field)
            return dict([item for item in zip(keys, values) if item[0] != ""])
        return {}

    def value_omitted_from_data(self, data, files, name):
        return False


class DynamicArrayWidget(Widget):
    template_name = "django_better_admin_arrayfield/forms/widgets/dynamic_array.html"

    @property
    def media(self):
        js = ("js/django_better_admin_arrayfield.min.js",)
        css = {"all": ("css/django_better_admin_arrayfield.min.css",)}
        return forms.Media(js=js, css=css)

    def __init__(self, *args, **kwargs):
        self.subwidget_form = kwargs.pop("subwidget_form", forms.URLInput)
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        value = json.loads(value) if isinstance(value, str) else value

        context_value = value or [""]
        context = super().get_context(name, context_value, attrs)
        final_attrs = context["widget"]["attrs"]
        id_ = context["widget"]["attrs"].get("id")
        context["widget"]["is_none"] = value is None

        subwidgets = []
        for index, item in enumerate(context["widget"]["value"]):
            widget_attrs = final_attrs.copy()
            if id_:
                widget_attrs["id"] = f"{id_}_{index}"
            widget = self.subwidget_form()
            widget.is_required = self.is_required
            subwidgets.append(widget.get_context(name, item, widget_attrs)["widget"])

        context["widget"]["subwidgets"] = subwidgets
        return context

    def value_from_datadict(self, data, files, name):
        try:
            getter = data.getlist
            return [value for value in getter(name) if value]
        except AttributeError:
            return data.get(name)

    def value_omitted_from_data(self, data, files, name):
        return False

    def format_value(self, value):
        return value or []
