import logging
import traceback

import Callnumber
import pandas, openpyxl, math, csv, os
from misc_functions \
    import insert_space, has_numbers, has_invalidchars, \
    replace_alphchars, has_alphabet, replace_nums, remove_latter_half, get_latter_half
from tqdm import tqdm

# Set the Logging Configuration #
logging.basicConfig(filename="error_log.txt", filemode= 'w')
full_log = open("debug_log.txt", "w")

'''
first_classify_compare(insertClassNum, lowerClassNum):
dict insertClassNum: represents the classification number that is being inserted into the list 
dict lowerClassNum: represents the lower value classification number being compared to the inserted classificaton number

----
Function: Compares the values of the insert classification number with the lower value value classification on the list:
Step 1.) Compares the Classification Letters
Step 2.) Compares the Classification Numbers
Step 3.) Compares the Cutter Letters
Step 4.) Compares the Cutter Numbers

If in any of the steps the insertClassNum values are smaller or larger than the lowerClassNum values then it will return
True.
If all the values are equal to one another than the values are equal to one another than the values return false.
--
Returns:
Tuple (Bool, String)
Bool = True if one value is larger than the others. False if all values in dictionary are equal.
String = Which of the values is larger.

If insertClassNum > listClassNum:
return ("Insert", True)
Else if insertClassNum < listClassNum:
return ("List", True)
Else if all values have been tested and all values are equal:
return ("Neither", False)
'''
def first_classify_compare(insertClassNum, listClassNum):
    if insertClassNum.getCallNumLetter() > listClassNum.getCallNumLetter():
        # print("Insert class letter is Larger than list's")
        full_log.write("Insert class letter is Larger than list's\n")
        return (True, "Insert")
    elif insertClassNum.getCallNumLetter() < listClassNum.getCallNumLetter():
        full_log.write("List class letter is Larger than Insert's\n")
        return (True, "List")
    else:
        full_log.write("Insert and List have same Classification Letters\n")
    if insertClassNum.getCallNumNumber() > listClassNum.getCallNumNumber():
        full_log.write("Insert classnumber is larger than list\n")
        return (True, "Insert")
    elif insertClassNum.getCallNumNumber() < listClassNum.getCallNumNumber():
        full_log.write("Second classnumber is larger than insert\n")
        return (True, "List")
    else:
        full_log.write("Insert and Second classnumbers are equal.\n")
    if insertClassNum.getCallNumCutLet() > listClassNum.getCallNumCutLet():
        full_log.write("Insert cutter letter is larger than the second.\n")
        return (True, "Insert")
    elif insertClassNum.getCallNumCutLet() < listClassNum.getCallNumCutLet():
        full_log.write("Second cutter letter is larger than the first.\n")
        return (True, "List")
    else:
        full_log.write("Insert and Second cutterletters are equal.\n")
    if insertClassNum.getCallNumCutNum() > listClassNum.getCallNumCutNum():
        full_log.write("Insert cutter number is larger than the second.\n")
        return (True, "Insert")
    elif insertClassNum.getCallNumCutNum() < listClassNum.getCallNumCutNum():
        full_log.write("Second cutter number is larger than the first.\n")
        return (True, "List")
    else:
        full_log.write("Insert and second cutter numbers are equal.\n")
        return (False, "Neither")


'''
second_classify_compare(insertClassNum, listClassNum):
CallNumber insertClassNum: Classification Number Being Inserted Into the List
CallNumber listClassNum: Classification Number from the List Being Compared To the Inserted Class Number
---
Function:
Looks at the two call numbers, looks to see if they have a Second Cutter Numbers, Index, or Year Of Publication.
If they both do, then they compare the two of them and looks to see if one is larger than the other in value, or if
one has a Supplement and the other doesn't; or one has an Index while the other does not.
---
Return:
If insertClassNum > listClassNum:
return ("Insert", True)
Else if insertClassNum < listClassNum:
return ("List", True)
Else if all values have been tested and all values are equal:
return ("Neither", False)
'''
def second_classify_compare(insertClassNum, listClassNum):
    if (insertClassNum.callnum_seccutter == True and listClassNum.callnum_seccutter == True):
        if insertClassNum.getSecCallNumDict()['second cutletter'] > listClassNum.getSecCallNumDict()['second cutletter']:
            full_log.write("Insert cutter letter is Larger than list's\n")
            return (True, "Insert")
        elif insertClassNum.getSecCallNumDict()['second cutletter'] < listClassNum.getSecCallNumDict()['second cutletter']:
            full_log.write("List cutter letter is Larger than insert's\n")
            return (True, "List")
        else:
            full_log.write("Both Insert and List Cutter Letters are equal.\n")
        insrt_seccut = insertClassNum.getSecCallNumDict()["second cutnumber"]
        list_seccut = listClassNum.getSecCallNumDict()["second cutnumber"]
        if insrt_seccut > list_seccut:
            full_log.write("Insert cutter number is Larger than list's\n")
            return (True, "Insert")
        elif insrt_seccut < list_seccut:
            full_log.write("List cutter number is Larger than insert's\n")
            return (True, "List")
        else:
            full_log.write("Both Insert and List Cutter Numbers are equal.\n")
    elif insertClassNum.testCallNumIndex() == True and listClassNum.testCallNumIndex() == False:
        full_log.write("Insert classnum has an index value while List class num does not. Insert has a greater value\n")
        return (True, "Insert")
    elif insertClassNum.testCallNumIndex() == False and listClassNum.testCallNumIndex() == True:
        full_log.write("List classnum has an index num while Insert class num does not. List has a greater value\n")
        return (True, "List")
    elif insertClassNum.testCallNumSupp() == True and listClassNum.testCallNumSupp() == False:
        full_log.write("Insert classnum has a supplement value while List classnum does not. Insert has a greater value\n")
        return (True, "Insert")
    elif insertClassNum.testCallNumSupp() == False and listClassNum.testCallNumSupp() == True:
        full_log.write("List classnum has a supplement value while Insert classnum does not. List has a greater value\n")
        return (True, "List")
    if (insertClassNum.testCallNumYear() != None and listClassNum.testCallNumYear() != None):
        insrt_year = insertClassNum.testCallNumYear()
        insrt_year_num = 0
        insrt_year_alph = ""
        if "-" in insrt_year:
            if has_alphabet(insrt_year):
                insrt_year_alph = replace_nums(insrt_year)
            insrt_year_num = int(replace_alphchars(insrt_year.split('-',1)[1]))
        else:
            if has_alphabet(insrt_year):
                insrt_year_alph = replace_nums(insrt_year)
            insrt_year_num = int(replace_alphchars(insrt_year))
        list_year = listClassNum.testCallNumYear()
        list_year_num = 0
        list_year_alph = ""
        if "-" in list_year:
            if has_alphabet(list_year):
                list_year_alph = replace_nums(list_year)
            list_year_num = int(replace_alphchars(list_year.split('-',1)[1]))
        else:
            if has_alphabet(list_year):
                list_year_alph = replace_nums(list_year)
            list_year_num = int(replace_alphchars(list_year))
        if insrt_year_num > list_year_num:
            full_log.write("Insert Publication Year is larger than the List's.\n")
            return (True, "Insert")
        elif insrt_year_num < list_year_num:
            full_log.write("List Publication Year is larger than the Insert's\n")
            return (True, "List")
        else:
            full_log.write("Insert and List Publication Years are equal.\n")
            if insrt_year_alph > list_year_alph:
                full_log.write("Insert year has a larger alphabetical value.\n")
                return (True, "Insert")
            elif insrt_year_alph < list_year_alph:
                full_log.write("List year has a larger alphabetical value.\n")
                return (True, "List")
            else:
                full_log.write("Both years have the same alphabetical values.\n")
                return (False, "Neither")
            # return (False, "Neither")
    elif (insertClassNum.testCallNumYear() != None and listClassNum.testCallNumYear() == None):
        full_log.write("Insert has a publication year, while List does not, so Insert CallNum is larger\n")
        return (True, "Insert")
    elif (insertClassNum.testCallNumYear() == None and listClassNum.testCallNumYear() != None):
        full_log.write("List has a publication year, while Insert does not, so List CallNum is larger\n")
        return (True, "List")
    return (False, "Neither")


