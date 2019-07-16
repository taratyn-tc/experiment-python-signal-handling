import asyncio
import signal
from datetime import datetime

keep_going = True


async def expensive_op():
    print(f"starting op at {datetime.utcnow()}")
    await asyncio.sleep(3)
    print(f"ending op at {datetime.utcnow()}")


def signal_handler(loop):
    print(f"got signal in loop {loop}")
    global keep_going
    keep_going = False


async def main():
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, lambda: signal_handler(loop))
    while keep_going:
        print("about to do expensive op")
        await expensive_op()
    print("exiting...")


if __name__ == "__main__":
    asyncio.run(main())
