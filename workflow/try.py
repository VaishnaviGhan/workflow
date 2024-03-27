my_list = [8, [6, 1, 9], 10]

found_one = False

for item in my_list:
    if isinstance(item, list):
        for i in item:
            if i == 1:
                found_one = True
                if found_one is True:
                    iDX = my_list.index(item)
                    print(iDX)
                    if iDX == len(my_list)-1:
                     next_ele = my_list[iDX]
                     print('mocambo in sublist and and that sublist is at last index of main list',next_ele)
                    else:
                        next_ele = my_list[iDX+1]
                        print('mocambo is in inbetween sublist and next element is = ',next_ele)
                    #==if next_ele is list
                    #--code here
                break  # Exit the loop once 1 is found in the nested list
    elif item == 1:
        found_one = True
        if found_one is True:
            iDX = my_list.index(item)
            if iDX == len(my_list)-1:
             next_ele = my_list[iDX]
             print('mocambo is last member and next_ele is = ',next_ele)
            else:
                next_ele = my_list[iDX+1]
                print('mocambo in between somewhere',next_ele)
        break  # Exit the loop once 1 is found in the main list

if found_one:
    print('1 is present')
else:
    next_ele = my_list[0]
    print('mocambo not present in workflow list and next _ele is ',next_ele)
    print('1 is not present')


