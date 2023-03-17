#!/usr/bin/env python
import sys
import zipfile

buttons = [
    0x040,
    0x080,
    0x020,
    0x010,
    0x008,
    0x004,
    0x002,
    0x001,
    0x200,
    0x100,
]

def compress(inputs):
    prev = None
    count = -1
    res = []
    for input in inputs:
        if input == prev and count < 64:
            count += 1
        else:
            if prev is not None:
                res.append(prev | (count-1)<<10)
            prev = input
            count = 1
    return res

def main():
    movie_file = zipfile.ZipFile(sys.argv[1], 'r')
    movie_data = movie_file.read('Input Log.txt').decode()
    movie_data = movie_data.splitlines()
    inputs = []
    for frame in movie_data:
        if frame[0] != '|':
            continue
        input = frame.split(',')[-1][:-1]
        assert len(input) == 11
        f = 0
        for i, c in enumerate(input):
            if c != '.':
                if i == 10:
                    print('power not supported')
                    exit(1)
                f |= buttons[i]
        inputs.append(f)
    old = len(inputs)
    inputs = compress(inputs)
    print(f'uncompressed: {old} inputs, {old*2} bytes')
    print(f'compressed:   {len(inputs)} inputs, {len(inputs)*2} bytes')
    print(f'compression ratio: {(len(inputs)*2)/(old*2):.3}')
    inputs = inputs[:60*60*5]
    with open('source/arm11/inputs.h', 'w') as input_file:
        print('const u16 inputs[] = {', file=input_file)
        for input in inputs:
            print(f'  {input:#06x},', file=input_file)
        print('};', file=input_file)


if __name__ == '__main__':
    main()
