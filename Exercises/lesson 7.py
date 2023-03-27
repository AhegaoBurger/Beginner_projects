n = int(input("Enter length: "))

user_list = []

number = 0
while number < n:
    string = "Enter element no." + str(number + 1) + ": "
    user_list.append(input(string))
    number +=1

print(user_list)
