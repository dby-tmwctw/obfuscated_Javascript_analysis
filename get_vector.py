# -*- coding: utf -8 -*-
import os
import statistics

def str_with_num_and_char(string_array):
    # Returns the share of strings containing numbers or special char in all strings
    # 返回含数字或特殊字符的字符串占所有字符串的比例
    # 特殊字符串包括 '_', '#', '=', '-', '+', '<', '>', '(', ')', '.', ','
    count = 0
    for string in string_array:
        if contains_num_or_special_char(string):
            count += 1
    return 0 if len(string_array) == 0 else count / len(string_array)

def contains_num_or_special_char(string):
    # Returns a boolean indicating whether the string contains a number or special char
    # 返回string是否含有数字或特殊字符
    num_char_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', '#', '=', '-', '+', '<', '>', '(', ')', '.', ',']
    for char in string:
        if char in num_char_list:
            return True
    return False

def substrings(target_strings):
    # Given a list of strings, return a list of substrings
    # 输入一个字符串列表，返回子串列表
    substrings = []
    for target_string in target_strings:
        for i in range(len(target_string)):
            for j in range(i + 1, len(target_string) + 1):
                substrings.append(target_string[i:j])
    return substrings

# All target strings are in lower case
# 目标字符串列表中的字符串全部已转为小写
target_strings = ['wscript.shell', 'readystate', 'regwrite', '%temp%/', 'aplet.dll', 'quit', '.dll', '/elevate', 'responsebody',
'type', 'get', 'savetofile', 'folderexists', 'regsvr32 /s ', 'position', 'send', 'open', 'exists', 'msxml2.xmlhttp', 'arguments',
'div', 'scriptfullname', 'createtextfile', 'finish.scr', 'runas', 'floor', '.exe', 'random', '%username%', '%appdata%', 'sleep',
'fileexists', 'adodb.stream', 'write', 'c:\\users\\', 'run', 'close', 'fromcharcode', 'eval', 'createobject', 'expandenvironmentstrings',
 'elevate', 'activexobject', 'split', 'scripting.filesystemobject', 'string.fromcharcode()', 'wscript', '%temp%', 'shellexecute',
 'shell.application', 'fullname', 'reg_dword', 'named', 'c:\\programdata\\trava', 'c:\\windows\\syswow64\\', 'c:\\windows\\system32\\',
'c:\\program files (x86)\\', '"c:\\program files\\gbplugin"']

substrings_list = substrings(target_strings)

# count_hit returns the number of hits of substrings. Single letter hits and whole word hits are not counted
# count_hit返回strings中有多少个子串命中。忽略单字母命中，忽略全词命中。
def count_hit(strings):
    count = 0
    for string in strings:
        if (string.lower() in substrings_list) and len(string) > 1 and string not in target_strings:
            count += 1
    if (len(strings) < 10):
        count = 0
    return count


#---------------------Main Function---------------------#
#-------------------------主函数-------------------------#

def get_vector(abnormal_count, plus_equal_percentage, square_bracket_percentage, string_list):
    # 构建特征向量
    feature_vector = []

    # f0: +和+=的数量 / 运算符数量 ***
    feature_vector.append(plus_equal_percentage)
    # f1: 字符串数量 / token数量
    #feature_vector.append(string_count / token_count)
    # f2: 字符串平均长度 ***
    feature_vector.append(ave_string_length(string_list))
    # f3: 长度为1-5的字符串数量 / 字符串总数 ***
    feature_vector.append(count_1_to_5(string_list))
    # f4: 特殊字符(.\/@#%:_&) / 字符串总长度
    feature_vector.append(count_special_char(string_list))
    # f5: charAt, fromCharCode, eval数量 / token数量
    #feature_vector.append(charAt_fromCharCode_eval_percentage)
    # f6: [ 数量 / token数量
    feature_vector.append(square_bracket_percentage)
    # f7: 含数字和特殊字符的字符串数量 / 字符串总数 ***
    feature_vector.append(str_with_num_and_char(string_list))
    # f8: 命中数 / 字符串总数 ***
    feature_vector.append(count_hit(string_list))
    # f9: 异常函数调用 / identifier总数 ***
    feature_vector.append(abnormal_count)

    return feature_vector

def ave_string_length(string_list):
    # Returns the average string length
    # 返回脚本中所有字符串的平均长度
    length_list = []
    for string in string_list:
        length_list.append(len(string))
    return 0 if len(length_list) == 0 else statistics.mean(length_list)

def count_1_to_5(string_list):
    # Returns the share of strings of length 1-5 among all strings
    # 返回长度为1-5的字符串占所有字符串中的比例
    result_count = 0
    for i in string_list:
        if (len(i) >= 1 and len(i) <= 5):
            result_count += 1
    return 0 if len(string_list) == 0 else result_count / len(string_list)

def count_special_char(string_list):
    # Returns the ratio of special characters (.,\/@#%:_&) to the total string length
    # 返回特殊字符(.,\/@#%:_)占字符串总长度的比例
    special_set = {'.', ',', '\\', '/', '@', '#', '%', '_', '&'}
    special_count = 0
    total_string_length = 0
    for i in string_list:
        if i in special_set:
            special_count += 1
        total_string_length += len(i)
    return 0 if total_string_length == 0 else special_count / total_string_length

#---------------------Execution---------------------#
#vect = get_vector('/Users/chenpengyuan/Desktop/Virus/fb0c9ea4406e98e48b579d3d0a1a3550', '/Users/chenpengyuan/Desktop/JavaScriptKeywords.txt')
#print(vect)
'''
abnormal_result_array = []
l = []
for root, dirs, files in os.walk('/Users/chenpengyuan/Desktop/has_concatenation'):
    l.extend(files)
for f in l:
    vector = get_vector('/Users/chenpengyuan/Desktop/has_concatenation/' + f, '/Users/chenpengyuan/Desktop/JavaScriptKeywords.txt')
    vector.append(1)
    # 1是类别，代表有拼接
    abnormal_result_array.append(vector)
# print(abnormal_result_array)
# print("---------------------------------------------")
normal_result_array = []
for i in range(1, 101):
    try:
        vector = get_vector('/Users/chenpengyuan/Desktop/1/File ' + str(i) + '.js', '/Users/chenpengyuan/Desktop/JavaScriptKeywords.txt')
        vector.append(0)
        # 0是类别，代表无拼接
        normal_result_array.append(vector)
    except:
       pass
'''
# print(normal_result_array)
