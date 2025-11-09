from random import randint

def create_num():
    nums=[]
    for i in range(6):
        while True:
            num=randint(1,33)
            if num not in nums:
                nums.append(num)
                break
    blue=randint(1,16)
    nums.append(blue)
    return nums
def panduan(nums,buy_nums):
    red=0
    blue=0
    for i in buy_nums[:-1]:
        if i in nums[:-1]:
            red+=1
    if buy_nums[-1]==nums[-1]:
        blue+=1

    if red==6 and blue==1:
        return 1
    elif red==6:
        return 2
    elif red==5 and blue==1:
        return 3
    elif red+blue==5:
        return 4
    elif red+ blue==4:
        return 5
    elif (red==2 and blue==1) or(red==1 and blue==1) or blue==1:
        return 6
    else:
        return 0
nums=create_num()
print('开奖号码为:',nums)
buy_nums=[12,25,16,12,26,27,11]
print('您的号码为',buy_nums)
print(f'您中了{panduan(nums,buy_nums)}等奖!!!')