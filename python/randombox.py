# This is written by myself applying the AI SCHOOL contents to comply with their copyright issues.
# Purpose: To make a random box to ramdomly choose who's gonna pay the dinner for all.
# 본 코드는 멋쟁이 사자처럼에서 진행하는 AI SCHOOL의 교육 내용을 응용하여 새롭게 작성되었습니다.
# 목표: 저녁식사를 결제할 한 사람을 뽑는 랜덤박스를 만들어보기.

import random
import time

names = ['Ryun', 'Apeach', 'Donald', 'Roman', 'Eden']

while True:
    print(names)
    item = input("Please input new member's name (to exit: q):")
    if item == "q":
        break
    else:
        names.append(item)
print(names)

set_names = set(names)

while True:
    print(set_names)
    item = input("Please input a name you want to delete from the list (to exit: q):")
    if item =='q':
        break
    else:
        set_names = set_names - set([item])
print(set_names)

print("The machine will choose one person among the list :", set_names)

for i in range(5):
    print(5-i)
    time.sleep(1)
    
final_return = random.choice(list(set_names))
print("The result is... " + final_return + "is chosen to pay the dinner. Clap clap clap!")
print("The applicaion closed.")