'''
description_compare(CallNumber insertClassNum, CallNumber listClassNum):
insertClassNum: ClassNumber that is being placed into the array and is being compared with the current ClassNumber from
the list.
listClassNum: ClassNumber that is from the list being compared with the insertClassNum.
---
Function:
Compares the classification number that is being inserted into the array with a classification number that has come from
the list. It will look through the different values such as the volume, part, number, etc. As well as look through the
different sub values that are inside of the initial volume, part, number, etc.

---
Return:
If the insert ClassNumber is larger than the list ClassNumber:
return (True, "Insert")
Else if the list is larger than the insert:
return (True, "List")
Else if all the values have been tested and all values are equal:
return (False, "Neither")
'''
def description_compare(insertClassNum, listClassNum):
    full_log.write("Comparing Descriptions\n")
    if (insertClassNum.testVolVolume() == True and listClassNum.testVolVolume() == True):
        full_log.write("Both have a Volume Number\n")
        insert_vol = insertClassNum.getDescriptionDict()["Volume Number"]
        insrt_vol_num = 0
        insrt_vol_alph = ""
        if insert_vol[0].isnumeric() == True:
            if "-" in insert_vol:
                if has_alphabet(insert_vol) == True:
                    insrt_vol_alph = has_invalidchars(replace_nums(insert_vol.upper()))
                split_vol = insert_vol.split("-", 1)
                if split_vol[1][0].isnumeric():
                    insrt_vol_num = int(split_vol[1])
                else:
                    insrt_vol_num = int(split_vol[0])
                # insrt_vol_num = int(remove_latter_half(insert_vol.split("-", 1)[1]))
            else:
                if has_alphabet(insert_vol) == True:
                    insrt_vol_alph = replace_nums(insert_vol.upper())
                insrt_vol_num = int(remove_latter_half(insert_vol))
        else:
            insrt_vol_alph = replace_nums(insert_vol.upper())
        list_vol = listClassNum.getDescriptionDict()["Volume Number"]
        list_vol_num = 0
        list_vol_alph = ""
        if list_vol[0].isnumeric() == True:
            if "-" in list_vol:
                if has_alphabet(list_vol) == True:
                    list_vol_alph = has_invalidchars(replace_nums(list_vol.upper()))
                split_vol = list_vol.split("-", 1)
                if split_vol[1][0].isnumeric():
                    list_vol_num = int(split_vol[1])
                else:
                    list_vol_num = int(split_vol[0])
                # list_vol_num = int(list_vol.split("-", 1)[1])
            else:
                if has_alphabet(list_vol) == True:
                    list_vol_alph = replace_nums(list_vol.upper())
                list_vol_num = int(remove_latter_half(list_vol))
        else:
            list_vol_alph = replace_nums(list_vol.upper())
        if (insrt_vol_num > list_vol_num):
            full_log.write("Insert Volume number is larger than the List's Volume number\n")
            return (True, "Insert")
        elif (insrt_vol_num < list_vol_num):
            full_log.write("List Volume number is larger than the Insert's Volume number\n")
            return (True, "List")
        else:
            full_log.write("Both have the same volume number\n")
            if (insrt_vol_alph > list_vol_alph):
                full_log.write("Insert Vol alpha is larger than List Vol Alpha\n")
                return (True, "Insert")
            elif (insrt_vol_alph < list_vol_alph):
                full_log.write("List Vol alpha is larger than Insert Vol Alpha\n")
                return (True, "List")
            else:
                full_log.write("Both have the same volume alphabet\n")
        if (insertClassNum.vol_part == True and listClassNum.vol_part == True):
            insrt_vol_part = insertClassNum.getDescriptionDict()["Volume Part"]
            insrt_vol_pt_num = 0
            insrt_vol_pt_alph = ""
            if insrt_vol_part[0].isnumeric() == True:
                if "-" in insrt_vol_part:
                    insrt_vol_pt_num = int(insrt_vol_part.split("-", 1)[1])
                elif insrt_vol_part[len(insrt_vol_part)-1].isalpha:
                    all_nums = ""
                    restOfpt = ""
                    for chara in range(len(insrt_vol_part)):
                        if insrt_vol_part[chara].isnumeric() == True:
                            all_nums += insrt_vol_part[chara]
                        else:
                            restOfpt = insrt_vol_part[chara:]
                            break
                    insrt_vol_pt_num = int(all_nums)
                    insrt_vol_pt_alph = restOfpt.upper()
                else:
                    insrt_vol_pt_num = int(insrt_vol_part)
            else:
                insrt_vol_pt_alph = replace_nums(insrt_vol_part.upper())
            list_vol_part = listClassNum.getDescriptionDict()["Volume Part"]
            lst_vol_pt_num = 0
            lst_vol_pt_alph = ""
            if insrt_vol_part[0].isnumeric() == True:
                if "-" in insrt_vol_part:
                    lst_vol_pt_num = int(insrt_vol_part.split("-", 1)[1])
                elif insrt_vol_part[len(insrt_vol_part) - 1].isalpha:
                    all_nums = ""
                    restOfpt = ""
                    for chara in range(len(list_vol_part)):
                        if list_vol_part[chara].isnumeric() == True:
                            all_nums += list_vol_part[chara]
                        else:
                            restOfpt = list_vol_part[chara:]
                            break
                    lst_vol_pt_num = int(all_nums)
                    lst_vol_pt_alph = restOfpt.upper()
            else:
                list_vol_pt_alph = replace_nums(list_vol_part.upper())
            if (insrt_vol_pt_num > lst_vol_pt_num):
                full_log.write("Insert has a larger volume part than list\n")
                return (True, "Insert")
            elif (insrt_vol_pt_num < lst_vol_pt_num):
                full_log.write("List has a larger volume part than insert\n")
                return (True, "List")
            else:
                full_log.write("Both have the same part size\n")
                if (insrt_vol_pt_alph > lst_vol_pt_alph):
                    full_log.write("Insert has a larger vol part alpha\n")
                    return (True, "Insert")
                elif (insrt_vol_pt_alph < lst_vol_pt_alph):
                    full_log.write("List has a larger vol part alpha\n")
                    return (True, "List")
                else:
                    full_log.write("Both have the same vol part alpha\n")
        if (insertClassNum.testVolIndex() == True and listClassNum.testVolIndex() == False):
            full_log.write("Insert has an index value, while list doesn't. Insert has the larger value\n")
            return (True, "Insert")
        elif (insertClassNum.testVolIndex() == False and listClassNum.testVolIndex() == True):
            full_log.write("List has an index value, while insert doesn't. List has the larger value\n")
            return (True, "List")
        if (insertClassNum.testVolSupp() == True and listClassNum.testVolSupp() == False):
            full_log.write("Insert has a supplement value, while list does not. Insert has the larger value\n")
            return (True, "Insert")
        elif (insertClassNum.testVolSupp() == False and listClassNum.testVolSupp() == True):
            full_log.write("List has a supplement value, while insert does not. List has the larger value\n")
            return (True, "List")
    if (insertClassNum.testPrtPart() == True and listClassNum.testPrtPart() == True):
        full_log.write("Both have a Part Value\n")
        insrt_part = insertClassNum.getDescriptionDict()["Part Number"]
        insrt_pt_num = 0
        insrt_pt_letter = ""
        if insrt_part[0].isnumeric() == True:
            if "-" in insrt_part:
                if has_alphabet(insrt_part) == True:
                    insrt_pt_letter = replace_nums(insrt_part.upper())
                insrt_pt_num = int(remove_latter_half(insrt_part.split("-", 1)[1]))
            else:
                if has_alphabet(insrt_part) == True:
                    insrt_pt_letter = replace_nums(insrt_part.upper())
                insrt_pt_num = int(remove_latter_half(insrt_part))
        else:
            insrt_pt_num = replace_nums(insrt_part.upper())
        list_part = listClassNum.getDescriptionDict()["Part Number"]
        list_pt_num = 0
        list_pt_letter = ""
        if list_part[0].isnumeric() == True:
            if "-" in list_part:
                if has_alphabet(list_part) == True:
                    list_pt_letter = replace_nums(list_part.upper())
                list_pt_num = int(remove_latter_half(list_part.split("-", 1)[1]))
            else:
                if has_alphabet(list_part) == True:
                    list_pt_letter = replace_nums(list_part.upper())
                list_pt_num = int(remove_latter_half(list_part))
        else:
            list_pt_num = replace_nums(list_part.upper())
        if (insrt_pt_num > list_pt_num):
            full_log.write("Insert has a larger part than List's Part\n")
            return (True, "Insert")
        elif (insrt_pt_num < list_pt_num):
            full_log.write("List has a larger part than Insert's Part\n")
            return (True, "List")
        else:
            full_log.write("Both Insert and List have the same part.\n")
            if (insrt_pt_letter > list_pt_letter):
                full_log.write("Insert has a larger letter than list.\n")
                return (True, "Insert")
            elif (insrt_pt_letter < list_pt_letter):
                full_log.write("List has a larger letter than list.\n")
                return (True, "Insert")
            else:
                full_log.write("Both Insert and List have the same letter value.\n")
        if (insertClassNum.part_hasvol == True and listClassNum.part_hasvol == True):
            insrt_pt_vol = insertClassNum.getDescriptionDict()["Part Volume"]
            in_pt_vol_num = 0
            if insrt_pt_vol[0].isnumeric() == True:
                if "-" in insrt_pt_vol:
                    in_pt_vol_num = int(insrt_pt_vol.split("-", 1)[1])
                else:
                    in_pt_vol_num = int(insrt_pt_vol)
            else:
                in_pt_vol_num = 9999999
            list_pt_vol = listClassNum.getDescriptionDict()["Part Volume"]
            list_pt_vol_num = 0
            if list_pt_vol[0].isnumeric() == True:
                if "-" in insrt_pt_vol:
                    list_pt_vol_num = int(list_pt_vol.split("-", 1)[1])
                else:
                    list_pt_vol_num = int(list_pt_vol)
            else:
                list_pt_vol_num = 9999999
            if (in_pt_vol_num > list_pt_vol_num):
                full_log.write("")
                return (True, "Insert")
            elif (in_pt_vol_num < list_pt_vol_num):
                full_log.write("")
                return (True, "List")
            if (insertClassNum.testPrtSupp() == True and listClassNum.testPrtSupp() == False):
                full_log.write("")
                return (True, "Insert")
        elif (insertClassNum.testPrtSupp() == False and listClassNum.testPrtSupp() == True):
            full_log.write("")
            return (True, "List")
    if (insertClassNum.testNumNumber() == True and listClassNum.testNumNumber() == True):
        full_log.write("Both have a Number value\n")
        insrt_number = insertClassNum.getDescriptionDict()["Number"]
        insrt_num = 0
        insrt_alph = ""
        if insrt_number[0].isnumeric() == True:
            if "," in insrt_number:
                full_insrt_num = insrt_number.split(",", 1)
                if full_insrt_num[len(full_insrt_num)-1] != '':
                    insrt_number = full_insrt_num[len(full_insrt_num) - 1]
                else:
                    insrt_number = full_insrt_num[0]
            if "-" in insrt_number:
                if has_alphabet(insrt_number) == True:
                    insrt_alph = has_invalidchars(replace_nums(insrt_number.upper()))
                split_nums = insrt_number.split("-", 1)
                if split_nums[1][0].isnumeric():
                    insrt_num = int(split_nums[1])
                else:
                    insrt_num = int(split_nums[0])
                # insrt_num = int(remove_latter_half(insrt_number.split("-", 1)[1]))

            else:
                if has_alphabet(insrt_number) == True:
                    insrt_alph = replace_nums(insrt_number.upper())
                insrt_num = int(remove_latter_half(insrt_number))
        else:
            insrt_alph = insrt_number
        list_number = listClassNum.getDescriptionDict()["Number"]
        list_num = 0
        list_alph = ""
        if list_number[0].isnumeric() == True:
            if "," in list_number:
                full_list_num = list_number.split(",", 1)
                if full_list_num[len(full_list_num)-1] != '':
                    list_number = full_list_num[len(full_list_num) - 1]
                else:
                    list_number = full_list_num[0]
            if "-" in list_number:
                if has_alphabet(list_number) == True:
                    list_alph = replace_nums(list_number.upper())
                split_nums = list_number.split("-", 1)
                if split_nums[1][0].isnumeric():
                    list_num = int(split_nums[1])
                else:
                    list_num = int(split_nums[0])
                # list_num = int(remove_latter_half(list_number.split("-", 1)[1]))
            else:
                if has_alphabet(list_number) == True:
                    list_alph = replace_nums(list_number.upper())
                list_num = int(remove_latter_half(list_number))
        else:
            list_alph = list_number
        if (insrt_num > list_num):
            full_log.write("Insert has a larger number than the List.\n")
            return (True, "Insert")
        elif (insrt_num < list_num):
            full_log.write("List has a larger number than the Insert.\n")
            return (True, "List")
        else:
            full_log.write("Both have similar number values.\n")
            if (insrt_alph > list_alph):
                full_log.write("Insert has a larger alpha character.\n")
                return (True, "Insert")
            elif (insrt_alph < list_alph):
                full_log.write("List has a larger alpha character.\n")
                return (True, "List")
            else:
                full_log.write("Both have similar alpha characters for numbers.\n")
        if (insertClassNum.testNumVol() == True and listClassNum.testNumVol() == True):
            full_log.write("Both have a volume with their number\n")
            insert_num_vol = insertClassNum.getDescriptionDict()["Number Volume"]
            insrt_num_vol_num = 0
            insrt_num_vol_alph = ""
            if insert_num_vol[0].isnumeric() == True:
                if "-" in insert_num_vol:
                    if has_alphabet(insert_num_vol) == True:
                        insrt_num_vol_alph = replace_nums(insert_num_vol.upper())
                    split_num_pt = insert_num_vol.split("-", 1)
                    if split_num_pt[1][0].isnumeric():
                        insrt_num_vol_num = int(split_nums[1])
                    else:
                        insrt_num_vol_num = int(split_nums[0])
                else:
                    if has_alphabet(insert_num_vol) == True:
                        insrt_num_vol_alph = replace_nums(insert_num_vol.upper())
                    insrt_num_vol_num = int(remove_latter_half(insert_num_vol))
            else:
                insrt_num_vol_alph = replace_nums(insert_num_vol.upper())
            list_num_vol = listClassNum.getDescriptionDict()["Number Volume"]
            list_num_vol_num = 0
            list_num_vol_alph = ""
            if list_num_vol[0].isnumeric() == True:
                if "-" in list_num_vol:
                    if has_alphabet(list_num_vol) == True:
                        list_num_vol_alph = replace_nums(list_num_vol.upper())
                    split_num_pt = list_num_vol.split("-", 1)
                    if split_num_pt[1][0].isnumeric():
                        list_num_vol_num = int(split_nums[1])
                    else:
                        list_num_vol_num = int(split_nums[0])
                else:
                    if has_alphabet(list_num_vol) == True:
                        list_num_vol_alph = replace_nums(list_num_vol.upper())
                    list_num_vol_num = int(remove_latter_half(list_num_vol))
            else:
                list_num_vol_alph = replace_nums(list_num_vol.upper())
            if (insrt_num_vol_num > list_num_vol_num):
                full_log.write("Insert has a larger numeric vol than the list.\n")
                return (True, "Insert")
            elif (insrt_num_vol_num < list_num_vol_num):
                full_log.write("List has a larger numeric vol than the Insert.\n")
                return (True, "List")
            else:
                full_log.write("Insert and List have the same no. ## and v. ## value.\n")
                if (insrt_num_vol_alph > list_num_vol_alph):
                    full_log.write("Insert has a larger value than List with Alpha\n")
                    return (True, "Insert")
                elif (insrt_num_vol_alph < list_num_vol_alph):
                    full_log.write("List has a larger value than Insert with Alpha\n")
                    return (True, "List")
                else:
                    full_log.write("Both have the same alphabetical value\n")
        if (insertClassNum.testNumPart() == True and listClassNum.testNumPart() == True):
            full_log.write("Both have a part of their number.\n")
            insrt_number_pt = insertClassNum.getDescriptionDict()["Number Part"]
            insrt_num_pt = 0
            insrt_num_pta = ""
            if insrt_number_pt[0].isnumeric() == True:
                if "-" in insrt_number_pt:
                    if has_alphabet(insrt_number_pt) == True:
                        insrt_num_pta = replace_nums(insrt_number_pt.upper())
                    split_num_pt = insrt_number_pt.split("-", 1)
                    if split_num_pt[1][0].isnumeric():
                        insrt_num_pt = int(split_nums[1])
                    else:
                        insrt_num_pt = int(split_nums[0])
                    # insrt_num_pt = int(remove_latter_half(insrt_number_pt.split("-", 1)[1]))
                else:
                    if has_alphabet(insrt_number_pt) == True:
                        insrt_num_pta = replace_nums(insrt_number_pt.upper())
                    insrt_num_pt = int(remove_latter_half(insrt_number_pt))
            else:
                insrt_num_pta = replace_nums(insrt_number_pt.upper())
            list_number_pt = listClassNum.getDescriptionDict()["Number Part"]
            list_num_pt = 0
            list_num_pta = ""
            if list_number_pt[0].isnumeric() == True:
                if "-" in list_number_pt:
                    if has_alphabet(list_number_pt) == True:
                        list_num_pta = replace_nums(list_number_pt.split("-", 1)[1].upper())
                    split_num_pt = list_number_pt.split("-", 1)
                    if split_num_pt[1][0].isnumeric():
                        list_num_pt = int(split_nums[1])
                    else:
                        list_num_pt = int(split_nums[0])
                    # list_num_pt = int(remove_latter_half(list_number_pt.split("-", 1)[1]))
                else:
                    if has_alphabet(list_number_pt) == True:
                        list_num_pta = replace_nums(list_number_pt.upper())
                    list_num_pt = int(remove_latter_half(list_number_pt))
            else:
                list_num_pta = remove_latter_half(list_number_pt)
            if (insrt_num_pt > list_num_pt):
                full_log.write("Insert has a larger numeric part than the list.\n")
                return (True, "Insert")
            elif (insrt_num_pt < list_num_pt):
                full_log.write("List has a larger numeric part than the Insert.\n")
                return (True, "List")
            else:
                full_log.write("Insert and List have the same no. ## and pt. ## value.\n")
                if (insrt_num_pta > list_num_pta):
                    full_log.write("Insert has a larger value than List with Alpha\n")
                    return (True, "Insert")
                elif (insrt_num_pta < list_num_pta):
                    full_log.write("List has a larger value than Insert with Alpha\n")
                    return (True, "List")
                else:
                    full_log.write("Both have the same alphabetical value\n")
    if (insertClassNum.testSerSeries() == True and listClassNum.testSerSeries() == True):
        full_log.write("Both have a Series value\n")
        insert_series = insertClassNum.getDescriptionDict()["Series"]
        insrt_ser_num = 0
        insrt_ser_alph = ""
        if insert_series[0].isnumeric() == True:
            if "-" in insert_series:
                if has_alphabet(insert_series) == True:
                    insrt_ser_alph = replace_nums(insert_series.split("-", 1)[1].upper())
                insrt_ser_num = int(remove_latter_half(insert_series.split("-", 1)[1]))
            else:
                if has_alphabet(insert_series) == True:
                    insrt_ser_alph = replace_nums(insert_series.upper())
                insrt_ser_num = int(remove_latter_half(insert_series))
        else:
            insrt_ser_alph = replace_nums(insert_series.upper())
        list_series = listClassNum.getDescriptionDict()["Series"]
        list_ser_num = 0
        list_ser_alph = ""
        if list_series[0].isnumeric() == True:
            if "-" in list_series:
                if has_alphabet(insert_series) == True:
                    list_ser_alph = replace_nums(list_series)
                list_ser_num = int(remove_latter_half(list_series.split("-", 1)[1]))
            else:
                if has_alphabet(insert_series) == True:
                    list_ser_alph = replace_nums(list_series)
                list_ser_num = int(remove_latter_half(list_series))
        else:
            list_ser_alph = replace_nums(list_series.upper())
        if (insrt_ser_num > list_ser_num):
            full_log.write("Insert has a larger series than list.\n")
            return (True, "Insert")
        elif (insrt_ser_num < list_ser_num):
            full_log.write("Insert has a larger series than list.\n")
            return (True, "List")
        else:
            full_log.write("Both Insert and List have the same series number\n")
            if (insrt_ser_alph > list_ser_alph):
                full_log.write("Insert series has a larger alphabetical value\n")
                return (True, "Insert")
            elif (insrt_ser_alph < list_ser_alph):
                full_log.write("List series has a larger alphabetical value\n")
                return (True, "List")
            else:
                full_log.write("Both have the same series alphabetical value\n")
        if (insertClassNum.testSerVol() == True and listClassNum.testSerVol() == True):
            full_log.write("Both Series' have a volume\n")
            insert_series_pt = insertClassNum.getDescriptionDict()["Series Volume"]
            insrt_ser_pt = 0
            insrt_ser_pta = ""
            if insert_series_pt[0].isnumeric() == True:
                if "-" in insert_series_pt:
                    if (has_alphabet(insert_series_pt) == True):
                        insrt_ser_pta = replace_nums(insert_series_pt.upper())
                    insrt_ser_pt = int(remove_latter_half(insert_series_pt.split("-", 1)[1]))
                else:
                    if (has_alphabet(insert_series_pt) == True):
                        insrt_ser_pta = replace_nums(insert_series_pt.upper())
                    insrt_ser_pt = int(remove_latter_half(insert_series_pt))
            else:
                insrt_ser_pta = replace_nums(insrt_ser_pt.upper())
            list_series_pt = listClassNum.getDescriptionDict()["Series Volume"]
            list_ser_pt = 0
            list_ser_pta = ""
            if insert_series_pt[0].isnumeric() == True:
                if "-" in list_series_pt:
                    if (has_alphabet(list_series_pt) == True):
                        list_ser_pta = replace_nums(list_series_pt.upper())
                    list_ser_pt = int(remove_latter_half(list_series_pt.split("-", 1)[1]))
                else:
                    if (has_alphabet(list_series_pt) == True):
                        list_ser_pta = replace_nums(list_series_pt.upper())
                    list_ser_pt = int(remove_latter_half(list_series_pt))
            else:
                list_ser_pt = replace_nums(list_series_pt.upper())
            if (insrt_ser_pt > list_ser_pt):
                full_log.write("Insert has a larger series volume number\n")
                return (True, "Insert")
            elif (insrt_ser_pt < list_ser_pt):
                full_log.write("List has a larger series volume number\n")
                return (True, "List")
            else:
                full_log.write("Insert and List have the same volume number\n")
                if (insrt_ser_pta > list_ser_pta):
                    full_log.write("Insert series alphabet value is larger\n")
                    return (True, "Insert")
                elif (insrt_ser_pta > list_ser_pta):
                    full_log.write("List series alphabet value is larger\n")
                    return (True, "List")
                else:
                    full_log.write("Both series alphabet values are the same\n")
        if (insertClassNum.testSerIndex() == True and listClassNum.testSerIndex() == False):
            full_log.write("Insert has a series index number, list does not. Insert is the larger number.\n")
            return (True, "Insert")
        elif (insertClassNum.testSerIndex() == False and listClassNum.testSerIndex() == True):
            full_log.write("List has a series index number, insert does not. List is the larger number.\n")
            return (True, "List")
    elif (insertClassNum.testSerIndex() == True and listClassNum.testSerIndex() == False):
        full_log.write("Insert Callnumber has an index value while List does not, therefore Insert is greater\n")
        return (True, "Insert")
    elif (insertClassNum.testSerIndex() == False and listClassNum.testSerIndex() == True):
        full_log.write("List Callnumber has an index value while Insert does not, therefore List is greater\n")
        return (True, "List")
    elif (insertClassNum.testDescSupp() == True and listClassNum.testDescSupp() == False):
        full_log.write("Insert Callnumber has a Supplement value while List does not, therefore Insert is greater\n")
        return (True, "Insert")
    elif (insertClassNum.testDescSupp() == False and listClassNum.testDescSupp() == True):
        full_log.write("List Callnumber has a Supplement value while Insert does not, therefore List is greater\n")
        return (True, "List")
    elif (insertClassNum.testCopyNum() != None and listClassNum.testCopyNum() != None):
        full_log.write("Both have a copy number\n")
        if (insertClassNum.getDescriptionDict()["Copy Number"] > listClassNum.getDescriptionDict()["Copy Number"]):
            full_log.write("Insert has a larger Copy Number than List\n")
            return (True, "Insert")
        elif (insertClassNum.getDescriptionDict()["Copy Number"] < listClassNum.getDescriptionDict()["Copy Number"]):
            full_log.write("List has a larger Copy Number than List\n")
            return (True, "List")
    elif (insertClassNum.testCopyNum() != None and listClassNum.testCopyNum() == None):
        full_log.write("Insert has a copy number, while list does not. Insert has the higher value.\n")
        return (True, "Insert")
    elif (insertClassNum.testCopyNum() == None and listClassNum.testCopyNum() != None):
        full_log.write("List has a copy number, while insert does not. List has the higher value.\n")
        return (True, "List")
    full_log.write("All matched, no discrepancies found\n")
    return (False, "Neither")


