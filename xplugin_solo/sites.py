from xadmin.sites import site as xadmin_site
from xadmin.views import CommAdminView, UpdateAdminView, ListAdminView, CreateAdminView


def register(site=None):
    """Plugin register views"""
    if site is None:
        site = xadmin_site

    from xplugin_solo.plugin import SoloUrlPlugin, SoloPlugin

    site.register_plugin(SoloUrlPlugin, CommAdminView)
    site.register_plugin(SoloPlugin, CreateAdminView)
    site.register_plugin(SoloPlugin, UpdateAdminView)
    site.register_plugin(SoloPlugin, ListAdminView)
