import asyncio
import threading


class AsyncRunner(threading.Thread):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        super().__init__()
        self.loop = loop
        self.daemon = True
        self.start()

    @classmethod
    def create(cls):
        loop = asyncio.new_event_loop()
        return cls(loop)

    def run(self):
        self.loop.run_forever()

    def stop(self):
        self.loop.stop()

    def forward(self, func, *args, **kwargs) -> asyncio.Future:
        continue_future = asyncio.run_coroutine_threadsafe(func(*args, **kwargs), self.loop)
        return continue_future


class ThreadRunner:
    @classmethod
    def create(cls):
        return cls()

    def forward(self, func, *args, **kwargs) -> asyncio.Future:
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