'''
all_compare(ClassNumber insertClassNum, ClassNumber listClassNum):
insertClassNum: ClassNumber being put into the list and being compared with the listClassNum.
listClassNum: ClassNumber from the list that is being compared with the insertClassNum.
----
Function:
Goes through all the other comparison function and tests to see if either of the values is larger
than the either.
----
Return:
Tuple (Bool, String)
Bool = True if one value is larger than the others. False if all values in dictionary are equal.
String = Which of the values is larger.

If insertClassNum > listClassNum:
return ("Insert", True)
Else if insertClassNum < listClassNum:
return ("List", True)
Else:
return ("Neither", False)
'''
def all_compare(insertClassNum, listClassNum):
    class_comp = first_classify_compare(insertClassNum, listClassNum)
    if class_comp [0]== False:
        sec_class_comp = second_classify_compare(insertClassNum, listClassNum)
        if sec_class_comp[0] == False:
            desc_comp = description_compare(insertClassNum, listClassNum)
            if desc_comp[0] == False:
                return (False, "Neither")
            elif desc_comp[1] == "Insert":
                return (True, "Insert")
            elif desc_comp[1] == "List":
                return (True, "List")
        elif sec_class_comp[1] == "Insert":
            return (True, "Insert")
        elif sec_class_comp[1] == "List":
            return (True, "List")
    elif class_comp[1] == "Insert":
        return (True, "Insert")
    elif class_comp[1] == "List":
        return (True, "List")
    return (False, "Neither")

