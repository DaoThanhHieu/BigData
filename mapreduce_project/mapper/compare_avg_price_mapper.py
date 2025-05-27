#!/usr/bin/env python3
import sys
import json

def process_input(tag):
    for line in sys.stdin:
        try:
            record = json.loads(line)
            price = float(record.get('price', 0))
            print(f"{tag}\t{price}\t1")
        except:
            continue

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: compare_avg_price_mapper.py <tag>", file=sys.stderr)
        sys.exit(1)
    
    tag = sys.argv[1]
    process_input(tag)
