int1 = 14
int2 = 55

bit_mask1 = format(int1, '032b')[::-1]
bit_mask2 = format(int2, '032b')[::-1]
print(bit_mask1)
print(bit_mask2)

bit_mask_not_eq = []
for i in range(0, len(bit_mask1), 1):
    print(i)
    if bit_mask1[i] != bit_mask2[i]:
        bit_mask_not_eq.append(i)

print(bit_mask_not_eq)
