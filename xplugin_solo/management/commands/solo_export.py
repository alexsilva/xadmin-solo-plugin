# coding=utf-8
import argparse

from django.apps import apps
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.core.management import BaseCommand
from solo.models import SingletonModel


class Command(BaseCommand):
    """Export site configuration"""

    def add_arguments(self, parser):
        parser.add_argument('--app-model', type=str, required=True,
                            help="app name plus model name like app.model")
        parser.add_argument('--filepath', type=argparse.FileType('w'),
                            required=False, default=None,
                            help='export to this filepath')
        parser.add_argument('--format', type=str, required=False,
                            help="serialize format", choices=['json', 'xml'],
                            default='json')

    def handle(self, *args, **options):
        app_model = options['app_model']
        srl_format = options['format']
        filepath = options['filepath']

        model = apps.get_model(*app_model.split('.'))
        opts = model._meta

        if not issubclass(model, SingletonModel):
            raise ImproperlyConfigured(f'Model "{opts.app_label}.{opts.model_name}" '
                                       f'does not inherit from the model "solo.SingletonModel"')

        data = serializers.serialize(srl_format, [model.get_solo()])

        if filepath is None:
            self.stdout.write(data)
        else:
            filepath.write(data)
            filepath.close()
