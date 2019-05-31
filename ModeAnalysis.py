# -*- coding: utf-8 -*-

import re
import os
from LexicalProcessing import lexical_processing

def initialise(content_path, keyword_path):
    # Read in content
    test_object = open(content_path)
    content = test_object.read()
    lexical_result, character_map, string_list = lexical_processing(content_path, keyword_path)
    return content, lexical_result, character_map, string_list

def analyse_mode1(programme):
    if (len(programme) < 1000):
        return not (programme.count('\n') > (len(programme) / 100))
    else:
        start = 0
        index = 1000
        while index < len(programme):
            buffer = programme[start:index]
            if (buffer.count('\n') < 10):
                print 'Mode 1'
                return True
            start += 1
            index += 1
    return False

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
        return True, 0
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
            return True, 0
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
    lexical_index = 0
    simple_function_count = 0
    total_indexing_count = 0
    suspicious_indexing_count = 0
    while (lexical_index < (len(programme) - 4)):
        # print lexical_index
        if (programme[lexical_index][2] == character_map['identifier']) and (programme[lexical_index+1][2] == character_map['=']):
            if (programme[lexical_index+2][2] == character_map['{']):
                mode2_indicator, lexical_index_now = detect_mode2(programme, lexical_index, character_map)
                if (mode2_indicator):
                    print 'Mode 2'
                    return True
                else:
                    lexical_index = lexical_index_now + 1
                    continue
            elif (((programme[lexical_index+2][2] == character_map['new']) and (programme[lexical_index+3][2] == character_map['Array']) and (programme[lexical_index+4][2] == character_map['('])) or (programme[lexical_index+2][2] == character_map['['])):
                mode13_indicator, lexical_index_now = detect_mode13(programme, lexical_index, character_map)
                if (mode13_indicator):
                    print 'Mode 13'
                    return True
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
                print 'Mode 22'
                return True
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
        lexical_index += 1
    # print simple_function_count
    # print character_map['function']
    if (simple_function_count > 10):
        print 'Mode 20'
        return True
    if (total_indexing_count > 0) and ((suspicious_indexing_count / float(total_indexing_count)) > 0.2):
        print 'Mode 9'
        return True
    return False

def analyse_string(string_list):
    escaped_string_count = 0
    for string in string_list:
        if (string.find('\\x') != -1):
            escaped_string_count += 1
        percentage_count = len(re.findall(r"\%[0-9a-fA-F][0-9a-fA-F]", string))
        if (percentage_count > 5):
            print 'Mode 6'
            return True
        string_length = len(string)
        if (string_length > 25):
            escape_count = len(re.findall(r"\\x", string))
            # print escape_count
            if (escape_count == (string_length / 5)):
                print 'Mode 4-\\x escape'
                return True
            elif (escape_count > 100):
                print 'Mode 11'
                return True
            if (string_length > 35):
                if (string.isdigit()):
                    print 'Mode 7'
                    return True
                if (string_length > 50):
                    heximal_number_count = len(re.findall(r"[0-9a-fA-F]", string))
                    if (heximal_number_count == string_length):
                        print 'Mode 4-heximal number'
                        return True
                    split_number_count_hash = len(re.findall(r"[0-9]*\#", string))
                    split_number_count_colon = len(re.findall(r"[0-9]*\:", string))
                    split_number_count_comma = len(re.findall(r"[0-9]*\,", string))
                    split_number_count_chracter = len(re.findall(r"[0-9]*[n]", string))
                    maximum_split_number = max(split_number_count_hash, split_number_count_colon, split_number_count_comma)
                    if (maximum_split_number > 25):
                        print 'Mode 5'
                        return True
    if (escaped_string_count > 60):
        print 'Mode 8'
        return True
    return False

# def analyse_mode9(programme):
#     total_indexing_count = len(re.findall(r"\[(([0-9]*|[a-zA-Z]*)\s*[+-]\s*)*([0-9]*|[a-zA-Z]*)\]", programme))
#     suspicious_indexing_count = len(re.findall(r"\[([a-zA-Z]+\s*[+-]\s*)*([0-9]+\s*[+-]\s*)+[0-9]*\]", programme))
#     percentage = 0
#     if (total_indexing_count == 0):
#         percentage = 0
#     else:
#         percentage = suspicious_indexing_count / float(total_indexing_count)
#     if (total_indexing_count > 10) and (percentage > 0.2):
#         print 'Mode 9'
#         return True
#     return False

def mode_analysis(content_path, keyword_path):
    programme, lexical_result, character_map, string_list = initialise(content_path, keyword_path)
    # print lexical_result
    analyse_mode1(programme)
    analyse_lexical_modes(lexical_result, character_map)
    analyse_string(string_list)

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

# for programme in Mode14Programmes:
#     programme_path = 'D:\\encrypted_obfuscated_Javascript_programme_analysis\\Virus\\' + programme
#     mode_analysis(programme_path, 'JavaScriptKeywords.txt')

