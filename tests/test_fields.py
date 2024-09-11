from django.test import TestCase

from jsonfield_toolkit.forms.widgets import ArrayWidget


class TestArrayWidget(TestCase):
    def test_field_initialization(self):
        self.widget = ArrayWidget()

    def test_get_context(self):
        self.widget = ArrayWidget()
        self.widget.get_context("test", ["val1", "val2"], {})

    def test_value_from_datadict(self):
        self.widget = ArrayWidget()
        self.widget.value_from_datadict(
            {"attributes_key[test]": ["key1", "key2"], "attributes_value[test]": ["val1", "val2"]},
            {},
            "test",
        )

    def test_render(self):
        self.widget = ArrayWidget()
        template = self.widget.render("test", ["val1", "val2"], {})
        x = 1
