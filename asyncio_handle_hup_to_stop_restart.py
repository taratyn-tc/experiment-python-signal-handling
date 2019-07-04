import asyncio
import signal

from asyncio import AbstractEventLoop
from datetime import datetime


class MyAIterator:
    def __init__(self):
        self.counter = 0
        self.keep_going = True

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.keep_going:
            raise StopAsyncIteration
        print(f"starting aiter op at {datetime.utcnow()}")
        self.counter += 1
        await asyncio.sleep(3)
        print(f"finished aiter op at {datetime.utcnow()}")
        return self.counter

    def stop(self):
        self.keep_going = False


class HUPHandler:
    def __init__(self):
        self.keep_going = True
        self.aiter = MyAIterator()
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, lambda: self.signal_handler(loop))

    async def expensive_op(self):
        print(f"starting op at {datetime.utcnow()}")
        await asyncio.sleep(3),
        print(f"ending op at {datetime.utcnow()}")

    async def run(self):
        async for val in self.aiter:
            print(f"val is {val}")

    def signal_handler(self, loop: AbstractEventLoop):
        print("got signal")
        self.aiter.stop()


async def main():
    handler = HUPHandler()
    await handler.run()


if __name__ == "__main__":
    asyncio.run(main())
