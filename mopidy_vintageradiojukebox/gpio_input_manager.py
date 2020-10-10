import logging
import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)

class GPIOButton():

    def __init__(self, frontend, channel, callback, cb_context):

        self.frontend = frontend
        self.channel = channel
        self.callback = callback
        self.cb_context = cb_context
        
        try:
            # GPIO Mode
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(channel, GPIO.BOTH, callback=self.event_handler, bouncetime=30)

        except RuntimeError:
            logger.error("GPIOButton: Not enough permission " +
                         "to use GPIO. GPIO input will not work")

    def event_handler(self, channel):
        if GPIO.input(channel) == 1:
            self.callback(self.cb_context)

class GPIORotaryEncoder():

    def __init__(self, frontend, channelA, channelB, callback, cb_context):

        self.frontend = frontend
        self.channelA = channelA
        self.channelB = channelB
        self.callback = callback
        self.cb_context = cb_context

        self.state_A = 0
        self.state_B = 0

        try:
            # GPIO Mode
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(channelA, GPIO.IN)
            GPIO.setup(channelB, GPIO.IN)

            GPIO.add_event_detect(channelA, GPIO.RISING,
                                  callback=self.event_handler)
            self.state_A = GPIO.input(channelA)

            GPIO.add_event_detect(channelB, GPIO.RISING,
                                  callback=self.event_handler)
            self.state_B = GPIO.input(channelB)

        except RuntimeError:
            logger.error("GPIORotaryEnc: Not enough permission " +
                         "to use GPIO. GPIO input will not work")

    def event_handler(self, channel):
        # read current state of encoder
        cur_A = GPIO.input(self.channelA)
        cur_B = GPIO.input(self.channelB)

        # check state changed, ignore bouncing
        if cur_A == self.state_A and cur_B == self.state_B:
            return
        
        # save current state
        self.state_A = cur_A
        self.state_B = cur_B

        # determine turning direction
        if cur_A == cur_B:
            if channel == self.channelA:
                self.callback(self.cb_context, +1)
            else:
                self.callback(self.cb_context, -1)
        
        return
