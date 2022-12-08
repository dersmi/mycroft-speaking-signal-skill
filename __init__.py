"""
skill SpeakingSignal

Sends a signal to an Adafruit Trinket M0 using GPIO, telling 
it to animate an LED mouth.  I could have connected the LEDs
directly to the RPI GPIO but I already had the Neopixels working 
on the Trinket so this was faster.
"""
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util import LOG
import gpiod
import time

GPIO_CHIP = 'gpiochip1'
TRINKET_LINE_OFFSET = 76

chip = gpiod.chip(GPIO_CHIP)
trinket_signal_pin = chip.get_line(TRINKET_LINE_OFFSET)

config = gpiod.line_request()
config.consumer = "SpeakingSignal"
config.request_type = gpiod.line_request.DIRECTION_OUTPUT

trinket_signal_pin.request(config)

class SpeakingSignal(MycroftSkill):
    def __init__(self):
        super(SpeakingSignal, self).__init__(name="SpeakingSignal")

    def initialize(self):
        self.add_event('recognizer_loop:audio_output_start',self.handle_speech_starting)
        self.add_event('recognizer_loop:audio_output_end',self.handle_speech_finished)

    def handle_speech_starting(self, message):
        self.log.info("handle_speech_starting: Signaling Trinket to animate a mouth!")
        # based on observation, 1 sets the pin to 3.3v (low signal)?
        trinket_signal_pin.set_value(1)

    def handle_speech_finished(self, message):
        self.log.info("handle_speech_finished: Signaling Trinket to stop mouth animation.")
        trinket_signal_pin.set_value(0)   

    def stop(self):
        pass

def create_skill():
    return SpeakingSignal()