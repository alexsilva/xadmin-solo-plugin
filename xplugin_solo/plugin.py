import inspect

from solo.models import SingletonModel
from xadmin.views import BaseAdminPlugin


class SoloPlugin(BaseAdminPlugin):
    """Solo config plugin"""

    def init_request(self, *args, **kwargs):
        model = getattr(self.admin_view, 'model', None)
        return bool(inspect.isclass(model) and
                    issubclass(model, SingletonModel))
