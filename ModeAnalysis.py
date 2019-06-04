# -*- coding: utf-8 -*-

import re
import os
from collections import *
from LexicalProcessing import lexical_processing

def initialise(content_path, keyword_path):
    # Read in content
    test_object = open(content_path)
    content = test_object.read()
    lexical_result, character_map, string_list = lexical_processing(content_path, keyword_path)
    return content, lexical_result, character_map, string_list

def analyse_mode1(programme):
    if (len(programme) < 1000):
        if (programme.count('\n') > (len(programme) / 100)):
            return set([])
        else:
            return set(['Mode 1'])
    else:
        start = 0
        index = 1000
        while index < len(programme):
            buffer = programme[start:index]
            if (buffer.count('\n') < 10):
                return set(['Mode 1'])
            start += 1
            index += 1
    return set([])

def pair_detection(programme, lexical_index, character_map):
    '''
    This function detects whether there is a key-value pair in programme
    starting from lexical_index and return the length of the key-value pair.
    Currently it only supports key-value pair in the form of something + ":" +
    something.
    '''
    key_set = set([character_map['identifier'], character_map['string'], character_map['number']])
    # print key_set
    # print programme[lexical_index], programme[lexical_index+1], programme[lexical_index+2], programme[lexical_index+3]
    if (programme[lexical_index][2] in key_set) and (programme[lexical_index+1][2] == character_map[':']) and ((programme[lexical_index+3][2] == character_map[',']) or (programme[lexical_index+3][2] == character_map['}'])):
        return True, 3
    return False, 0

def simple_function_detection(programme, lexical_index, character_map):
    simple_function_indicator = True
    simple_function_indicator = simple_function_indicator and (programme[lexical_index+1][2] == character_map['identifier'])
    simple_function_indicator = simple_function_indicator and (programme[lexical_index+2][2] == character_map['('])
    simple_function_indicator = simple_function_indicator and (programme[lexical_index+3][2] == character_map[')'])
    simple_function_indicator = simple_function_indicator and (programme[lexical_index+4][2] == character_map['{'])
    simple_function_indicator = simple_function_indicator and (programme[lexical_index+5][2] == character_map['return'])
    if (simple_function_indicator):
        lexical_index_now = lexical_index + 6
        delimiter_stack = []
        while (True):
            if (programme[lexical_index_now][2] != character_map['}']) and (len(delimiter_stack) == 0):
                break
            if ((programme[lexical_index_now][2] == character_map['(']) or (programme[lexical_index_now][2] == character_map['{']) or (programme[lexical_index_now][2] == character_map['['])):
                delimiter_stack.append(programme[lexical_index_now][2])
                lexical_index_now += 1
                continue
            elif (len(delimiter_stack) > 0) and (programme[lexical_index_now][2] == (delimiter_stack[len(delimiter_stack)-1] + 1)):
                delimiter_stack.pop()
                lexical_index_now += 1
                continue
            lexical_index_now += 1
        return True, lexical_index_now + 1
    else:
        return False, 0

def human_readable_identifier_detection(identifier):
    alphabetical_count = 0
    vowel_count = 0
    upper_case_letter_count = 0
    repeat_storage1 = identifier[0]
    repeat_storage2 = ''
    total_score = 0
    string_length = len(identifier)
    if (string_length > 3):
        repeat_storage2 = identifier[1]
    vowel_set = set(['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'])
    exceptions_set = set(['str', 'substr', 'WScript', 'wfscr', 'css', 'html', 'xfbml', 'msg', 'src', 'js', 'rCRLF', 'tmp', 'http', 'wp', 'mng', 'FB', 'fb', 'my', 'scrl', 'xhr', 'jscr', 'fn', 'rts', 'rgb', 'chr', 'warn', 'vm', 'json', 'JSON', 'key', 'this', 'bst', 'spy', 'end', 'name'])
    for i in range(0, string_length):
        if (identifier[i].isalpha()):
            alphabetical_count += 1
        if (identifier[i] in vowel_set):
            vowel_count += 1
        if (identifier[i].isupper()):
            upper_case_letter_count += 1
        if (i > 2) and (identifier[i] == repeat_storage2) and (identifier[i] == repeat_storage1):
            total_score += 1
        repeat_storage1 = repeat_storage2
        repeat_storage2 = identifier[i]
    if (alphabetical_count < (string_length * 0.7)):
        total_score += 1
    if (vowel_count < (alphabetical_count * 0.1)) or (vowel_count > (alphabetical_count * 0.8)):
        total_score += 1
    if (upper_case_letter_count > (alphabetical_count * 0.5)) and (upper_case_letter_count < (alphabetical_count * 0.95)):
        total_score += 1
    # print total_score
    if ((total_score == 0) or (string_length == 1)):
        # print identifier
        return True
    else:
        for exception in exceptions_set:
            if (identifier.find(exception) != -1):
                return True
        print 'Variable not human readable', identifier
        return False

