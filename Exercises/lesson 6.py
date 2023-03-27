count = 0
word = input("Write your world: ")
letter = input("Write your letter: ")
for look in word:
    if look == letter:
        count += 1

print("Count of", letter, "in word", word, "is", count)