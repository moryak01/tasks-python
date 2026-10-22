strings = ["яблоко", "кот", "банан", "он", "телевизор"]

longest = max(strings, key=len)
shortest = min(strings, key=len)

print(longest, len(longest))
print(shortest, len(shortest))