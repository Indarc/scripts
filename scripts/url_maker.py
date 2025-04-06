#!/usr/bin/env python

import argparse
import os
import re


def main():
    parser = argparse.ArgumentParser(description='Create URLs /path/to/complite --> http://example.com/path/to/complite')
    parser.add_argument('-i', '--input', default=None, type=str, required=False, help='Input (/path/to/complite)')
    parser.add_argument('-if', '--file', type=str, required=False, help='Path to file with url-paths')
    parser.add_argument('-s', '--secure', action='store_true', help='Return https://...')
    parser.add_argument('domain', type=str, help='Domain')
    parser.add_argument('-o', '--output', type=str, default=None , required=False, help='Output file')

    args = parser.parse_args()

    protocol = 'https://' if args.secure else 'http://'
    raw_domain = args.domain
    correct_domain = re.sub(r'^[^.]*\.', '', raw_domain)
    correct_domain = re.sub(r'[\[\]\{\}*$&%#@!\"\']', '', correct_domain)

    if args.input:
        raw_input = args.input
        if raw_input[0] != '/':
            correct_input = '/' + raw_input
        print(f'{protocol}{correct_domain}{correct_input}')
    elif args.file:
        if not os.path.exists(args.file):
            print(f'Incorrect file path [{args.file}]')
            exit(0)
        
        with open(args.file, 'r') as file:
            raw_lines = file.readlines()

        buffer = []

        for line in raw_lines:
            match = re.match(r'^([^\[]+)', line)
            url = f"{protocol}{correct_domain}{match}"
            buffer.append(url)
            print(url)
        
        if args.output:
            if not os.path.exists(args.output):
                mode = 'w'
            else:
                mode = 'a'
            
            with open(args.output, mode=mode) as file:
                for line in buffer:
                    file.write(line)
                print(f'Result saved in {args.output}')


if __name__ == "__main__":
    main()