'''
DEPRECATED: NO LONGER IN USE
sort_NewCSVList(ClassNumber insertClassNum, List curr_csv_list, Str perm_call_num, str perm_call_desc):
insertClassNum: ClassNumber being inserted into the curr_csv_list.
curr_csv_list: List of ClassNumbers that will be placed onto the new csv file.
perm_call_num: Permanent Call Number Column Header Name.
perm_call_desc: Description Column Header Name.
----
Function:
Goes through the list of ClassNumbers and finds the correct place for the insertClassNum ClassNumber, where it will use
different comparison functions between the different values of each ClassNumber.
If there are no values inside of the curr_csv_list, then insertClassNum will be appended to the list.

Else if there are two ClassNumbers in the list, then the list class number will be compared with the insertClassNum, and
if the insert has a larger value then it will be appended. If the insert ClassNumber has a smaller value than the list
then it will be inserted at the beginning of the list.

If the list has two or more items, then a comparison will begin at the middle of the list and will continue to move left
if the insertClassNum is smaller than the middle value or move right if the insertClassNum is larger than the middle
ClassNumber. If the comparison is going left of the list, then the comparisons will continue until the a value smaller 
than the insertClassNum is found. If the comparison is going right, then it will continue until a value larger than the
insertClassNum is found.
---
Returns Nothing
'''
def sort_NewCSVList(insertClassNum, curr_csv_list, perm_call_num, perm_call_desc):
    # print("Sorting through CSV List")
    if len(curr_csv_list) == 0:
        curr_csv_list.append(insertClassNum)
        return
    elif len(curr_csv_list) == 1:
        list_classnum = curr_csv_list[0]
        # print("Comparing {} {} ".format(insertClassNum.details[perm_call_num],
        #                                 insertClassNum.details[perm_call_desc]) +
        #       "with {} {}".format(list_classnum.details[perm_call_num], list_classnum.details[perm_call_desc]))
        list_compare = first_classify_compare(insertClassNum, list_classnum)
        if list_compare[0] == False:
            sec_list_comp = second_classify_compare(insertClassNum, list_classnum)
            if sec_list_comp[0] == False:
                desc_list_comp = description_compare(insertClassNum, list_classnum)
                if desc_list_comp[0] == False:
                    curr_csv_list.append(insertClassNum)
                elif desc_list_comp[1] == "List":
                    curr_csv_list.insert(0, insertClassNum)
                elif desc_list_comp[1] == "Insert":
                    curr_csv_list.append(insertClassNum)
                return
            elif sec_list_comp[1] == "List":
                curr_csv_list.insert(0, insertClassNum)
            elif sec_list_comp[1] == "Insert":
                curr_csv_list.append(insertClassNum)
        elif list_compare[1] == "List":
            curr_csv_list.insert(0,insertClassNum)
        elif list_compare[1] == "Insert":
            curr_csv_list.append(insertClassNum)
        return
    else:
        left, right = 0, len(curr_csv_list)
        middle = (left + right) // 2
        mid_ClassNum = curr_csv_list[middle]
        # print("Comparing {} {} ".format(insertClassNum.details[perm_call_num],
        #                                 insertClassNum.details[perm_call_desc]) +
        #       "with {} {}".format(mid_ClassNum.details[perm_call_num], mid_ClassNum.details[perm_call_desc]))
        mid_comp = all_compare(insertClassNum, mid_ClassNum)
        if mid_comp[1] == "Insert":
            middle += 1
            while middle < len(curr_csv_list):
                # print("Comparing {} {} ".format(insertClassNum.details[perm_call_num],
                #                                 insertClassNum.details[perm_call_desc]) +
                #       "with {} {}".format(curr_csv_list[middle].details[perm_call_num],
                #                           curr_csv_list[middle].details[perm_call_desc]))
                right_comp = all_compare(insertClassNum, curr_csv_list[middle])
                if right_comp[1] == "Insert":
                    middle += 1
                elif right_comp[1] == "List":
                    curr_csv_list.insert(middle, insertClassNum)
                    break
                else:
                    curr_csv_list.insert(middle, insertClassNum)
                    break
            if middle == len(curr_csv_list):
                curr_csv_list.insert(middle, insertClassNum)
        elif mid_comp[1] == "List":
            middle -= 1
            while middle >= 0:
                # print("Comparing {} {} ".format(insertClassNum.details[perm_call_num],
                #                                 insertClassNum.details[perm_call_desc]) +
                #       "with {} {}".format(curr_csv_list[middle].details[perm_call_num],
                #                           curr_csv_list[middle].details[perm_call_desc]))
                left_comp = all_compare(insertClassNum, curr_csv_list[middle])
                if left_comp[1] == "Insert":
                    curr_csv_list.insert(middle + 1, insertClassNum)
                    break
                elif left_comp[1] == "List":
                    middle -= 1
                else:
                    curr_csv_list.insert(middle, insertClassNum)
                    break
            if middle < 0:
                curr_csv_list.insert(middle + 1, insertClassNum)
        else:
            curr_csv_list.append(insertClassNum)


