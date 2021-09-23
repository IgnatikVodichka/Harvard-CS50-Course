# This is my program I have written in python long before taking CS50. I did it for HackerRank.
# Also I used it to guide myself throug same program in C.

# n = 9
# qty_value = 1

# for i in range(n):
#     print(' '*(n-1) + '#'*dqty_value + '  ' + '#'*qty_value)
#     qty_value += 1
#     n -= 1

# So here is modified version for this Course:

desired_num = 0

qty_value = 1

while True:
    desired_height = input("Height: ")

    if desired_height.isdigit() == False:
        continue

    elif int(desired_height) > 0 and int(desired_height) < 9:
        desired_height = int(desired_height)
        break

for i in range(desired_height):
    print(' '*(desired_height-1) + '#'*qty_value + '  ' + '#'*qty_value)
    qty_value += 1
    desired_height -= 1