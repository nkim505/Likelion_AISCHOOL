# I am gonna make a random box to ramdomly choose who's gonna pay the dinner for all.
# 저녁식사를 결제할 한 사람을 뽑는 랜덤박스를 만들어보았다.

import random
import time

names = ['미영', '지훈', '민지', '도윤', '상하']

while True:
    print(names)
    item = input("추가할 멤버의 이름을 입력하세요. (끝내려면 q):")
    if item == "q":
        break
    else:
        names.append(item)
print(names)

set_names = set(names)

while True:
    print(set_names)
    item = input("삭제할 멤버의 이름을 입력해주세요. (끝내려면 q):")
    if item =='q':
        break
    else:
        set_names = set_names - set([item])
print(set_names)

print(set_names, "중에서 오늘 식사를 결제할 한 사람을 고릅니다.")

for i in range(5):
    print(5-i)
    time.sleep(1)
    
final_return = random.choice(list(set_names))
print("랜덤 선택 결과는 " + final_return + "(이)가 오늘 식사를 결제하게 되었습니다. 축하 박수~~ 짝짝짝")
print("프로그램을 종료합니다.")