# human_readable_identifier_detection('X08yhffhg7xkxf')
# human_readable_identifier_detection('NCMCJKVczcCUyiV')
# human_readable_identifier_detection('rfhkryrz')
# human_readable_identifier_detection('bkrznnre')
# human_readable_identifier_detection('rwk')
# human_readable_identifier_detection('zkFgsm')
# human_readable_identifier_detection('RiDojs')
# human_readable_identifier_detection('pztgt')
# human_readable_identifier_detection('ibt')
# human_readable_identifier_detection('mwvjw')
# human_readable_identifier_detection('AC_AX_RunContent')
# human_readable_identifier_detection('uikb')
# human_readable_identifier_detection('xjkus')
# human_readable_identifier_detection('key_set')
# human_readable_identifier_detection('character_map')
# human_readable_identifier_detection('fromCharCode')
# human_readable_identifier_detection('logHuman')
# human_readable_identifier_detection('xhyrgs')


def detect_mode2(programme, lexical_index, character_map):
    lexical_index_now = lexical_index + 3
    key_value_pair = 0
    while (programme[lexical_index_now][2] != character_map['}']):
        if (programme[lexical_index_now][2] == character_map[',']):
            lexical_index_now += 1
            continue
        pair_indicator, pair_skip = pair_detection(programme, lexical_index_now, character_map)
        if (pair_indicator):
            key_value_pair += 1
            lexical_index_now += pair_skip
            continue
        else:
            # print programme[lexical_index], programme[lexical_index+1], programme[lexical_index+2]
            # raise Exception, 'Object literal parsing error'
            # Currently no working complete value recognition is
            # created, so we have to break out of the loop when other
            # value type is detected
            break
    if (key_value_pair > 50):
        return True, lexical_index_now
    return False, lexical_index_now

def detect_mode13(programme, lexical_index, character_map):
    lexical_index_now = lexical_index
    literal_definition = (programme[lexical_index_now+2][2] == character_map['new'])
    ending_character = ''
    if (literal_definition):
        lexical_index_now += 5
        ending_character = ')'
    else:
        lexical_index_now += 3
        ending_character = ']'
    element_count = 0
    delimiter_stack = []
    while ((lexical_index_now < len(programme)) and (programme[lexical_index_now][2] != character_map[ending_character]) or (len(delimiter_stack) != 0)):
        # print lexical_index
        # print programme[lexical_index]
        if (element_count > 50):
            return True, lexical_index_now
        if (len(delimiter_stack) == 0) and (programme[lexical_index_now][2] == character_map[',']):
            element_count += 1
            lexical_index_now += 1
            continue
        if ((programme[lexical_index_now][2] == character_map['(']) or (programme[lexical_index_now][2] == character_map['{']) or (programme[lexical_index_now][2] == character_map['['])):
            delimiter_stack.append(programme[lexical_index_now][2])
            lexical_index_now += 1
            continue
        elif (len(delimiter_stack) > 0) and (programme[lexical_index_now][2] == (delimiter_stack[len(delimiter_stack)-1] + 1)):
            delimiter_stack.pop()
            lexical_index_now += 1
            continue
        lexical_index_now += 1
    return False, lexical_index_now

