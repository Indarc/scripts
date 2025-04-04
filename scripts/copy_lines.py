#!/usr/bin/env python

import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='Replaces 1 line with the entered quantity')
    parser.add_argument('-c', '--copy', type=int, default=0, required=True, help='Number of repetitions')
    parser.add_argument('input_file', type=str, help='Input file path')
    parser.add_argument('output_file', default='result_copied.txt', type=str, help='Path to output file')

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f'Incorrect file path [{args.input_file}]')
        exit(0)

    with open(args.input_file, 'r') as file:
        lines = file.readlines()

    with open(args.output_file, 'w') as file:
        for line in lines:
            for i in range(args.copy):
                file.write(line)


if __name__ == "__main__":
    main()