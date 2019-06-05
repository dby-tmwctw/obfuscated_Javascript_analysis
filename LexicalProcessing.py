# -*- coding: utf-8 -*-

from collections import *
import os

'''
输入输出定义：

initialize函数：输入程序路径和关键字路径，返回字符串表示的程序、关键字集合、转义字符
映射与字符/关键字映射
parse_xxx：输入当前为止所有程序以及其他一些集合/映射，返回一个tuple。Tuple的形式为：
（是否检测到此种token，token，token长度）
lexical_processing函数：输入程序路径和关键字路径，对JavaScript程序进行词法分析并输出
一个包含所有词法单元的序列。每个词法单元是一个tuple，形式为（token，token种类，编码）
lexical_processing是此程序的主函数

Input-Output Definitions:

initialize:Input programme path and keyword path, return a string
representation of the programme, a keyword set, a escape character mapping and
a character/keyword mapping
parse_xxx:Input a string representation of the rest of the programme, return
whether it starts with the pattern this function is trying to detect. If so,
return a tuple in the form of (whether the token is detected, token, length of
the token)
lexical_processing:Input a programme path and a keyword path, perform lexical
analysis for the JavaScript programme and output a sequence of tokens. Each
token is in the form (token, type of token, number for this token)
lexical_processing is the main function of the programme
'''

def initialize(content_path, keyword_path):
    '''
    Initialization for the programme
    '''

    # Read in content
    test_object = open(content_path)
    content = test_object.read()

    # Keyword set
    keyword_document = open(keyword_path)
    keyword_string = keyword_document.read()
    keyword_list = list(keyword_string.split())
    keyword_set = set(keyword_list)
    # print keyword_set

    # Escape mapping
    escape_map = {}
    escape_map["\'"] = '\''
    escape_map['\"'] = '\"'
    escape_map['&'] = '&'
    escape_map['\\'] = '\\'
    escape_map['n'] = '\n'
    escape_map['r'] = '\r'
    escape_map['b'] = '\b'
    escape_map['f'] = '\f'
    escape_map['/'] = '/'
    escape_map['%'] = '%'
    escape_map['t'] = '\t'
    escape_map['\n'] = ''
    escape_map['d'] = '\d'
    escape_map['A'] = '\A'
    escape_map['>'] = '\>'
    escape_map['p'] = '\p'
    escape_map['.'] = '\.'

    #Character and keyword mapping
    special_character = list([';', ':', ',', '\\', '.', '?'])
    delimiter = list(['(', ')', '{', '}', '[', ']'])
    operational_character = list(['=', '+=', '-=', '*=', '/=', '%=', '+', '-', '*', '/', '%', '++', '--', '<<', '>>', '>>>', '&', '|', '^', '~'])
    comparational_character = list(['==', '===', '!=', '!==', '<', '>', '>=', '<=', '&&', '||', '!'])
    all_character = []
    all_character.extend(special_character)
    all_character.extend(delimiter)
    all_character.extend(operational_character)
    all_character.extend(comparational_character)
    all_character_set = set(all_character)
    all_character_keyword = list(all_character)
    all_character_keyword.extend(keyword_list)
    all_character_keyword_set = set(all_character_keyword)
    character_map = defaultdict(int)
    for i in range(1, len(all_character_keyword) + 1):
        character_map[all_character_keyword[i-1]] = i
    character_keyword_length = len(character_map.keys())
    string_signature = character_keyword_length + 1
    identifier_signature = character_keyword_length + 2
    number_signature = character_keyword_length + 3
    regex_signature = character_keyword_length + 4
    character_map['string'] = string_signature
    character_map['identifier'] = identifier_signature
    character_map['number'] = number_signature
    character_map['regex'] = regex_signature
    # print character_map


    return content, keyword_set, escape_map, character_map

def get_character_map(keyword_path):
    keyword_document = open(keyword_path)
    keyword_string = keyword_document.read()
    keyword_list = list(keyword_string.split())
    keyword_set = set(keyword_list)
    special_character = list([';', ':', ',', '\\', '.', '?'])
    delimiter = list(['(', ')', '{', '}', '[', ']'])
    operational_character = list(['=', '+=', '-=', '*=', '/=', '%=', '+', '-', '*', '/', '%', '++', '--', '<<', '>>', '>>>', '&', '|', '^', '~'])
    comparational_character = list(['==', '===', '!=', '!==', '<', '>', '>=', '<=', '&&', '||', '!'])
    all_character = []
    all_character.extend(special_character)
    all_character.extend(delimiter)
    all_character.extend(operational_character)
    all_character.extend(comparational_character)
    all_character_set = set(all_character)
    all_character_keyword = list(all_character)
    all_character_keyword.extend(keyword_list)
    all_character_keyword_set = set(all_character_keyword)
    character_map = defaultdict(int)
    for i in range(1, len(all_character_keyword) + 1):
        character_map[all_character_keyword[i-1]] = i
    return character_map