def detect_mode22(programme, lexical_index, character_map):
    state_record = 0
    comma_record = 0
    lexical_index_now = lexical_index + 2
    while (programme[lexical_index_now][2] != character_map[')']):
        if (programme[lexical_index_now][2] == character_map['string']):
            if ((state_record == 0) or (state_record == 2)):
                state_record = 1
            else:
                return False, 0
        elif (programme[lexical_index_now][2] == character_map[',']):
            if (state_record == 1):
                comma_record += 1
                state_record = 2
            else:
                return False, 0
        lexical_index_now += 1
    if (programme[lexical_index_now+1][2] == character_map['+']) and (state_record == 1) and (comma_record > 0):
        return True, lexical_index_now + 1
    return False, 0

def detect_mode9(programme, lexical_index, character_map):
    lexical_index_now = lexical_index + 1
    state = 0
    expression_record = 0
    expression_character_set = set([character_map['+'], character_map['-']])
    while (programme[lexical_index_now][2] != character_map[']']):
        if (state == 0):
            if ((programme[lexical_index_now][2] == character_map['identifier']) or (programme[lexical_index_now][2] == character_map['number'])):
                state = 1
                expression_record += 1
                lexical_index_now += 1
                continue
            else:
                state = 3
                break
        elif (state == 1):
            if (programme[lexical_index_now][2] in expression_character_set):
                state = 2
                lexical_index_now += 1
                continue
            else:
                state = 3
                break
        elif (state == 2):
            if (programme[lexical_index_now][2] == character_map['number']):
                state = 1
                expression_record += 1
                lexical_index_now += 1
                continue
            else:
                state = 3
                break
    if (state == 3):
        return False, 0, 0
    else:
        # print expression_record
        if (expression_record > 1):
            return True, lexical_index_now, 2
        else:
            return True, lexical_index_now, 1


def analyse_lexical_modes(programme, character_map):
    lexical_modes = set([])
    lexical_index = 0
    simple_function_count = 0
    total_indexing_count = 0
    suspicious_indexing_count = 0
    total_identifier_count = 0
    not_readable_count = 0
    single_character_count = 0
    identifier_set = set([])
    while (lexical_index < (len(programme) - 4)):
        # print lexical_index
        if (programme[lexical_index][2] == character_map['identifier']) and (programme[lexical_index+1][2] == character_map['=']):
            if (programme[lexical_index+2][2] == character_map['{']):
                mode2_indicator, lexical_index_now = detect_mode2(programme, lexical_index, character_map)
                if (mode2_indicator):
                    lexical_modes.add('Mode 2')
                    lexical_index = lexical_index_now + 1
                    continue
                else:
                    lexical_index = lexical_index_now + 1
                    continue
            elif (((programme[lexical_index+2][2] == character_map['new']) and (programme[lexical_index+3][2] == character_map['Array']) and (programme[lexical_index+4][2] == character_map['('])) or (programme[lexical_index+2][2] == character_map['['])):
                mode13_indicator, lexical_index_now = detect_mode13(programme, lexical_index, character_map)
                if (mode13_indicator):
                    lexical_modes.add('Mode 13')
                    lexical_index = lexical_index_now + 1
                    continue
                else:
                    lexical_index = lexical_index_now + 1
                    continue
        elif (programme[lexical_index][2] == character_map['function']):
            # print 'Function detected'
            mode20_indicator, lexical_index_now = simple_function_detection(programme, lexical_index, character_map)
            if (mode20_indicator):
                simple_function_count += 1
                lexical_index = lexical_index_now + 1
                continue
            else:
                lexical_index += 1
                continue
        elif (programme[lexical_index][2] == character_map['+']) and (programme[lexical_index+1][2] == character_map['(']):
            mode22_indicator, lexical_index_now = detect_mode22(programme, lexical_index, character_map)
            if (mode22_indicator):
                lexical_modes.add('Mode 22')
                lexical_index = lexical_index_now + 1
                continue
            else:
                lexical_index += 1
                continue
        elif (programme[lexical_index][2] == character_map['[']):
            # print 'Possible indexing'
            mode9_indicator, lexical_index_now, type = detect_mode9(programme, lexical_index, character_map)
            if (mode9_indicator):
                # print 'Indexing detected'
                total_indexing_count += 1
                if (type == 2):
                    # print 'Suspicious indexing detected'
                    suspicious_indexing_count += 1
                lexical_index = lexical_index_now + 1
                continue
            else:
                lexical_index += 1
                continue
        elif (programme[lexical_index][2] == character_map['identifier']):
            if (len(programme[lexical_index][0]) == 1):
                single_character_count += 1
            if (not (programme[lexical_index][0] in identifier_set)) and (not (human_readable_identifier_detection(programme[lexical_index][0]))):
                not_readable_count += 1
            identifier_set.add(programme[lexical_index][0])
        lexical_index += 1
    # print simple_function_count
    # print character_map['function']
    if (simple_function_count > 10):
        lexical_modes.add('Mode 20')
    if (total_indexing_count > 0) and ((suspicious_indexing_count / float(total_indexing_count)) > 0.2):
        lexical_modes.add('Mode 9')
    if (not_readable_count > 3):
        lexical_modes.add('Mode 23')
    if (single_character_count > 50):
        lexical_modes.add('Mode 24')
    # print identifier_set
    return lexical_modes