'''
sort_CSVBinary(ClassNumber insertClassNum, List curr_csv_list, Str perm_call_num, str perm_call_desc):
insertClassNum: ClassNumber being inserted into the curr_csv_list.
curr_csv_list: List of ClassNumbers that will be placed onto the new csv file.
perm_call_num: Permanent Call Number Column Header Name.
perm_call_desc: Description Column Header Name.
---
Function:
Use a modified Binary Search algorithm to compare the different values in the curr_csv_list, where left is the smallest
values and right is the largest values in the list. Where middle value represents the middle of the current search and
will continue to change, along with the left or right, until the right place for the insertClassNum has been found and
has been inserted.
--
Returns:
Nothing

'''
def sort_CSVBinary(insertClassNum, curr_csv_list, perm_call_num, perm_call_desc):
    if len(curr_csv_list) == 0:
        curr_csv_list.append(insertClassNum)
        return
    elif len(curr_csv_list) == 1:
        list_classnum = curr_csv_list[0]
        full_log.write("Comparing {} {} ".format(insertClassNum.getDetails()[perm_call_num],
                                        insertClassNum.getDetails()[perm_call_desc]) +
              "with {} {} \n".format(list_classnum.getDetails()[perm_call_num],
                                  list_classnum.getDetails()[perm_call_desc]))
        try:
            list_compare = first_classify_compare(insertClassNum, list_classnum)
        except Exception as exeption:
            logging.log(level=40, msg="call: {} desc: {} \n with \n call: {}  desc: {}".format(insertClassNum.getDetails()[perm_call_num],
                                        insertClassNum.getDetails()[perm_call_desc],
                                                                list_classnum.getDetails()[perm_call_num],
                                                                list_classnum.getDetails()[perm_call_desc]
                                                                ))
            logging.error(traceback.format_exc())
        if list_compare[0] == False:
            sec_list_comp = second_classify_compare(insertClassNum, list_classnum)
            if sec_list_comp[0] == False:
                desc_list_comp = description_compare(insertClassNum, list_classnum)
                if desc_list_comp[0] == False:
                    curr_csv_list.append(insertClassNum)
                elif desc_list_comp[1] == "List":
                    curr_csv_list.insert(0, insertClassNum)
                elif desc_list_comp[1] == "Insert":
                    curr_csv_list.append(insertClassNum)
                return
            elif sec_list_comp[1] == "List":
                curr_csv_list.insert(0, insertClassNum)
            elif sec_list_comp[1] == "Insert":
                curr_csv_list.append(insertClassNum)
        elif list_compare[1] == "List":
            curr_csv_list.insert(0,insertClassNum)
        elif list_compare[1] == "Insert":
            curr_csv_list.append(insertClassNum)
        return
    else:
        left, right = 0, len(curr_csv_list)-1
        middle = (left + right) // 2
        while left <= right:
            mid_ClassNum = curr_csv_list[middle]
            full_log.write("Comparing {} {} ".format(insertClassNum.getDetails()[perm_call_num],
                                            insertClassNum.getDetails()[perm_call_desc]) +
                  "with {} {} \n".format(mid_ClassNum.getDetails()[perm_call_num],
                                      mid_ClassNum.getDetails()[perm_call_desc]))
            try:
                mid_comp = all_compare(insertClassNum, mid_ClassNum)
            except Exception as exeption:
                logging.log(level=40, msg="call: {} desc: {} \n with \n call: {}  desc: {}".format(insertClassNum.getDetails()[perm_call_num],
                                        insertClassNum.getDetails()[perm_call_desc],
                                                                mid_ClassNum.getDetails()[perm_call_num],
                                                                mid_ClassNum.getDetails()[perm_call_desc]
                                                                ))
                logging.error(traceback.format_exc())
            if mid_comp[1] == "Insert":
                left = middle + 1
                middle = (left + right) // 2
            elif mid_comp[1] == "List":
                right = middle - 1
                middle = (left + right) // 2
            else:
                curr_csv_list.insert(middle + 1, insertClassNum)
                return
        curr_csv_list.insert(left, insertClassNum)
        return

