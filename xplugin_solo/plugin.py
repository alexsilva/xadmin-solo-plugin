import inspect

from functools import partial

from django.utils.functional import cached_property
from solo.models import SingletonModel
from xadmin.views import BaseAdminPlugin


def get_model_url(self, model, name, *args, **kwargs):
    """Redirects to the change or add screens based on the configuration
    (the changelist will no longer be used as it only has one record)"""
    if issubclass(model, self.model) and name == 'changelist':
        prefix = self.opts.label_lower.replace('.', "_")
        solo_config = getattr(self, f"__{prefix}_solo", None)
        return (self.get_model_url(model, 'change', solo_config.pk, *args, **kwargs)
                if solo_config else self.get_model_url(model, 'add', *args, **kwargs))
    else:
        return type(self).get_model_url(self, model, name, *args, **kwargs)


class SoloPlugin(BaseAdminPlugin):
    """Solo config plugin"""

    def init_request(self, *args, **kwargs):
        model = getattr(self.admin_view, 'model', None)
        return bool(inspect.isclass(model) and
                    issubclass(model, SingletonModel))

    def setup(self, *args, **kwargs):
        prefix = self.opts.label_lower.replace('.', "_")
        setattr(self.admin_view, f"__{prefix}_solo", self._solo_config)
        plugin = getattr(self.admin_view.get_model_url, 'plugin', None)
        if plugin is None or not isinstance(plugin, self) and hasattr(self.admin_view, "get_model_url"):
            self.admin_view.get_model_url = partial(get_model_url, self.admin_view)
            self.admin_view.get_model_url.plugin = self

    @cached_property
    def _solo_config(self):
        """Returns the first configuration created"""
        model = self.admin_view.model
        try:
            config = model.objects.get(pk=model.singleton_instance_id)
        except model.DoesNotExist:
            config = None
        return config

    def get_context(self, context):
        context['has_add_permission'] = self._solo_config is None
        context['has_delete_permission'] = context['show_delete'] = False
        context['show_save_and_add_another'] = False
        context['show_delete_link'] = False
        context['show_save'] = False
        return context
