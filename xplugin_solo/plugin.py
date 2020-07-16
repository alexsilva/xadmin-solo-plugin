import inspect

from solo.models import SingletonModel
from xadmin.views import BaseAdminPlugin


class SoloPlugin(BaseAdminPlugin):
    """Solo config plugin"""

    def init_request(self, *args, **kwargs):
        model = getattr(self.admin_view, 'model', None)
        return bool(inspect.isclass(model) and
                    issubclass(model, SingletonModel))

    def _get_config(self):
        model = self.admin_view.model
        try:
            config = model.objects.get()
        except model.DoesNotExist:
            config = None
        return config

    def get_context(self, context):
        context['has_add_permission'] = self._get_config() is None
        context['has_delete_permission'] = False
        context['show_save_and_add_another'] = False
        context['show_delete_link'] = False
        return context
