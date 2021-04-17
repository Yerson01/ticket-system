from django.test.testcases import TestCase


class FactoryTestMixin(object):
    factory_class = None
    model_class = None

    def setUp(self):
        assert self.factory_class is not None
        assert self.model_class is not None

    def test_create_new_object_is_successful(self):
        obj = self.factory_class()
        assert isinstance(obj, self.model_class)
        assert obj.pk

    def test_generate_new_instance_is_successful(self):
        instance = self.factory_class.build()
        assert isinstance(instance, self.model_class)
        assert not instance.pk

    def test_build_dictionary_is_successful(self):
        assert hasattr(self.factory_class, 'build_dict')
        data = self.factory_class.build_dict()
        assert isinstance(data, dict)
