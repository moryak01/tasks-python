A = [5, 10, 15, 10, 20]
D = 10

count_D = A.count(D)
first_index = A.index(D) if D in A else -1

print(count_D)
print(first_index)