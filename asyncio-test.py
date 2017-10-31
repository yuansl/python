#!/usr/bin/python3

import asyncio
import datetime

async def suspend_1s(sec):
    await asyncio.sleep(sec)
    print('time: ' + str(datetime.datetime.now()))

def print_time(end_time, loop):
    print(datetime.datetime.now())
    if loop.time() + 1.0 < end_time:
        loop.call_later(1, print_time, end_time, loop)
    else:
        loop.stop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print('start time: ' + str(datetime.datetime.now()))
    loop.run_until_complete(asyncio.wait([suspend_1s(6),
                                          suspend_1s(1),
                                          suspend_1s(2),
                                          suspend_1s(9),
                                          print_hello()]))
    loop.call_later(1, print_time, loop.time()+5, loop)
    loop.run_forever()
    loop.close()
