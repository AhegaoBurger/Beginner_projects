word = input("What are your hobbies: ")
# print(word.count('!'))
# print(word.capitalize())
# print(word.find('pr'))
hobby = word.split()

for i in range (len(hobby)):
    hobby[i] = hobby[i].capitalize()

result = ", ".join(hobby)
print(result)
