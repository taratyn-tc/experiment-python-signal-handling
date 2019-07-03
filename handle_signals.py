import datetime
import time


def main():
    try:
        start_loop()
    except KeyboardInterrupt as ki:
        print(f"got {str(ki)} {repr(ki)}")


def start_loop():
    while True:
        time_consuming_op()


def time_consuming_op():
    print(f"started op {datetime.datetime.utcnow()}")
    time.sleep(4)
    print(f"ended op {datetime.datetime.utcnow()}")


if __name__ == '__main__':
    main()
