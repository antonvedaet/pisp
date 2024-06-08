import sys

from translate import translate

if sys.argv[1] and sys.argv[2]:
    translate(sys.argv[1], sys.argv[2])
else:
    print("Usage: translate.py <source_file> <target_file>")

