#!/usr/bin/python3

import sys

def main(argc, argv):
    print('good boy', argc, argv[0])
    if argc != 1:
        print('Usage: ')
        sys.exit(1)

if __name__ == '__main__':
    main(3, ['hello'])
