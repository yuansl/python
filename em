#!/usr/bin/python3

import asyncio
import os
import sys
import datetime

async def start_process(progname, argv):
    pid = os.fork()
    if (pid == 0):
        os.execvp(progname, argv)
        os.exit(1)              # should never get here
    else:
        return pid
    
async def async_emacsclient():
    emacs_socket='/tmp/emacs'+str(os.getuid())+'/server'
    if not os.path.exists(emacs_socket):
        argv = ['emacs']
        await start_process('emacs', argv)
        await asyncio.sleep(0.6)
        
    if (len(sys.argv) > 1):
        argv = sys.argv
        argv[0] = 'emacsclient'
        argv.insert(1, '-n')
        argv.insert(2, '--socket-name')
        argv.insert(3, emacs_socket)
        await start_process('emacsclient', argv)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_emacsclient())
    loop.close()
