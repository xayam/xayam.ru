import sys
import os

from builder import Builder

def main():
    name = os.path.basename(sys.argv[0][:-3])
    packer = Builder(name=name)
    packer.run()

if __name__ == '__main__':
    main()
