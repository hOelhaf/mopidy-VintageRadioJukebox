****************************
Mopidy-VintageRadioJukebox
****************************

!!! Still under transition from mopidy-ttsgpio to mopidy-VintageRadioJukebox !!!

Control mopidy without screen using GPIO and TTS

For example if you play "Rather Be - Clean Bandit" you will hear:

http://translate.google.com/translate_tts?tl=en&q=rather%20be%20by%20clean%20bandit

TTS changed to `Festival <http://www.cstr.ed.ac.uk/projects/festival/>`_. Install it before using TTSGPIO::

    sudo apt-get install festival

Features
========

- Led to see if it is playing
- Next/Previous track by rotary encoder
- Select playlist by GPIO
- Hear the station name (Text To Speech)
- Shutdown


Installation
============

To use this extension you need an internet conection for the tts.

Install by running::

    pip install Mopidy-VintageRadioJukebox (coming soon...)

To access the GPIO pins in the raspberry pi you have to run mopidy with sudo::
	
	sudo mopidy



Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-VintageRadioJukebox to your Mopidy configuration file::

    [ttsgpio]
    debug_gpio_simulate = false # Set true to emulate GPIO buttons with on screen buttons
    TODO:
    [pin] [playlist|navigation|volume|shutdown] [playlistName]
    
You can set the pins you would like to use. The numbers are in BCM mode. You can check `here <http://raspberrypi.stackexchange.com/a/12967>`_ to see the numbers for your board.

Controls
========

- TODO

Project resources
=================

TODO

Changelog
=========

v1.0.0
----------------------------------------

- Fork from mopidy-ttsgpio