'''
read_through_excelsheet(string filename, string sheetname, string callnumberheader, string descriptionheader):
filename: a string value that represents the filename and path to the excel spreadsheet
sheetname: a string value that represents the name of the sheet that is currently being sorted through
callnumberheader: a string value that represents the header of the call-number column
descriptionheader: a string value that represents the name of the description column
---
Function:
Goes through the excelsheet to create different callnumber objects that will be sorted and put on a new excel 
spreadsheet.
'''
def read_through_excelsheet(filename,sheetname,callnumberheader,descriptionheader):
    print("Loading the excel spreadsheet information...")
    excel_sheet = pandas.read_excel(io=filename, header=0, sheet_name=sheetname)
    headers = excel_sheet.columns
    if callnumberheader not in headers:
        return ("Invalid", "Permanent Call Number")
    elif descriptionheader not in headers:
        return ("Invalid", "Description")
    csv_header = []
    for header in headers:
        csv_header.append(header)
    rowamnt = excel_sheet.shape[0]
    full_list = []
    # f = open("debug_log.txt", "w")
    print("Beginning to process and sort information...")
    for row in tqdm(range(int(rowamnt)), desc="Rows Processed", unit='rows', colour='white'):
        # print("On Item {} out of {}".format(row + 1, rowamnt))
        curr_item = excel_sheet.iloc[row]
        callnum = curr_item[callnumberheader]
        if isinstance(callnum, float) == True:
            continue
        desc = curr_item[descriptionheader]
        # f.write("{} {} ".format(callnum,desc))
        values = curr_item.values
        values_dict = {}
        for value in range(values.size):
            if isinstance(values[value], str) == False:
                values_dict.update({headers[value]: " "})
            else:
                values_dict.update({headers[value]: values[value]})
        try:
            callnumDictionary = createnewCallNum(callnum, desc, values_dict)
            # f.write("CallNumCreated: X ")
        except Exception as exeption:
            logging.log(level=40, msg="call: {} desc: {}".format(callnum, desc))
            logging.error(traceback.format_exc())

        # sort_NewCSVList(callnumDictionary, full_list, callnumberheader, descriptionheader)
        try:
            sort_CSVBinary(callnumDictionary,full_list,callnumberheader, descriptionheader)
            # f.write("Compared and Sorted: X \n")
        except  Exception as exeption:
            logging.log(level=40, msg="{} {}".format(callnum, desc))
            logging.error(traceback.format_exc())

        full_log.write("\n------Next Item------\n")
        # print("Going to next item")
    # f.close()
    full_log.write("\n\n-------Finished Sorting-------\n\n")
    return (csv_header,full_list)


