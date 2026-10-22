A = [10, 20, 30, 40, 50]

avg = sum(A) / len(A)
filtered_elements = [x for x in A if x > avg]

print(filtered_elements)
print(len(filtered_elements))