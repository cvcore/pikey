import evdev
import asyncio

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(device.path, device.name, device.phys)

device = evdev.InputDevice('/dev/input/event0')
print(device.capabilities(verbose=True))

device.grab()

async def helper(dev):
    async for ev in dev.async_read_loop():
        print(evdev.ecodes.EV[ev.type])
        print(evdev.categorize(ev))

loop = asyncio.get_event_loop()
loop.run_until_complete(helper(device))

device.ungrab()