'''
createnewCallNum(str callnumber, str description):
callnumber: Call number values from the Permanent Call Number Description
description: Call number values from the Descrption column
Function:
Looks through the callnumber and description strings to look for the different call number values that can be used
to sort all the callnumbers inside of the excel spreadsheet.
----
Return:
CallNum new_callnum- Newly created CallNumber Object
'''
def createnewCallNum(callnumber, description, details_dictionary):
    callnumber = insert_space(callnumber)
    # print("Creating {}".format(callnumber))
    full_log.write("Creating {}\n".format(callnumber))
    call_list = callnumber.split(" ")

    newcallnumDict = {}
    callnum_features = {}
    desc_features = {}
    vol_num = None
    vol_part = None
    vol_index = None
    vol_supp = None
    part_num = None
    part_vol = None
    part_sup = None
    number = None
    number_pt = None
    num_vol = None
    num_index = None
    num_supp = None
    series = None
    ser_vol = None
    ser_ind = None
    ser_sup = None
    copy_num = None
    supplement = False
    index = False
    other = ""


    ## Mainly in the Permanent Call Number ##
    for val in range(len(call_list)):
        if val == 0:
            class_num = has_invalidchars(call_list[0])
            if call_list[0][1].isalpha() == True and call_list[0][2].isalpha() == False:
                newcallnumDict["classification_letter"] = class_num[0:2].upper()
                if has_numbers(class_num[2:]) == True:
                    class_num = replace_alphchars(class_num)
                    newcallnumDict["classification_number"] = float(class_num)
                else:
                    newcallnumDict["classification_number"] = 0.0
            elif call_list[0][1].isalpha() == True and call_list[0][2].isalpha() == True:
                newcallnumDict["classification_letter"] = class_num[0:3].upper()
                if has_numbers(class_num[3:]) == True:
                    class_num = replace_alphchars(class_num)
                    newcallnumDict["classification_number"] = float(class_num)
                else:
                    newcallnumDict["classification_number"] = 0.0
            else:
                newcallnumDict["classification_letter"] = class_num[0:1].upper()
                if has_numbers(class_num[1:]) == True:
                    class_num = replace_alphchars(class_num)
                    newcallnumDict["classification_number"] = float(class_num)
                else:
                    newcallnumDict["classification_number"] = 0.0
        elif val == 1:
            cutter_num = has_invalidchars(call_list[val])
            if '.' not in call_list[val]:
                newcallnumDict["cutter_letter"] = call_list[val][0:1]
                if has_numbers(cutter_num) == True:
                    cutter_num = replace_alphchars(cutter_num)
                    newcallnumDict["cutter_num"] = float('.' + cutter_num)
                else:
                    newcallnumDict["cutter_num"] = 0.0
            else:
                newcallnumDict["cutter_letter"] = call_list[val][1:2]
                if has_numbers(cutter_num) == True:
                    cutter_num = replace_alphchars(cutter_num)
                    newcallnumDict["cutter_num"] = float(cutter_num)
                else:
                    newcallnumDict["cutter_num"] = 0.0
        elif val >= 2:
            if call_list[val][0:1].isalpha() == True:
                full_log.write("Is Alpha\n")
                if call_list[val][1:2].isnumeric():
                    full_log.write("Is second cutter\n")
                    sec_cutter = has_invalidchars(call_list[val])
                    callnum_features["second cutletter"] = sec_cutter[0:1]  # Second cutter letter that follows the first cutter
                    callnum_features["second cutnumber"] = float('.' + sec_cutter[1:])  # Second cutter number, decimal value, that follows the second cutter number
                else:
                    full_log.write("Not second cutter\n")
                    if 'sup.' in call_list[val] and number == None and vol_num == None and part_num == None\
                            and series == None:
                        callnum_features["supplement"] = True
                    elif 'Index' in call_list[val]:
                        callnum_features["Call Index"] = True
                    elif call_list[val][0:2] == "v." and vol_num == None and part_num == None and series == None:
                        vol_num = call_list[val][2:]
                        desc_features["Volume Number"] = vol_num
                    elif call_list[val][0:2] == "v." and part_num != None and series == None and number == None:
                        part_vol = call_list[val][2:]
                        desc_features["Part Volume"] = part_vol
                    elif call_list[val][0:2] == "v." and part_num == None and series != None and number == None:
                        ser_vol = call_list[val][2:]
                        desc_features["Series Volume"] = ser_vol
                    elif call_list[val][0:2] == "v." and part_num == None and series == None and number != None:
                        num_vol = call_list[val][2:]
                        desc_features["Number Volume"] = num_vol
                    elif call_list[val][0:3] == "pt." and part_num == None and vol_num == None and number == None:
                        part_num = call_list[val][3:]
                        desc_features["Part Number"] = part_num
                    elif call_list[val][0:3] == "pt." and vol_num != None and number == None:
                        vol_part = call_list[val][3:]
                        desc_features["Volume Part"] = vol_part
                    elif call_list[val][0:3] == "pt." and vol_num == None and number != None:
                        number_pt = call_list[val][3:]
                        desc_features["Number Part"] = number_pt
                    elif call_list[val][0:3] == "no." and number == None:
                        number = call_list[val][3:]
                        desc_features["Number"] = number
                    elif call_list[val][0:4] == "ser." and series == None:
                        series = call_list[val][4:]
                        desc_features["Series"] = series


            elif call_list[val][0:1].isnumeric():
                full_log.write("Is Year\n")
                callnum_features["Publication Year"] = has_invalidchars(call_list[val])
            else:
                full_log.write("Is Other\n")
                if "Other" not in callnum_features:
                    callnum_features["Other"] = call_list[val:]
                    break
                else:
                    callnum_features["Other"] += call_list[val:]
                    break

    if type(description) == str and description != '':
        desc_list = description.split(" ")
        for val in range(len(desc_list)):
            if has_alphabet(desc_list[val]) == False and has_numbers(desc_list[val]) == True:
                callnum_features["Publication Year"] = has_invalidchars(desc_list[val])
            elif desc_list[val][0:2] == "v." and vol_num == None and part_num == None and series == None\
                    and number == None:
                vol_num = desc_list[val][2:]
                desc_features["Volume Number"] = vol_num
            elif desc_list[val][0:2] == "v." and part_num != None and series == None and number == None:
                part_vol = desc_list[val][2:]
                desc_features["Part Volume"] = part_vol
            elif desc_list[val][0:2] == "v." and part_num == None and series != None and number == None:
                ser_vol = desc_list[val][2:]
                desc_features["Series Volume"] = ser_vol
            elif desc_list[val][0:2] == "v." and part_num == None and series == None and number != None:
                num_vol = desc_list[val][2:]
                desc_features["Number Volume"] = num_vol
            elif desc_list[val][0:3] == "pt." and part_num == None and vol_num == None and number == None:
                part_num = desc_list[val][3:]
                desc_features["Part Number"] = part_num
            elif desc_list[val][0:3] == "pt." and vol_num != None and number == None:
                vol_part = desc_list[val][3:]
                desc_features["Volume Part"] = vol_part
            elif desc_list[val][0:3] == "pt." and vol_num == None and number != None:
                number_pt = desc_list[val][3:]
                desc_features["Number Part"] = number_pt
            elif desc_list[val][0:3] == "no.":
                number = desc_list[val][3:]
                desc_features["Number"] = number
            elif desc_list[val][0:4] == "ser.":
                series = desc_list[val][4:]
                desc_features["Series"] = series
            elif (desc_list[val] == "Index" or desc_list[val] == "index") and vol_num == None and series == None and\
                number == None:
                index = True
                desc_features["Index Bool"] = index
            elif (desc_list[val] == "Index" or desc_list[val] == "index") and vol_num != None and series == None and\
                    number == None:
                vol_index = True
                desc_features["Volume Index"] = vol_index
            elif (desc_list[val] == "Index" or desc_list[val] == "index") and vol_num == None and series == None and\
                    number == None:
                ser_ind = True
                desc_features["Series Index"] = ser_ind
            elif (desc_list[val] == "Index" or desc_list[val] == "index") and vol_num == None and series == None and \
                    number != None:
                num_index = True
                desc_features["Number Index"] = num_index
            elif desc_list[val] == "sup." and vol_num == None and part_num == None and series == None and\
                    number == None:
                supplement = True
                desc_features["Supplement Bool"] = supplement
            elif desc_list[val] == "sup." and vol_num != None and part_num == None and series == None and\
                    number != None:
                vol_supp = True
                desc_features["Volume Supplement"] = vol_supp
            elif desc_list[val] == "sup." and vol_num == None and part_num != None and series == None and\
                    number == None:
                part_sup = True
                desc_features["Part Supplement"] = part_sup
            elif desc_list[val] == "sup." and vol_num == None and part_num != None and series == None and\
                    number == None:
                ser_sup = True
                desc_features["Series Supplement"] = ser_sup
            elif desc_list[val] == "sup." and vol_num == None and part_num != None and series == None and \
                    number == None:
                num_supp = True
                desc_features["Number Supplement"] = num_supp
            elif desc_list[val][0:4] == "cop.":
                copy_num = desc_list[val][4:]
                desc_features["Copy Number"] = copy_num
            else:
                other += desc_list[val]
        desc_features["Other details"] = other

    new_callnum = Callnumber.CallNumber(newcallnumDict,callnum_features,desc_features, details_dictionary)

    # print("Finishing setting the new call number variable values")
    full_log.write("Finishing setting the new call number variable values\n"
                   "----Comparing and Setting Call Number on List----\n")
    return new_callnum