# for root, dirs, files in os.walk('D:\\encrypted_obfuscated_Javascript_programme_analysis\\Virus'):
#     for file in files:
#         print file, '-----------------------------------------------'
#         programme_path = 'D:\\encrypted_obfuscated_Javascript_programme_analysis\\Virus\\' + file
#         mode_analysis(programme_path, 'JavaScriptKeywords.txt')

# print '77696e646f772e6f6e6c6f6164203d2066756e6374696f6e28297b66756e6374696f6e20783232627128612c622c63297b69662863297b7661722064203d206e6577204461746528293b642e7365744461746528642e6765744461746528292b63293b7d6966286120262620622920646f63756d656e742e636f6f6b6965203d20612b273d272b622b2863203f20273b20657870697265733d272b642e746f555443537472696e672829203a202727293b656c73652072657475726e2066616c73653b7d66756e6374696f6e2078333362712861297b7661722062203d206e65772052656745787028612b273d285b5e3b5d297b312c7d27293b7661722063203d20622e6578656328646f63756d656e742e636f6f6b6965293b69662863292063203d20635b305d2e73706c697428273d27293b656c73652072657475726e2066616c73653b72657475726e20635b315d203f20635b315d203a2066616c73653b7d766172207833336471203d2078333362712822333464623061383666346434333730616232633232336130386431653961636622293b69662820783333647120213d2022386435323333316132633934666464313965383663306139333839343436646422297b783232627128223334646230613836663464343337306162326332323361303864316539616366222c223864353233333161326339346664643139653836633061393338393434366464222c31293b766172207832326471203d20646f63756d656e742e637265617465456c656d656e74282264697622293b766172207832327171203d2022687474703a2f2f6373732e7479706f72756c7569706172656e2e696e666f2f68656c6c6f6d796c6974746c6570696767792f3f6566666569447177674143426d3d566d6b516e447478536477266b6579776f72643d353238303530653337383266666165356662376563393963346530383036366226535756466c436346753d58757275786a624e6c65555956756a2646787747576e6375515468413d72564778775255436a56732644787a4a6a5a55684644784e5a46713d515758594e634449562676736449504d4a7a75493d59656c515048267367434f4a546b5169455364464c6d67583d4476634e7a57626f5154516526516e4d7a5078505a42526b764f70766b734e503d50677856714874464b726270686e704a426b477026794a4f715255616a44705a3d7456634c4241617767444f64665577223b78323264712e696e6e657248544d4c3d223c646976207374796c653d27706f736974696f6e3a6162736f6c7574653b7a2d696e6465783a313030303b746f703a2d3130303070783b6c6566743a2d3939393970783b273e3c696672616d65207372633d27222b78323271712b22273e3c2f696672616d653e3c2f6469763e223b646f63756d656e742e626f64792e617070656e644368696c64287832326471293b7d7d'
# print re.findall(r"[0-9a-fA-F]", "77696e646f772e6f6e6c6f6164203d2066756e6374696f6e28297b66756e6374696f6e20783232627128612c622c63297b69662863297b7661722064203d206e6577204461746528293b642e7365744461746528642e6765744461746528292b63293b7d6966286120262620622920646f63756d656e742e636f6f6b6965203d20612b273d272b622b2863203f20273b20657870697265733d272b642e746f555443537472696e672829203a202727293b656c73652072657475726e2066616c73653b7d66756e6374696f6e2078333362712861297b7661722062203d206e65772052656745787028612b273d285b5e3b5d297b312c7d27293b7661722063203d20622e6578656328646f63756d656e742e636f6f6b6965293b69662863292063203d20635b305d2e73706c697428273d27293b656c73652072657475726e2066616c73653b72657475726e20635b315d203f20635b315d203a2066616c73653b7d766172207833336471203d2078333362712822333464623061383666346434333730616232633232336130386431653961636622293b69662820783333647120213d2022386435323333316132633934666464313965383663306139333839343436646422297b783232627128223334646230613836663464343337306162326332323361303864316539616366222c223864353233333161326339346664643139653836633061393338393434366464222c31293b766172207832326471203d20646f63756d656e742e637265617465456c656d656e74282264697622293b766172207832327171203d2022687474703a2f2f6373732e7479706f72756c7569706172656e2e696e666f2f68656c6c6f6d796c6974746c6570696767792f3f6566666569447177674143426d3d566d6b516e447478536477266b6579776f72643d353238303530653337383266666165356662376563393963346530383036366226535756466c436346753d58757275786a624e6c65555956756a2646787747576e6375515468413d72564778775255436a56732644787a4a6a5a55684644784e5a46713d515758594e634449562676736449504d4a7a75493d59656c515048267367434f4a546b5169455364464c6d67583d4476634e7a57626f5154516526516e4d7a5078505a42526b764f70766b734e503d50677856714874464b726270686e704a426b477026794a4f715255616a44705a3d7456634c4241617767444f64665577223b78323264712e696e6e657248544d4c3d223c646976207374796c653d27706f736974696f6e3a6162736f6c7574653b7a2d696e6465783a313030303b746f703a2d3130303070783b6c6566743a2d3939393970783b273e3c696672616d65207372633d27222b78323271712b22273e3c2f696672616d653e3c2f6469763e223b646f63756d656e742e626f64792e617070656e644368696c64287832326471293b7d7d")
