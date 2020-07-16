from xadmin.sites import site as xadmin_site
from xadmin.views import UpdateAdminView, ListAdminView


def register(site=None):
    """Plugin register views"""
    if site is None:
        site = xadmin_site

    from xplugin_solo.plugin import SoloPlugin

    site.register_plugin(SoloPlugin, UpdateAdminView)
    site.register_plugin(SoloPlugin, ListAdminView)
