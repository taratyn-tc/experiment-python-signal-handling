import signal
import time
from datetime import datetime

keep_going = True


def expensive_op(n: int = 0):
    print(f"starting op at {datetime.utcnow()}")
    time.sleep(n)
    print(f"ending op at {datetime.utcnow()}")


def signal_handler(signum, frame):
    print(f"got signal {signum}")
    global keep_going
    keep_going = False


def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    while keep_going:
        print("about to do expensive op")
        expensive_op(3)
    print("exiting...")


if __name__ == "__main__":
    main()
