from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext



__version__ = '1.0.0'

logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = 'Mopidy-VintageRadioJukebox'
    ext_name = 'VintageRadioJukebox'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        for pin in range(28):
            schema[f"bcm{pin:d}"] = config.String()
        return schema

    def setup(self, registry):

        from .frontend import VintageRadioJukebox
        registry.add('frontend', VintageRadioJukebox)
