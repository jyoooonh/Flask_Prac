##### argparse 사용법

# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("-d", "--decimal", dest="decimal", action="store")          # extra value
# parser.add_argument("-f", "--fast", dest="fast", action="store_true")           # existence/nonexistence
# args = parser.parse_args()

# print(args.decimal)
# print(args.fast)

##### ====================================================================

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-hl", "--hello", dest="hello", action="store")
parser.add_argument("-f", "--fast", dest="fast", action="store_true")
args = parser.parse_args()

if args.hello == '1':
    print("Hello World!!!")
else:
    print("What the Hell!!")
# print(args.hello)
# print(args.fast)