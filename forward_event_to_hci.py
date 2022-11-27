# Forward event from /dev/input/event* to /dev/hci*

import evdev
from evdev.events import InputEvent, KeyEvent
from evdev import ecodes
import asyncio
from typing import List, Optional
import hid_key_code
import ctypes

INPUT_DEVICE = '/dev/input/event0'
OUTPUT_DEVICE = '/dev/hidg0'

class InputEventAggregator:

    def __init__(self, input_dev_path: str, output_dev_path: str, grab_all_events: bool=True):

        self._input_dev = evdev.InputDevice(input_dev_path)
        self._output_dev_path = output_dev_path
        self._grab_all_events = grab_all_events
        if self._grab_all_events:
            print(f"Grabbing all events from {self._input_dev}")
            self._input_dev.grab()

        self.reset_key_state()

    def __del__(self):

        if self._grab_all_events:
            print(f"Releasing device {self.input_dev}")
            self._input_dev.ungrab()


    def reset_key_state(self):

        self._mod_key_state = 0x0
        self._non_mod_key_buf = set()

    def feed_event(self, event: InputEvent):

        if event.type == ecodes.EV_KEY:
            self._feed_output_device(
                    self._get_current_hci_code(
                        evdev.util.categorize(event)))

    def _get_current_hci_code(self, event: KeyEvent) -> Optional[List]:

        if event.keystate == KeyEvent.key_hold:
            return None

        if event.keycode in hid_key_code.MODIFIER_KEYS:
            try:
                hid = hid_key_code.__getattribute__(event.keycode)
            except AttributeError:
                return None
            print(hid)

            if event.keystate == KeyEvent.key_up:
                self._mod_key_state = ctypes.c_uint8(self._mod_key_state & ~hid).value

            else: # event.keystate == KeyEvent.key_down
                self._mod_key_state = ctypes.c_uint8(self._mod_key_state | hid).value

        else: # Non-modifier keys
            try:
                hid = hid_key_code.__getattribute__(event.keycode)
            except AttributeError:
                return None

            if event.keystate == KeyEvent.key_up:
                self._non_mod_key_buf.remove(hid)

            else: #event.keystate == KeyEvent.key_down
                self._non_mod_key_buf.add(hid)

        hci_code = [0] * 8
        hci_code[0] = self._mod_key_state
        hci_code[2:2+len(self._non_mod_key_buf)] = self._non_mod_key_buf

        return hci_code


    def _feed_output_device(self, hci_code: List):
        """
        hci_code: list of len(8), definition see https://www.usb.org/sites/default/files/documents/hid1_11.pdf, page 55
        """
        if hci_code is not None:
            print(f"{hci_code[0]:b} {hci_code[1:]}")
            with open(self._output_dev_path, 'wb+') as hid_handle:
                hid_handle.write(bytearray(hci_code))
        else:
            print("None")


if __name__ == "__main__":

    aggregator = InputEventAggregator(INPUT_DEVICE, OUTPUT_DEVICE)

    async def helper(dev):
        async for ev in dev.async_read_loop():
            print(evdev.ecodes.EV[ev.type])
            print(evdev.categorize(ev))
            aggregator.feed_event(ev)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(helper(aggregator._input_dev))
