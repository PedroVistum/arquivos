#!/usr/bin/env python3

# Read from the standard input and print the result to the standard
# output.

import sys
import unicodedata as uni
import re
from collections import defaultdict, Counter
import argparse
from functools import reduce
import operator

class MissingTagError(Exception):
    def __init__(self, line):
        self.line = line

def read_record(infile):
    record = {}
    for line in infile:
        if re.match(r'\s+', line):
            continue
        
        m = re.match(r'(..)  - (.*)', line)

        if not m:
            raise MissingTagError(line)

        tag, value = m.groups()
        
        if tag == 'ER': 
            return record
        
        record[tag] = value

def norm(string):
    s = ''.join(c for c in uni.normalize('NFD', string)
                if uni.category(c) != 'Mn')
    s = re.sub(r'^[^a-z]+', '', s, flags=re.IGNORECASE)
    s = re.sub(r'[^a-z]+$', '', s, flags=re.IGNORECASE)
    s = s.replace('(', '')
    s = s.replace(')', '')
    s = s.replace(':', '')
    s = s.replace('\' ', '')
    s = s.replace('\'', '')
    s = s.replace('-', ' ')
    s = s.upper()
    return s

parser = argparse.ArgumentParser()
parser.add_argument('-k', type=int, default=0)
parser.add_argument('--sep', default='\t')
parser.add_argument('--missing', default='<não informada>')
args = parser.parse_args()

table = defaultdict(Counter)
while record := read_record(sys.stdin):
    members = {norm(value)
               for tag, value in record.items()
               if re.match('U[0-9]+', tag)
               and value}
    members |= {norm(record['AU']), norm(record['OR'])}
    for member in members:
        area = norm(record['C1'])
        if not area: area = args.missing
        table[member][area] += 1

columns = sorted(col
                 for col, c
                 in reduce(operator.add, table.values()).items()
                 if args.k <= c)

print(*['name', *columns], sep=args.sep)
for member in sorted(table):
    print(*[member, *[str(table[member][c]) for c in columns]],
          sep=args.sep)