'''
setonnewCSV( List csv_headers, List full_lst, Str newcsvName):
csv_headers: List of headers from the original Sheet to be set onto the new csv file.
full_list: All of the CallNumber values that have been sorted with details of the original excel sheet entry
stored into a dictionary value.
----
Function:
Sets the field name from the csv_headers, and then goes through the full_lst list of sorted CallNumbers to
then place their details values onto the new csvfile.
----
Return:
None
'''
def setonnewCSV(csv_headers, full_lst, newcsvName, pathToNewCSVName):
    new_path = os.path.join(pathToNewCSVName, newcsvName)
    with open(new_path, 'w', newline='', encoding='utf-8') as csvfile:
        field_names = csv_headers
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for item in range(len(full_lst)):
            curr_row = full_lst[item].getDetails()
            writer.writerow(curr_row)
        full_log.write("\n\n-------Finished Sorting-------\n\n")

'''
DEPRECATED- No longer being worked on, CSV function fulfills the same requirements. 
setonnewExcelSheet(array headers ,array full_list, str sheet_name, str workbook_name):
headers= array of header values from the csv file
full_lst= full list of values from the original excel sheet
sheet_name= name of the original sheet being read from
workbook_name= name of the original work_book
---
Function:
Grabs the details values from the full_lst and places them into a dataframe to be placed into a new Excelsheet.
--
To Do:
Find a way to place them onto a new sheet or a new excel workbook. 
---
Return:
None
'''
def setonnewExcelSheet(newCSVName, full_lst,sheet_name, pathToNewCSVName):
    new_path = os.path.join(pathToNewCSVName, newCSVName)
    to_spreadsheet = []
    for item in range(len(full_lst)):
        curr_row = full_lst[item].getDetails()
        to_spreadsheet.append(curr_row)
    dataframe = pandas.DataFrame(to_spreadsheet)
    dataframe.to_excel(excel_writer=new_path, sheet_name=sheet_name, index=False)
    full_log.close()


    # print("Excel Sheet")

