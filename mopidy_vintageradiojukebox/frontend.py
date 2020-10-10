import logging
import traceback
import os
import pykka
import re

from mopidy import core

from .tts import TTS
from .gpio_input_manager import GPIOButton, GPIORotaryEncoder

logger = logging.getLogger(__name__)


class VintageRadioJukebox(pykka.ThreadingActor, core.CoreListener):

    def __init__(self, config, core):
        super(VintageRadioJukebox, self).__init__()
        #self.tts = TTS()
        self.core = core
        
        config_gpios = dict((k, v) for (k, v) in config['VintageRadioJukebox'].items() if 'bcm' in k.lower())
        # get playlist mapping from config
        self.gpio_playlists = []
        config_playlists = dict((k, v) for (k, v) in config_gpios.items() if 'playlist' in v.lower())
        for k, v in config_playlists.items():
            gpio_pin = int(k.replace("bcm", ""))
            name = v.replace("playlist", "").strip()

            playlist = self._get_playlist_by_name(name)
            if playlist:
                logger.info("Register playlist " + playlist.name + " at GPIO pin " + str(gpio_pin))
                self.gpio_playlists.append(GPIOButton(self, gpio_pin, self.input_playlist, playlist))
            else:
                logger.info("Playlist " + name + " not found.")

        # get generic button mapping from config
        self.gpio_buttons = []
        config_shutdown = [(k, v) for (k, v) in config_gpios.items() if 'shutdown' in v.lower()]
        if config_shutdown:
            gpio_pin = int(config_shutdown[0][0].replace("bcm", ""))
            logger.info("Register button shutdown at GPIO pin " + str(gpio_pin))                        
            self.gpio_buttons.append(GPIOButton(self, gpio_pin, self.input_shutdown, 'shutdown')) 

        # get rotary encoder mapping from config
        self.gpio_rotaryEncs = []
        config_rotary_encoders = dict((k, v) for (k, v) in config_gpios.items() if 'rotary_encoder' in v.lower())
        rotary_encoder_names = {re.sub(r'rotary_encoder_[ABab]', "", v).strip() for (k, v) in config_rotary_encoders.items()}
        for name in rotary_encoder_names:
            r_enc = dict((k, v) for (k, v) in config_rotary_encoders.items() if name in v)
            config_rotary_A = [k for (k, v) in r_enc.items() if 'rotary_encoder_a' in v.lower()]
            config_rotary_B = [k for (k, v) in r_enc.items() if 'rotary_encoder_b' in v.lower()]
            if config_rotary_A and config_rotary_B:
                gpio_A = int(config_rotary_A[0].replace("bcm", ""))
                gpio_B = int(config_rotary_B[0].replace("bcm", ""))
                logger.info("Register rotary encoder " + name + " at GPIO pins " + str(gpio_A) + ", " + str(gpio_B))
                self.gpio_rotaryEncs.append(GPIORotaryEncoder(self, gpio_A, gpio_B, self.input_rotary_encoder, name))

    def on_start(self):
        # read all playlist gpio's to select a playlist 
        for gpio_playlist in self.gpio_playlists:
            gpio_playlist.event_handler(gpio_playlist.channel)

    def on_stop(self):
        pass
    
    def input_playlist(self, playlist):
        logger.info("Playlist " + playlist.name + " event received")
        self.core.tracklist.clear()
        tracks = self.core.playlists.get_items(playlist.uri).get()
        logger.info(tracks)
        track_uris = [track.uri for track in tracks]
        logger.info("Tracks: {0}".format(track_uris))
        self.core.tracklist.add(uris=track_uris)
        self.core.playback.play()

    def input_shutdown(self, name):
        logger.debug(name + " event received")
        if name == 'shutdown':
            #self.tts.speak_text(name)
            os.system("shutdown now -h")

    def input_rotary_encoder(self, name, value):
        logger.info(name + " event received. value="+str(value))
        if value > 0:
            self.core.playback.next()
        else:
            self.core.playback.previous()

    def _get_playlist_by_name(self, name):
        for playlist in self.core.playlists.as_list().get():
            if name.lower() == playlist.name.lower():
                return playlist
        return
