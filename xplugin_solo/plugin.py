import inspect

from functools import partial

from django.utils.functional import cached_property
from solo.models import SingletonModel
from xadmin.views import BaseAdminPlugin


def get_model_url(self, model, name, *args, **kwargs):
    """Redirects to the change or add screens based on the configuration
    (the changelist will no longer be used as it only has one record)"""
    if issubclass(model, self.solo_plugin.singleton_model) and name == 'changelist':
        solo_config = self.solo_plugin.get_solo_config(model)
        return (self.get_model_url(model, 'change', solo_config.pk, *args, **kwargs)
                if solo_config else self.get_model_url(model, 'add', *args, **kwargs))
    else:
        return type(self).get_model_url(self, model, name, *args, **kwargs)


class SoloUrlPlugin(BaseAdminPlugin):
    singleton_model = SingletonModel

    def setup(self, *args, **kwargs):
        plugin = getattr(self.admin_view, 'solo_plugin', None)
        if plugin is None or not isinstance(plugin, type(self)) and hasattr(self.admin_view, "get_model_url"):
            self.admin_view.get_model_url = partial(get_model_url, self.admin_view)
            self.admin_view.solo_plugin = self

    def get_solo_config(self, model: SingletonModel):
        """Returns the first configuration created"""
        try:
            config = model.objects.get(pk=model.singleton_instance_id)
        except model.DoesNotExist:
            config = None
        return config


class SoloPlugin(SoloUrlPlugin):
    """Solo config plugin"""

    def init_request(self, *args, **kwargs):
        model = getattr(self.admin_view, 'model', None)
        return bool(inspect.isclass(model) and issubclass(model, SingletonModel))

    @cached_property
    def _solo_config(self):
        return self.get_solo_config(self.model)

    def get_context(self, context):
        context['has_add_permission'] = self._solo_config is None
        context['has_delete_permission'] = context['show_delete'] = False
        context['show_save_and_add_another'] = False
        context['show_delete_link'] = False
        context['show_save'] = False
        return context
