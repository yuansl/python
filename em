#!/usr/bin/python3

import asyncio
import os

async def __make_process(progname, argv):
    pid = os.fork()
    if (pid == 0):
        os.execvp(progname, argv)
        os.exit(1)              # should never get here
    else:
        return pid
    
async def wait_emacs_server(emacs_socket_name):
    timeout = 0
    while not os.path.exists(emacs_socket_name):
        timeout += 0.1
        await asyncio.sleep(timeout)

async def start_emacs():
    emacs_socket='/tmp/emacs'+str(os.getuid())+'/server'
    if not os.path.exists(emacs_socket):
        # start emacs server
        await __make_process('emacs', ['emacs'])
    import sys
    # start emacsclient
    if (len(sys.argv) > 1):
        await wait_emacs_server(emacs_socket)
        argv = sys.argv
        argv[0] = 'emacsclient'
        argv.insert(1, '-n')
        argv.insert(2, '--socket-name')
        argv.insert(3, emacs_socket)
        await __make_process('emacsclient', argv)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_emacs())
    loop.close()