# def analyse_string1(string_list):
#     escaped_string_count = 0
#     for string in string_list:
#         if (string.find('\\x') != -1):
#             escaped_string_count += 1
#         percentage_count = len(re.findall(r"\%[0-9a-fA-F][0-9a-fA-F]", string))
#         if (percentage_count > 5):
#             print 'Mode 6'
#             return True
#         string_length = len(string)
#         if (string_length > 25):
#             escape_count = len(re.findall(r"\\x", string))
#             # print escape_count
#             if (escape_count == (string_length / 5)):
#                 print 'Mode 4-\\x escape'
#                 return True
#             elif (escape_count > 100):
#                 print 'Mode 11'
#                 return True
#             if (string_length > 35):
#                 if (string.isdigit()):
#                     print 'Mode 7'
#                     return True
#                 if (string_length > 50):
#                     heximal_number_count = len(re.findall(r"[0-9a-fA-F]", string))
#                     if (heximal_number_count == string_length):
#                         print 'Mode 4-heximal number'
#                         return True
#                     split_number_count_hash = len(re.findall(r"[0-9]*\#", string))
#                     split_number_count_colon = len(re.findall(r"[0-9]*\:", string))
#                     split_number_count_comma = len(re.findall(r"[0-9]*\,", string))
#                     split_number_count_chracter = len(re.findall(r"[0-9]*[n]", string))
#                     maximum_split_number = max(split_number_count_hash, split_number_count_colon, split_number_count_comma)
#                     if (maximum_split_number > 25):
#                         print 'Mode 5'
#                         return True
#     if (escaped_string_count > 60):
#         print 'Mode 8'
#         return True
#     return False

def analyse_string(string_list):
    string_modes = set([])
    escaped_string_count = 0
    string_list_length = len(string_list)
    for string in string_list:
        string_length = len(string)
        escape_count = 0
        digit_count = 0
        hex_digit_count = 0
        percentage_count = 0
        character_count = defaultdict(int)
        for i in range(0, string_length):
            character_count[string[i]] += 1
            if (i < string_length - 2) and (string[i] == '\\') and (string[i+1] == 'x'):
                escaped_string_count += 1
                escape_count += 1
            if (string[i].isdigit()):
                digit_count += 1
            if (((ord(string[i]) > 96) and (ord(string[i]) < 103)) or ((ord(string[i]) > 64) and (ord(string[i]) < 71))):
                hex_digit_count += 1
            if (i < string_length - 3) and (string[i] == '%') and (string[i+1].isdigit()) and (string[i+2].isdigit()):
                percentage_count += 1
        if (percentage_count > 5):
            string_modes.add('Mode 6')
        if (string_length > 25) and (escape_count == (string_length / 5)):
            string_modes.add('Mode 4-\\x escape')
        if (escape_count > 100):
            string_modes.add('Mode 11')
        if (string_length > 35) and (digit_count == string_length):
            string_modes.add('Mode 7')
        if (string_length > 50) and ((digit_count + hex_digit_count) == string_length):
            string_modes.add('Mode 4-heximal number')
        if (string_length > 500):
            for character in character_count.keys():
                if (character_count[character] > (string_length / 4)):
                    string_modes.add('Mode 5')
    if (escaped_string_count > 60):
        string_modes.add('Mode 8')
    return string_modes

