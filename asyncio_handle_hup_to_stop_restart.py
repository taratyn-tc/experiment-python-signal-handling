import asyncio
import signal
import uuid

from asyncio import AbstractEventLoop
from datetime import datetime


class MyAIterator:
    def __init__(self):
        self.counter = 0
        self.keep_going = True
        self.id = str(uuid.uuid4())

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.keep_going:
            raise StopAsyncIteration
        print(f"starting aiter op at {datetime.utcnow()}")
        self.counter += 1
        await asyncio.sleep(3)
        print(f"finished aiter op at {datetime.utcnow()}")
        return f"from {self.id}: {self.counter}"

    def stop(self):
        self.keep_going = False


class HUPHandler:
    def __init__(self):
        self.keep_going = True
        self.aiter = MyAIterator()
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, lambda: self.sigint_handler(loop))
        loop.add_signal_handler(signal.SIGHUP, lambda: self.sighup_handler(loop))

    async def expensive_op(self):
        print(f"starting op at {datetime.utcnow()}")
        await asyncio.sleep(3),
        print(f"ending op at {datetime.utcnow()}")

    async def run(self):
        async for val in self.aiter:
            print(f"val is {val}")

    async def restart_run(self, loop: AbstractEventLoop):
        print("restarting run")
        self.aiter = MyAIterator()
        await self.run()

    def sigint_handler(self, loop: AbstractEventLoop):
        print("got sigint")
        self.aiter.stop()

        # raising an exception doesn't work as it only bubbles up into the
        # asyncio library code. I can't catch it in `main()` or in __main__.
        # raise Exception("foobar")

        # can't just call stop because that's too aggressive
        # loop.stop()

        def stop_if_only_one():
            tasks = asyncio.all_tasks(loop)
            if len(tasks) == 0:
                print("work done, stopping loop")
                loop.stop()
            else:
                print("left over work to do, check again in ~.5s.")
                loop.call_later(0.5, stop_if_only_one)

        loop.call_soon(stop_if_only_one)
        print("exiting sigint")

    def sighup_handler(self, loop: AbstractEventLoop):
        print("got sighup")
        self.aiter.stop()
        loop.create_task(self.restart_run(loop))
        print("done processing_sighup")


async def main():
    handler = HUPHandler()
    loop = asyncio.get_running_loop()
    loop.create_task(handler.run())
    print("exiting main")


if __name__ == "__main__":
    main_loop = asyncio.get_event_loop()
    main_loop.create_task(main())
    main_loop.run_forever()
    print("end of script file.")