def parse_comment(content):
    '''
    Given a string representation of a programme, check whether it starts with
    a comment. If so, return the number of positions we need to skip
    '''
    if (content[0] == '/'):
        if (content[1] == '*'):
            index = content.find('*/', 2)
            if (index != -1):
                return True, '', index + 2
            else:
                return True, -1, index + 2
        elif (content[1] == '/'):
            index = content.find('\n', 2)
            if (index == -1):
                index = content.find('\r', 2)
            if (index != -1):
                return True, '', index + 1
    return False, '', 0

def parse_string(content, escape_map):
    '''
    Given a string representation of a programme, test whether it starts with a
    string. If so, return the string and the number of positions we should skip
    '''
    if ((content[0] == '\"') or (content[0] == '\'') or (content[0] == '`')):
        # print '-------------------------------------------------'
        string_token = ''
        slash_detector = False
        index = 1
        if (content[0] == '\''):
            while index < len(content):
                if (content[index] == '\'') and (slash_detector == False):
                    break
                if (content[index] == '\\') and (slash_detector == False):
                    slash_detector = True
                else:
                    slash_detector = False
                index += 1
            # index = content.find('\'', 1)
            # while (index != -1) and (content[index-1] == '\\') and (content[index-2] != '\\'):
            #     index = content.find('\'', index + 1)
        elif (content[0] == '\"'):
            while index < len(content):
                # print index
                # print content[index]
                # print slash_detector
                if (content[index] == '\"') and (slash_detector == False):
                    # print 'Exit'
                    break
                if (content[index] == '\\') and (slash_detector == False):
                    # print 'Slash detected'
                    slash_detector = True
                    index += 1
                    continue
                # print 'Slash changed'
                slash_detector = False
                index += 1
            # index = content.find('\"', 1)
            # while (index != -1) and (content[index-1] == '\\') and (content[index-2] != '\\'):
            #     index = content.find('\"', index + 1)
        else:
            while index < len(content):
                # print 'Entered'
                if (content[index] == '`') and (slash_detector == False):
                    break
                if (content[index] == '\\') and (slash_detector == False):
                    slash_detector = True
                else:
                    slash_detector = False
                index += 1
            # index = content.find('\'', 1)
            # while (index != -1) and (content[index-1] == '\\') and (content[index-2] != '\\'):
            #     index = content.find('\'', index + 1)
        # print index
        if (index != -1):
            # if (content[index-1] != '\\'):
            range_list = iter(range(1, index))
            for i in range_list:
                if (content[i] != '\\'):
                    string_token += content[i]
                elif (i < index - 1):
                    # print 'entered'
                    try:
                        if (content[i+1] == 'x'):
                            string_token += '\\x'
                            string_token += str(int(content[i+2:i+4], 16))
                            range_list.next()
                            range_list.next()
                            range_list.next()
                        elif (content[i+1] == 'u'):
                            string_token += '\\u'
                            range_list.next()
                        else:
                            string_token += escape_map[content[i+1]]
                            range_list.next()
                    except KeyError:
                        string_token += content[i+1]
                        range_list.next()
            # print len(string_token)
            # print string_token
            return True, string_token, index + 1
    return False, '', 0

# print parse_string(read_string)
# print read_string[parse_string(read_string)[2]:]
# print parse_string('\"\n\"123')

def parse_identifier_keyword(content):
    '''
    Given a string representation of a programme, check if it starts with an
    identifier or keyword. If so, return whether it is an identifier or
    keyword (0 represents keyword and 1 represents identifier), and the
    identifier or keyword itself.
    '''
    if ((content[0].isalpha()) or (content[0] == '$') or (content[0] == '_')):
        identifier_keyword = ''
        identifier_keyword += content[0]
        content_length = len(content)
        index = 1
        while (index < content_length):
            if ((content[index].isalpha()) or (content[index].isdigit()) or (content[index] == '$') or (content[index] == '_')):
                identifier_keyword += content[index]
                index += 1
            else:
                break
        return True, identifier_keyword, len(identifier_keyword)
    return False, '', 0

