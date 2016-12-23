from processor import Processor
import sys
import struct


def main(file):
    processor = Processor()
    index = 0

    with open(file, "rb") as f:
        hword = f.read(2)
        while len(hword) != 0:
            processor.loadProgram(index, struct.unpack("<h", hword)[0])
            index += 1
            hword = f.read(2)
    while True:
        processor.doOperation()
    print("\r")


if __name__ == '__main__':
    main(sys.argv[1])