def mode_analysis(content_path, keyword_path):
    detected_modes = set([])
    programme, lexical_result, character_map, string_list = initialise(content_path, keyword_path)
    # print lexical_result
    # detected_modes |= analyse_mode1(programme)
    detected_modes |= analyse_lexical_modes(lexical_result, character_map)
    # detected_modes |= analyse_string(string_list)
    return detected_modes

# print ('aaaaasdfaew\naabc\naa'.count('\n'))
Mode1Programmes = ['0a0e10988e66bffe2be4fb6d62760d73', '0a7b662dba064819a1e3c762fadb697b',
                   '0a89e057b47001aa96cbb9b350913cbc', '0a0408ceb46f34f230e333557328d2fc',
                   '0a6891b0e0e717445feb7d08c8e84b81', '0a74359f190c92a6c0f776034c08855a',
                   '0aac8b7a77c8da292e612d63077d280c', '0aec8291a01f84dbd8ea186494937f6a',
                   '00bd3cda5a94327755fb107b1af8a570', '0ce0f66bae012600e943a3d32638d58c',
                   '0d7ab883292d9b0356bcc1a1246e7b1b', '0d9faee0c0b21b290bc33648ac0313ea',
                   '0d45b6318f8d1b9dad2faa6b6703774f', '0d90839bd4c9bcb62795a8a1f20ce7bd',
                   '0db0c7164e7f6a734957991166513539', '0db6dfe80b877e5598dadb487ffb986b']

Mode2Programmes = ['0a0e10988e66bffe2be4fb6d62760d73','0a6891b0e0e717445feb7d08c8e84b81']

Mode4Programmes = ['0a2cde294b9ca35da02aa4f1f405f890','0c935f8a039dc1e294822cfd0bc8031d',
'00cf3db1b71970e6847a70a6f4ff8a77','0d6ad8c36ced8b3baa0315eabc3a0b3c',
'0db02a3e6bf6d3ea41837efa316ee05b','0db3b56c858994234127dbb8ab373318']

Mode5Programmes = ['0a05f424b1908af2557d516b10c62a21','0a6fd674b29ae6f398e8ab220db5f728',
'0a8efb49e9b76de51615c4580d8a6f1f','0a8f13c992f57bd9f10b4c1ae2b69088',
'0a22a4f7c703b3207c7d47bd83e1a6e3','0a064e49f8f7404d78b0559679b93e2e',
'0a731d9f2d3f4a7981cceefe6ecd133e','0a89272d23e4a8f38cfcc18ade36ade4',
'0a98070c857158bd59ba7aeb03276657','0ab3d18999ef455a232b69c36673efec',
'0ac73533cabb6a56173ff2d06f22937d','0ad3edee1d7589fb0ac121d7cfb3eefe',
'0ad6b8069639e1e3389f8537443b9e8f','0ae2c1ed6e3081ad8362aab8bde81365',
'0b1c60c722af1bb363a6f7d850a4dd88','0b2a23dc4434d7b14f2aa63311ea304e',
'0b3d83caf5eca204dbcde7b688be87dd','0b3d83caf5eca204dbcde7b688be87dd',
'0b19fe6decd393343f63940be2751cd8','0b41c445b47fdeb69089c6122607703b',
'0b455aa47882535d58c1fd658e67938e','0b639cd4b4ea70d3435f88819b3f7fc7',
'0b3084e6e70af11b34c137cc1a778714','0b32249ea2f89944f2d018c905328ce6',
'0b53337f93039f1bf4573e83cc5a14a7','00b5520907d65113bbded4243f115c3b',
'0bb15ebf23e4ddd72f83baa1dfd9ef8d','0be4f2317ba0413409f044c473b03dd8',
'0be9164444acd043f579b1e717130683','0bf2ad82818d3fb88ce9b597836e399f',
'0c1d820178887bc91e0fa8f92464c7d5','0c2dec535aa08e66895bb457892b3ea6',
'0c2f3756f570c68e8aa0d385f6dd7aa0','0c4f61aebf1f17fe357d83121a6b98de',
'0c7c3179743e4e26343770f5d6220828','0c17e38301683d5729b0251e7490450f',
'0c81abb723826cbf63cbabe2d9cc70ea','0c152ca996a9b276486682d446ae53b1',
'00c313e315a3af55b1dfa3c672962710','0c1869a7dfba3f1cc31c9290b4ab13de',
'0c2790d4a6dbda97307f7e378d1527f4','0c37459c939e29944f52e667180a713a',
'0cab24403eab1aa9bf8de060cb88a832','0cad7a177ab5931cdc4a63c959e41598',
'0d0fb3fa7b08ca2cf5dbebdc2fee82a1','0d1d63a86e3a1da7b6d56d720b91496a',
'0d5c36be7f5a722a758f3a6d8360ea1e','0cac3fb2d0f5fd38f1e53263163d95e2',
'00d6d12b78db6dd9467060df94fc308c','0d8ff59b25c90e835a3406c9af5bc87f',
'0d9f72e8f51c760e99bea89ded22bf4c','0d47f2c51f97bf58e0ed4f1cc4fae52a',
'0d58dc62c6886c13d749db53cce69c46','0d55283262ac89d37fd34bb3eb746c68',
'00da63a10066ca0eea605e3fad3b231d','0db6dfe80b877e5598dadb487ffb986b',
'00dd1c07fb998137da41a3adfdc1c8d4']