def parse_number(content):
    '''
    Given a string representation of a programme, check whether it starts with
    a number. If so, return a string representation of that number.
    '''
    hexical_number = set(['a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F'])
    if ((content[0].isdigit()) or ((content[0] == '.') and (content[1].isdigit()))):
        number = ''
        number += content[0]
        scientific_representation = False
        index = 1
        # In the while loop below, we assume the JavaScript gives us a valid
        # number
        while index < len(content):
            if (content[index].isdigit()) or (content[index] in hexical_number) or (content[index] == '.') or (content[index] == 'x'):
                number += content[index]
                index += 1
            elif (content[index] == 'e') or (content[index] == 'E'):
                number += content[index]
                scientific_representation = True
                index += 1
            elif ((scientific_representation) and ((content[index] == '+') or (content[index] == '-'))):
                number += content[index]
                scientific_representation = False
                index += 1
            else:
                break
        return True, number, len(number)
    return False, '', 0

def parse_character(content, character_map):
    '''
    Given a string representation of a programme, check whether it starts with
    a character. If so, return the longest possible character found.
    '''
    test_3 = content[0:3]
    test_2 = content[0:2]
    test_1 = content[0:1]
    if (character_map[test_3] != 0):
        return True, test_3, 3
    elif (character_map[test_2] != 0):
        return True, test_2, 2
    elif (character_map[test_1] != 0):
        return True, test_1, 1
    # print repr(content[0])
    return False, '', 0

def parse_regex(content, token, character_map):
    '''
    Given a string representation of a programme, check whether it starts with
    a regular expression. If so, return the regular expression.
    '''
    regex_flag = set(['g', 'm', 'i', 'y', 'u', 's'])
    # print token
    if (content[0] == '/') and (content[1] != '>') and (token[1] != 'identifier') and (token[1] != 'number') and (token[2] != character_map[')']) and (token[2] != character_map[']']) and (token[2] != character_map['<']):
        regex = ''
        regex += content[0]
        square_brackets = 0
        slash_detector = False
        index = 1
        while index < len(content):
            # print content[index]
            regex += content[index]
            if ((content[index] == '/') and (square_brackets == 0) and (slash_detector == False) or ((content[index-1] == '/') and (content[index] in regex_flag))):
                break
            if (content[index] == '['):
                square_brackets += 1
            elif (content[index] == ']'):
                square_brackets -= 1
            if (content[index] == '\\') and (slash_detector == False):
                slash_detector = True
            else:
                slash_detector = False
            index += 1
        while (index < len(content) - 1) and (content[index+1] in regex_flag):
            regex += content[index+1]
            index += 1
        return True, regex, len(regex)
    return False, '', 0

# print parse_regex('/12234/', ('=', character_map['=']))
# print parse_regex('/12234/i', ('=', character_map['=']))
# print parse_regex('/^(?:(?:https?|mailto|ftp):|[^:/?#]*(?:[/?#]|$))/i', ('=', character_map['=']))
# print parse_regex('/8', (56, 'number'))

def string_to_number(number):
    '''
    Given a string representation of a number, return the number it represents
    '''
    index_dot = number.find('.')
    index_e = number.find('e')
    index_E = number.find('E')
    if (number[0] == '0') and (len(number) > 1) and (index_dot == -1):
        if (number[1] == 'x'):
            return hex(int(number, 16))
        elif (number[1] == 'b'):
            return bin(int(number, 0))
        else:
            return oct(int(number, 8))
    if (index_dot == -1) and (index_e == -1) and (index_E == -1):
        return int(number)
    elif (index_e == -1):
        try:
            return float(number)
        except ValueError:
            return number
    elif (index_E == -1):
        try:
            base = float(number[:index_e])
            power = int(number[index_e+1:])
            return base * (10 ** power)
        except ValueError:
            return number
    else:
        try:
            base = float(number[:index_E])
            power = int(number[index_E+1:])
            return base * (10 ** power)
        except ValueError:
            return number

# print string_to_number('.09543')

def lexical_processing(content_path, keyword_path, debug = False):
    '''
    Given a string representation of a programme, return a list of tokens in
    the form of <symbol, token number>. As currently we don't know how many
    numbers are we going to use, for some special cases we use strings to
    represent the token number
    '''
    content, keyword_set, escape_map, character_map = initialize(content_path, keyword_path)
    meaningless_value = set([' ', '\n', '\r', '\b', '\f', unichr(0x0009), '\xbb', '\xbf', '\xef'])
    i = 0
    content_length = len(content)
    token_list = []
    token_list.append(tuple([None, None, int(len(character_map.keys()) + 2)]))
    string_list = []
    while i < content_length:
        if (debug):
            print token_list[len(token_list)-1]
        if (content[i] in meaningless_value):
            i += 1
            continue
        flag1, comment, comment_length = parse_comment(content[i:])
        if (flag1):
            # print 'comment block detected', '------------------------------'
            # print comment
            # print comment_length
            if (comment_length == -1):
                raise Exception, 'Comment block not closed'
            i = i + comment_length
            continue
        flag2, string, index = parse_string(content[i:], escape_map)
        if (flag2):
            token_list.append(tuple([string, 'string', character_map['string']]))
            string_list.append(string)
            i = i + index
            # print string
            continue
        flag3, identifier, identifier_length = parse_identifier_keyword(content[i:])
        if (flag3):
            if (identifier in keyword_set):
                token_list.append(tuple([identifier, 'keyword', character_map[identifier]]))
                i = i + identifier_length
            else:
                token_list.append(tuple([identifier, 'identifier', character_map['identifier']]))
                i = i + identifier_length
            continue
        flag4, number, number_length= parse_number(content[i:])
        if (flag4):
            token_list.append(tuple([string_to_number(number), 'number', character_map['number']]))
            i = i + number_length
            continue
        flag5, regex, regex_length= parse_regex(content[i:], token_list[len(token_list)-1], character_map)
        if (flag5):
            # print 'Regular Expression Detected'
            token_list.append(tuple([regex, 'regular expression', character_map[regex]]))
            i = i + regex_length
            # print regex
            continue
        flag6, character, character_length= parse_character(content[i:], character_map)
        if (flag6):
            token_list.append(tuple([character, 'character', character_map[character]]))
            i = i + character_length
            continue
        token_list.append(tuple([content[i], 'invalid character', len(character_map.keys()) + 1]))
        i += 1
        # print repr(content[i:i+20])
        # raise Exception, 'Character Not Valid'
    token_list.pop(0)
    return token_list, character_map, string_list

# print lexical_processing('D:\\encrypted_obfuscated_Javascript_programme_analysis\\Virus\\0b8c85bb8a1624e8a5a2a64b412d91fe', 'D:\\encrypted_obfuscated_Javascript_programme_analysis\\JavaScriptKeywords.txt')
# Mode1Programmes = ['0a0e10988e66bffe2be4fb6d62760d73', '0a7b662dba064819a1e3c762fadb697b',
#                    '0a89e057b47001aa96cbb9b350913cbc', '0a0408ceb46f34f230e333557328d2fc',
#                    '0a6891b0e0e717445feb7d08c8e84b81', '0a74359f190c92a6c0f776034c08855a',
#                    '0aac8b7a77c8da292e612d63077d280c', '0aec8291a01f84dbd8ea186494937f6a',
#                    '00bd3cda5a94327755fb107b1af8a570', '0ce0f66bae012600e943a3d32638d58c',
#                    '0d7ab883292d9b0356bcc1a1246e7b1b', '0d9faee0c0b21b290bc33648ac0313ea',
#                    '0d45b6318f8d1b9dad2faa6b6703774f', '0d90839bd4c9bcb62795a8a1f20ce7bd',
#                    '0db0c7164e7f6a734957991166513539', '0db6dfe80b877e5598dadb487ffb986b']
# for programme in Mode1Programmes:
#     print programme, '-------------------------------------------'
#     programme_path = 'D:\encrypted_obfuscated_Javascript_programme_analysis\Virus\\' + programme
#     lexical_processing(programme_path, 'JavaScriptKeywords.txt')

# for root, dirs, files in os.walk('D:\\encrypted_obfuscated_Javascript_programme_analysis\\Virus'):
#     for file in files:
#         print file, '-----------------------------------------'
#         programme_path = 'D:\\encrypted_obfuscated_Javascript_programme_analysis\\Virus\\' + file
#         lexical_processing(programme_path, 'JavaScriptKeywords.txt')

# print lexical_processing('D:\\encrypted_obfuscated_Javascript_programme_analysis\\Virus\\js_4385.txt', 'JavaScriptKeywords.txt', True)[0]

# test_string = '\n\
# a'
# print repr(test_string)
#
# for i in range(0, len(test_string)):
#     print repr(test_string[i])