Mode6Programmes = ['0a6edb058be48ffa9c730a81f6a03d8f','0a3679d658f853b79770058ef4a86c31',
'0ad0f4a357e3fde1e2be90fdba9ebcd1','0d3c2276663f0cf19f276c6b8ce2dab4']

Mode7Programmes = ['00a21bb3c5f44c95c5cfaf4cde64af14','0aeebe748a3bb812a708e866de88a650',
'0cb83cc2ca346a4c49bb49e20afa6e5b','0d1f2c541fb1a80328829148828c53e8',
'0d152f86f63d0677596260509fcb8ce0']

Mode8Programmes = ['0a85cf2e69232ab5bb8dcef24171ac9a','0a74359f190c92a6c0f776034c08855a']

Mode11Programmes = ['0b8c85bb8a1624e8a5a2a64b412d91fe','0bd03d0ce78d61a874f8890e15c20d04',
'0ceea2d3162b9f7584240b77692b65dd','0d5c51ef8d41a3b5f334d108a25db3f0']

Mode9Programmes = ['0a26124a3790fd438183d8d968043c60','0bc299985821ed7cf9cbc5b50dc7a18d',
'0c6d8c0c04f5af57ea7ad7ff07457f32']

Mode13Programmes = ['0b40593f1d2dd27a1d25830c6918f7d2','0c8ebff9d1172e502414fb2d419df316']

Mode20Programmes = ['0db02a3e6bf6d3ea41837efa316ee05b']

Mode16Programmes = ['0d0f8c58b0ad357b0510e0da264afb7d']

Mode14Programmes = ['0bc595a9d7c77fea81d355cfac04cf28','00bd3cda5a94327755fb107b1af8a570',
'0d0f8c58b0ad357b0510e0da264afb7d']

# for programme in Mode9Programmes:
#     programme_path = 'D:\\encrypted_obfuscated_Javascript_programme_analysis\\Virus\\' + programme
#     mode_analysis(programme_path, 'JavaScriptKeywords.txt')

# error_count = 0
# for root, dirs, files in os.walk('D:\\encrypted_obfuscated_Javascript_programme_analysis\\NormalProgrammes'):
#     for file in files:
#         print file, '-----------------------------------------------'
#         programme_path = 'D:\\encrypted_obfuscated_Javascript_programme_analysis\\NormalProgrammes\\' + file
#         if ('Mode 23' in mode_analysis(programme_path, 'JavaScriptKeywords.txt')):
#             error_count += 1
#             print 'Random variable name detected in', file, '-----------------'
#         else:
#             print 'Normal', file
# print error_count
