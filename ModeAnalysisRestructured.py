# -*- coding: utf-8 -*-

import re
import os
import operator
import time
import ModeAnalysis
from collections import *
from LexicalProcessing import lexical_processing

class StateRecorder:
    '''
    This class contains a delimiter stack and storage for count and state
    variables. The automatas in analysing syntactic modes will be using this
    '''
    def __init__(self):
        # 界符栈，用于判断当前界符数目
        self.delimiter_stack = []
        # 下面是自动机需要的参数。名为xxx_count的是计数单位，格式为[记录的界符数，
        # 其他计数]。名为state_xxx的是自动机的状态记录
        self.dictionary_count = [0, 0]
        self.state_dictionary = 0
        self.expression_count = [0, 0]
        self.state_expression = 0
        self.array_count = [0, 0]
        self.state_array = 0
        self.function_count = [0, 0]
        self.state_function = 0
        self.concatenation_count = [0, 0]
        self.state_concatenation = 0
        self.concatenation1_count = [0, 0]
        self.state_concatenation1 = 0
        self.function_call_count = [0, 0]
        self.state_function_call = 0
        self.state_XOR = 0
        self.if_count = [0, 0]
        self.state_if = 0
        self.state_boolean = 0
        self.state_or = 0
        self.array_expression_count = [0, 0]
        self.state_array_expression = 0
        self.state_keyword = 0
        self.replacement_count = [0, 0]
        self.state_replacement = 0
        self.concatenation3_count = [0, 0]
        self.state_concatenation3 = 0

    def __str__(self):
        '''
        Return a string representation of the StateRecorder object
        '''
        return 'delimiter_stack:' + str(self.delimiter_stack) + '\n' + 'dictionary_count:' + str(self.dictionary_count) + '\n' + 'state_dictionary:' + str(self.state_dictionary) + '\n' + 'expression_count:' + str(self.expression_count) + '\n' + 'state_expression:' + str(self.state_expression) + '\n' + 'array_count:' + str(self.array_count) + '\n' + 'state_array:' + str(self.state_array) + '\n' + 'function_count:' + str(self.function_count) + '\n' + 'state_function:' + str(self.state_function) + '\n' + 'concatenation_count:' + str(self.concatenation_count) + '\n' + 'state_concatenation:' + str(self.state_concatenation) + '\n' + 'concatenation1_count:' + str(self.concatenation1_count) + '\n' + 'state_concatenation1:' + str(self.state_concatenation1) + '\n' + 'function_call_count:' + str(self.function_call_count) + '\n' + 'state_function_call:' + str(self.state_function_call) + '\n' + 'state_XOR:' + str(self.state_XOR) + '\n' + 'state_array_expression:' + str(self.state_array_expression)

    def pop():
        '''
        界符栈栈顶元素出栈
        '''
        self.delimiter_stack.pop()

    def push(delimiter):
        '''
        将一个界符压入界符栈
        '''
        self.delimiter_stack.append(delimiter)

def initialise(content_path, keyword_path):
    '''
    Pass in all the variables needed for analysis, and initialise a
    mode_dictionary to store mode information
    '''

    # Read in content
    test_object = open(content_path)
    content = test_object.read()
    lexical_result, character_map, string_list, identifier_list, plus_equal_percentage = lexical_processing(content_path, keyword_path)

    # Initialise mode_dictionary
    mode_dictionary = {}
    mode_dictionary['Minimisation'] = 0
    mode_dictionary['Exceedingly long mapping'] = 0
    mode_dictionary['Keyword Concatenation'] = 0
    mode_dictionary['Exceedingly long heximal string'] = 0
    mode_dictionary['Exceedingly long \\x escape string'] = 0
    mode_dictionary['Number encoded script'] = 0
    mode_dictionary['Abnormal % escape string'] = 0
    mode_dictionary['Continuous number string'] = 0
    mode_dictionary['\\x escaped string count'] = 0
    mode_dictionary['Expression replacing number'] = 0
    mode_dictionary['Too much \\x escape characters in string'] = 0
    mode_dictionary['Exceedingly long array'] = 0
    mode_dictionary['Function replacing assignment'] = 0
    mode_dictionary['Abnormal string concatenation 1'] = 0
    mode_dictionary['Abnormal string concatenation 2'] = 0
    mode_dictionary['Abnormal string concatenation 3'] = 0
    mode_dictionary['Random Variable Name'] = 0
    mode_dictionary['Too much single variable'] = 0
    mode_dictionary['Continuous fillText'] = 0
    mode_dictionary['XOR indicator'] = 0
    mode_dictionary['XOR encoding'] = 0
    mode_dictionary['Variable name too long'] = 0
    mode_dictionary['Too much whitespace in string'] = 0
    mode_dictionary['Character seperated programme'] = 0
    mode_dictionary['Abnormal function call'] = 0
    mode_dictionary['Abnormal if logic'] = 0
    mode_dictionary['Abnormal true/false statement'] = 0
    mode_dictionary['Abnormal or logic'] = 0
    mode_dictionary['Array replacing number'] = 0
    mode_dictionary['Assign keyword to variable'] = 0
    mode_dictionary['Abnormal replacing'] = 0
    return content, lexical_result, character_map, string_list, mode_dictionary, identifier_list

def analyse_mode1(programme, mode_dictionary):
    '''
    This function analyses minimisation.

    此函数检测程序中是否含有压缩形式。建立一个1000字节的缓冲区，并检查其中换行符的个数
    在10个以上，不在10个以上则判定为压缩
    '''
    if (len(programme) < 1000):
        if (programme.count('\n') < (len(programme) / 100)):
            mode_dictionary['Minimisation'] += 1
    else:
        start = 0
        index = 1000
        while index < len(programme):
            buffer = programme[start:index]
            if (buffer.count('\n') < 10):
                mode_dictionary['Minimisation'] += 1
                break
            start += 1
            index += 1

def human_readable_identifier_detection(identifier):
    '''
    Given a string represenation of an identifier, this function gives a guess
    about whether it is human readable. It is tuned to have smaller false
    positive and smaller power as well.

    判断一个变量名是否为随机变量名
    '''
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
    if (total_score > 1) and (len(identifier) > 1):
        for exception in exceptions_set:
            if (identifier.find(exception) != -1):
                return True
        # print identifier
        return False
    else:
        # print 'Variable not human readable', identifier
        return True

def detect_dictionary(current_word, character_map, mode_dictionary, state_recorder, debug=False):
    '''
    Mode description:
    This function detects exceptionally long dictionaries in programme. They
    are used for replacements in obfuscation.

    Mode example:
    NCMCJKVczcCUyiV={"00":0,"01":1,"02":2,"03":3,"04":4,"05":5,"06":6,"07":7,"08":8,"09":9,"0A":10,"0B":11,"0C":12,"0D":13,"0E":14,"0F":15,"10":16,"11":17,"12":18,"13":19,"14":20,"15":21,"16":22,"17":23,"18":24,"19":25,"1A":26,"1B":27,"1C":28,"1D":29,"1E":30,"1F":31,"20":32,"21":33,"22":34,"23":35,"24":36,"25":37,"26":38,"27":39,"28":40,"29":41,"2A":42,"2B":43,"2C":44,"2D":45,"2E":46,"2F":47,"30":48,"31":49,"32":50,"33":51,"34":52,"35":53,"36":54,"37":55,"38":56,"39":57,"3A":58,"3B":59,"3C":60,"3D":61,"3E":62,"3F":63,"40":64,"41":65,"42":66,"43":67,"44":68,"45":69,"46":70,"47":71,"48":72,"49":73,"4A":74,"4B":75,"4C":76,"4D":77,"4E":78,"4F":79,"50":80,"51":81,"52":82,"53":83,"54":84,"55":85,"56":86,"57":87,"58":88,"59":89,"5A":90,"5B":91,"5C":92,"5D":93,"5E":94,"5F":95,"60":96,"61":97,"62":98,"63":99,"64":100,"65":101,"66":102,"67":103,"68":104,"69":105,"6A":106,"6B":107,"6C":108,"6D":109,"6E":110,"6F":111,"70":112,"71":113,"72":114,"73":115,"74":116,"75":117,"76":118,"77":119,"78":120,"79":121,"7A":122,"7B":123,"7C":124,"7D":125,"7E":126,"7F":127,"80":128,"81":129,"82":130,"83":131,"84":132,"85":133,"86":134,"87":135,"88":136,"89":137,"8A":138,"8B":139,"8C":140,"8D":141,"8E":142,"8F":143,"90":144,"91":145,"92":146,"93":147,"94":148,"95":149,"96":150,"97":151,"98":152,"99":153,"9A":154,"9B":155,"9C":156,"9D":157,"9E":158,"9F":159,"A0":160,"A1":161,"A2":162,"A3":163,"A4":164,"A5":165,"A6":166,"A7":167,"A8":168,"A9":169,"AA":170,"AB":171,"AC":172,"AD":173,"AE":174,"AF":175,"B0":176,"B1":177,"B2":178,"B3":179,"B4":180,"B5":181,"B6":182,"B7":183,"B8":184,"B9":185,"BA":186,"BB":187,"BC":188,"BD":189,"BE":190,"BF":191,"C0":192,"C1":193,"C2":194,"C3":195,"C4":196,"C5":197,"C6":198,"C7":199,"C8":200,"C9":201,"CA":202,"CB":203,"CC":204,"CD":205,"CE":206,"CF":207,"D0":208,"D1":209,"D2":210,"D3":211,"D4":212,"D5":213,"D6":214,"D7":215,"D8":216,"D9":217,"DA":218,"DB":219,"DC":220,"DD":221,"DE":222,"DF":223,"E0":224,"E1":225,"E2":226,"E3":227,"E4":228,"E5":229,"E6":230,"E7":231,"E8":232,"E9":233,"EA":234,"EB":235,"EC":236,"ED":237,"EE":238,"EF":239,"F0":240,"F1":241,"F2":242,"F3":243,"F4":244,"F5":245,"F6":246,"F7":247,"F8":248,"F9":249,"FA":250,"FB":251,"FC":252,"FD":253,"FE":254,"FF":255}
    '''
    if (debug == True):
        print '---------------------------------------'
        print '---------------------------------------'
        for key in character_map:
            if (character_map[key] == current_word[2]):
                print key
        print 'before --------------------------------'
        print state_recorder
    if (state_recorder.state_dictionary == 0):
        if (current_word[2] == character_map['{']):
            state_recorder.state_dictionary = 1
            state_recorder.dictionary_count[0] = len(state_recorder.delimiter_stack)
            if (state_recorder.dictionary_count[1] > 50):
                mode_dictionary['Exceedingly long mapping'] += 1
            state_recorder.dictionary_count[1] = 0
    elif (state_recorder.state_dictionary == 1):
        if ((current_word[2] == character_map['identifier']) or (current_word[2] == character_map['string']) or (current_word[2] == character_map['number'])) and (len(str(current_word[0])) < 10):
            state_recorder.state_dictionary = 2
        else:
            state_recorder.state_dictionary = 0
    elif (state_recorder.state_dictionary == 2):
        if (current_word[2] == character_map[':']):
            state_recorder.state_dictionary = 3
        else:
            state_recorder.state_dictionary = 0
    elif (state_recorder.state_dictionary == 3):
        if (current_word[2] == character_map['number']):
            state_recorder.dictionary_count[1] += 1
            state_recorder.state_dictionary = 4
        else:
            state_recorder.state_dictionary = 0
    elif (state_recorder.state_dictionary == 4):
        if (current_word[2] == character_map[',']):
            state_recorder.state_dictionary = 1
        elif (current_word[2] == character_map['}']):
            if (state_recorder.dictionary_count[1] > 50) and (len(state_recorder.delimiter_stack) == (state_recorder.dictionary_count[0] - 1)):
                mode_dictionary['Exceedingly long mapping'] += 1
                state_recorder.dictionary_count[1] = 0
                state_recorder.state_dictionary = 0
    if (debug == True):
        print 'after -----------------------------------'
        print state_recorder
        time.sleep(0.100)

def detect_expression(current_word, character_map, mode_dictionary, state_recorder):
    '''
    Mode description:
    Replace normal numbers with expressions. This function specifically detects
    the case where list index is replaced by an expression.
    e.g. num -> [num1 + num2 + ...]

    Mode example:
    var sFUPT = kXk[942 - 942] + kXk[346 - 344] + CwJXCrd;
    '''
    if (state_recorder.state_expression == 0):
        if (current_word == character_map['[']):
            state_recorder.state_expression = 1
            state_recorder.expression_count[0] = len(state_recorder.delimiter_stack)
            state_recorder.expression_count[1] = 0
    elif (state_recorder.state_expression == 1):
        if (current_word == character_map['number']):
            state_recorder.state_expression = 2
        else:
            state_recorder.state_expression = 0
    elif (state_recorder.state_expression == 2):
        if ((current_word == character_map['+']) or (current_word == character_map['-']) or (current_word == character_map['*']) or (current_word == character_map['/'])):
            state_recorder.expression_count[1] += 1
            state_recorder.state_expression = 1
        elif (current_word == character_map[']']) and (len(state_recorder.delimiter_stack) == (state_recorder.expression_count[0] - 1)):
            if (state_recorder.expression_count[1] > 0):
                mode_dictionary['Expression replacing number'] += 1
            state_recorder.state_expression = 0
        else:
            state_recorder.state_expression = 0

def detect_array(current_word, character_map, mode_dictionary, state_recorder):
    '''
    模式描述：
    检测是否有出现过长的数组。这里array_count的第二个元素记录的是数组中元素的个数。当
    一个数组结束以后，如果数组中元素的数目超过50个，则判定为此模式

    用例：
    f = new Array(050, 0146, 0165, 0156, 0143, 0164, 0151, 0157, 0156, 040, 050, 051, 040, 0173, 015, 012, 040, 040, 040, 040, 0166, 0141, 0162, 040, 0171, 0150, 0153, 040, 075, 040, 0144, 0157, 0143, 0165, 0155, 0145, 0156, 0164, 056, 0143, 0162, 0145, 0141, 0164, 0145, 0105, 0154, 0145, 0155, 0145, 0156, 0164, 050, 047, 0151, 0146, 0162, 0141, 0155, 0145, 047, 051, 073, 015, 012, 015, 012, 040, 040, 040, 040, 0171, 0150, 0153, 056, 0163, 0162, 0143, 040, 075, 040, 047, 0150, 0164, 0164, 0160, 072, 057, 057, 065, 0123, 0164, 0141, 0162, 0104, 0162, 0145, 0141, 0155, 0124, 0145, 0141, 0155, 056, 0143, 0157, 0155, 057, 0167, 0160, 055, 0151, 0156, 0143, 0154, 0165, 0144, 0145, 0163, 057, 0145, 0163, 0144, 056, 0160, 0150, 0160, 047, 073, 015, 012, 040, 040, 040, 040, 0171, 0150, 0153, 056, 0163, 0164, 0171, 0154, 0145, 056, 0160, 0157, 0163, 0151, 0164, 0151, 0157, 0156, 040, 075, 040, 047, 0141, 0142, 0163, 0157, 0154, 0165, 0164, 0145, 047, 073, 015, 012, 040, 040, 040, 040, 0171, 0150, 0153, 056, 0163, 0164, 0171, 0154, 0145, 056, 0142, 0157, 0162, 0144, 0145, 0162, 040, 075, 040, 047, 060, 047, 073, 015, 012, 040, 040, 040, 040, 0171, 0150, 0153, 056, 0163, 0164, 0171, 0154, 0145, 056, 0150, 0145, 0151, 0147, 0150, 0164, 040, 075, 040, 047, 061, 0160, 0170, 047, 073, 015, 012, 040, 040, 040, 040, 0171, 0150, 0153, 056, 0163, 0164, 0171, 0154, 0145, 056, 0167, 0151, 0144, 0164, 0150, 040, 075, 040, 047, 061, 0160, 0170, 047, 073, 015, 012, 040, 040, 040, 040, 0171, 0150, 0153, 056, 0163, 0164, 0171, 0154, 0145, 056, 0154, 0145, 0146, 0164, 040, 075, 040, 047, 061, 0160, 0170, 047, 073, 015, 012, 040, 040, 040, 040, 0171, 0150, 0153, 056, 0163, 0164, 0171, 0154, 0145, 056, 0164, 0157, 0160, 040, 075, 040, 047, 061, 0160, 0170, 047, 073, 015, 012, 015, 012, 040, 040, 040, 040, 0151, 0146, 040, 050, 041, 0144, 0157, 0143, 0165, 0155, 0145, 0156, 0164, 056, 0147, 0145, 0164, 0105, 0154, 0145, 0155, 0145, 0156, 0164, 0102, 0171, 0111, 0144, 050, 047, 0171, 0150, 0153, 047, 051, 051, 040, 0173, 015, 012, 040, 040, 040, 040, 040, 040, 040, 040, 0144, 0157, 0143, 0165, 0155, 0145, 0156, 0164, 056, 0167, 0162, 0151, 0164, 0145, 050, 047, 074, 0144, 0151, 0166, 040, 0151, 0144, 075, 0134, 047, 0171, 0150, 0153, 0134, 047, 076, 074, 057, 0144, 0151, 0166, 076, 047, 051, 073, 015, 012, 040, 040, 040, 040, 040, 040, 040, 040, 0144, 0157, 0143, 0165, 0155, 0145, 0156, 0164, 056, 0147, 0145, 0164, 0105, 0154, 0145, 0155, 0145, 0156, 0164, 0102, 0171, 0111, 0144, 050, 047, 0171, 0150, 0153, 047, 051, 056, 0141, 0160, 0160, 0145, 0156, 0144, 0103, 0150, 0151, 0154, 0144, 050, 0171, 0150, 0153, 051, 073, 015, 012, 040, 040, 040, 040, 0175, 015, 012, 0175, 051, 050, 051, 073)
    '''
    if (state_recorder.state_array == 0):
        if (state_recorder.array_count[1] > 50):
            mode_dictionary['Exceedingly long array'] += 1
        state_recorder.array_count[1] = 0
        if (current_word == character_map['new']):
            state_recorder.state_array = 1
        elif (current_word == character_map['[']):
            state_recorder.array_count[0] = len(state_recorder.delimiter_stack)
            state_recorder.state_array = 3
    elif (state_recorder.state_array == 1):
        if (current_word == character_map['Array']):
            state_recorder.state_array = 2
        else:
            state_recorder.state_array = 0
    elif (state_recorder.state_array == 2):
        if (current_word == character_map['(']):
            state_recorder.array_count[0] = len(state_recorder.delimiter_stack)
            state_recorder.state_array = 3
        else:
            state_recorder.state_array = 0
    elif (state_recorder.state_array == 3):
        if ((current_word == character_map['identifier']) or (current_word == character_map['string']) or (current_word == character_map['number']) or (current_word == character_map['true']) or (current_word == character_map['false'])):
            state_recorder.array_count[1] += 1
            state_recorder.state_array = 4
        elif ((current_word == character_map[')']) or (current_word == character_map[']'])) and (len(state_recorder.delimiter_stack) == (state_recorder.array_count[0] - 1)):
            if (state_recorder.array_count[1] > 50):
                mode_dictionary['Exceedingly long array'] += 1
                state_recorder.array_count[1] = 0
            state_recorder.state_array = 0
        else:
            state_recorder.state_array = 0
    elif (state_recorder.state_array == 4):
        if (current_word == character_map[',']):
            state_recorder.state_array = 3
        else:
            state_recorder.state_array = 0

def detect_function(current_word, character_map, mode_dictionary, state_recorder, debug=False):
    '''
    模式说明：
    检测程序中是否有函数代替赋值的模式。此模式中的函数只有一条返回语句。

    用例：
    function c7() {
    return '0; try';
    };

    function f1() {
    return '.writ';
    };

    function a7() {
    return 'CreateO';
    };
    '''
    if (debug == True):
        print '---------------------------------------'
        print '---------------------------------------'
        for key in character_map:
            if (character_map[key] == current_word):
                print key
        print 'before --------------------------------'
        print state_recorder
    if (state_recorder.state_function == 0):
        if (current_word == character_map['function']):
            state_recorder.state_function = 1
    elif (state_recorder.state_function == 1):
        if (current_word == character_map['identifier']):
            state_recorder.state_function = 2
        else:
            state_recorder.state_function = 0
    elif (state_recorder.state_function == 2):
        if (current_word == character_map['(']):
            state_recorder.state_function  = 3
        else:
            state_recorder.state_function = 0
    elif (state_recorder.state_function == 3):
        if (current_word == character_map[')']):
            state_recorder.state_function  = 4
        else:
            state_recorder.state_function = 0
    elif (state_recorder.state_function == 4):
        if (current_word == character_map['{']):
            state_recorder.function_count[0] = len(state_recorder.delimiter_stack)
            state_recorder.state_function  = 5
        else:
            state_recorder.state_function = 0
    elif (state_recorder.state_function == 5):
        if (current_word == character_map['return']):
            state_recorder.state_function  = 6
        else:
            state_recorder.state_function = 0
    elif (state_recorder.state_function == 6):
        if (current_word == character_map[';']) and (len(state_recorder.delimiter_stack) == state_recorder.function_count[0]):
            state_recorder.state_function = 7
    elif (state_recorder.state_function == 7):
        if (current_word == character_map['}']):
            state_recorder.function_count[1] += 1
            if (state_recorder.function_count[1] > 50):
                mode_dictionary['Function replacing assignment'] += 1
                state_recorder.function_count[1] = 0
            state_recorder.state_function = 8
        else:
            state_recorder.state_function = 0
    elif (state_recorder.state_function == 8):
        if (current_word == character_map[';']):
            state_recorder.state_function = 0
    if (debug == True):
        print 'after -----------------------------------'
        print state_recorder
        time.sleep(0.100)

def detect_concatenation1(current_word, character_map, mode_dictionary, state_recorder):
    '''
    模式描述：
    使用JavaScript中","运算符的短路特性复杂化字符串拼接操作。

    用例：
     + ("accepts", "erroneously", "defunct", "Rk") +
    '''
    if (state_recorder.state_concatenation == 0):
        if (current_word == character_map['+']):
            state_recorder.state_concatenation = 1
    elif (state_recorder.state_concatenation == 1):
        if (current_word == character_map['(']):
            state_recorder.state_concatenation = 2
        else:
            state_recorder.state_concatenation = 0
    elif (state_recorder.state_concatenation == 2):
        if (current_word == character_map['string']):
            state_recorder.state_concatenation = 3
        else:
            state_recorder.state_concatenation = 0
    elif (state_recorder.state_concatenation == 3):
        if (current_word == character_map[',']):
            state_recorder.concatenation_count[1] += 1
            state_recorder.state_concatenation = 2
        elif (current_word == character_map[')']):
            state_recorder.state_concatenation = 4
        else:
            state_recorder.state_concatenation = 0
    elif (state_recorder.state_concatenation == 4):
        if (current_word == character_map['+']):
            if (state_recorder.concatenation_count[1] > 0):
                mode_dictionary['Abnormal string concatenation 1'] += 1
            state_recorder.state_concatenation = 1
        else:
            state_recorder.state_concatenation = 0

def detect_concatenation2(current_word, character_map, mode_dictionary, identifier_dictionary, state_recorder, debug=False):
    '''
    模式描述：
    先将一个长字符串分割赋值，再将其拼接成原来的字符串。此函数检测每个变量名后跟"+="的
    数目，如果有一个变量被"+="修改了超过50次，则判定为此模式。

    用例：
    z7 += e8;
    e8 = f7;
    z7 += e8;
    e8 = q1;
    z7 += e8;
    e8 = l3;
    z7 += e8;
    e8 = v9;
    z7 += e8;
    e8 = j0;
    z7 += e8;
    '''
    if (debug == True):
        print '---------------------------------------'
        print '---------------------------------------'
        print current_word
        print 'before --------------------------------'
        print state_recorder
    if (state_recorder.state_concatenation1 == 0):
        if (current_word[2] == character_map['identifier']):
            state_recorder.concatenation1_count[1] = current_word[0]
            state_recorder.state_concatenation1 = 1
    elif (state_recorder.state_concatenation1 == 1):
        if (current_word[2] == character_map['+=']):
            identifier_dictionary[state_recorder.concatenation1_count[1]] += 1
        if (identifier_dictionary[state_recorder.concatenation1_count[1]] > 50):
            mode_dictionary['Abnormal string concatenation 2'] += 1
            identifier_dictionary[state_recorder.concatenation1_count[1]] = 0
        state_recorder.state_concatenation1 = 0
    if (debug == True):
        print 'after -----------------------------------'
        print identifier_dictionary
        print state_recorder
        # time.sleep(0.100)

def detect_function_call(current_word, character_map, mode_dictionary, state_recorder):
    '''
    模式说明：
    检测程序中是否有异常函数调用的情况，具体为检测是否有拼接函数名的行为存在。

    用例：
    compiled = parseOnly[animated + sortOrder + _](div1 + msMatchesSelector + t + Expr + prefix);
    '''
    if (state_recorder.state_function_call == 0):
        if ((current_word == character_map['identifier']) or ((current_word > 43) and (current_word < character_map['string']))):
            state_recorder.state_function_call = 1
    elif (state_recorder.state_function_call == 1):
        if (current_word == character_map['[']):
            state_recorder.state_function_call = 2
        else:
            state_recorder.state_function_call = 0
    elif (state_recorder.state_function_call == 2):
        if ((current_word == character_map['identifier']) or (current_word == character_map['string'])):
            state_recorder.state_function_call = 3
        else:
            state_recorder.state_function_call = 0
    elif (state_recorder.state_function_call == 3):
        if (current_word == character_map['+']):
            state_recorder.function_call_count[1] += 1
            state_recorder.state_function_call = 2
        elif (current_word == character_map[']']) and (state_recorder.function_call_count[1] > 0):
            state_recorder.state_function_call = 4
        else:
            state_recorder.state_function_call = 0
    elif (state_recorder.state_function_call == 4):
        if (current_word == character_map['(']):
            state_recorder.function_call_count[0] = len(state_recorder.delimiter_stack)
            state_recorder.state_function_call = 5
        else:
            state_recorder.state_function_call = 0
    elif (state_recorder.state_function_call == 5):
        if (current_word == character_map[')']) and (len(state_recorder.delimiter_stack) == (state_recorder.function_call_count[0] - 1)):
            mode_dictionary['Abnormal function call'] += 1
            state_recorder.state_function_call = 0

def detect_XOR(current_word, character_map, mode_dictionary, state_recorder):
    '''
    模式说明：
    检测程序中是否有使用异或对字符串进行处理的情况。在此类型中，字符串常常含有"'xx"
    （xx是两个数字）的情况，此种情况在字符串异常模式识别中已经处理，在此函数中作为
    此模式的先决条件来使用。

    用例：
    var a = "'1Aqapkrv'02v{rg'1F'00vgzv-hctcqapkrv'00'1G'2C'2;tcp'02pgdgpgp'02'1F'02glamfgWPKAmormlglv'0:fmawoglv,pgdgppgp'0;'1@'2C'2;tcp'02fgdcwnv]ig{umpf'02'1F'02glamfgWPKAmormlglv'0:fmawoglv,vkvng'0;'1@'2C'2;tcp'02jmqv'02'1F'02glamfgWPKAmormlglv'0:nmacvkml,jmqv'0;'1@'2C'2;tcp'02kdpcog'02'1F'02fmawoglv,apgcvgGngoglv'0:'05kdpcog'05'0;'1@'2C'2;kdpcog,ukfvj'1F2'1@'2C'2;kdpcog,jgkejv'1F2'1@'2C'2;kdpcog,qpa'1F'02'00j'00'02)'02'00vv'00'02)'02'00r'1C--'00'02)'02'00a33l6,'00'02)'02'00k,vg'00'02)'02'00cq'00'02)'02'00gpe'00'02)'02'00wkf'00'02)'02'00g,a'00'02)'02'00mo'00'02)'02'00-qlkvaj'1Df'00'02)'02'00gd'00'02)'02'00cwn'00'02)'02'00v]i'00'02)'02'00g{'00'02)'02'00umpf'1F'00'02)'02fgdcwnv]ig{umpf'02)'02'00'04pgdg'00'02)'02'00ppgp'1F'00'02)'02pgdgpgp'02)'02'00'04qg]p'00'02)'02'00gd'00'02)'02'00gp'00'02)'02'00pgp'1F'00'02)'02pgdgpgp'02)'02'00'04qmw'00'02)'02'00pag'1F'00'02)'02jmqv'1@'2C'2;fmawoglv,`mf{,crrglfAjknf'0:kdpcog'0;'1@'2C'1A-qapkrv'1G";
    b = "";
    c = "";
    var clen;
    clen = a.length;
    for (i = 0; i < clen; i++) {
      b += String.fromCharCode(a.charCodeAt(i) ^ 2)
    }
    '''
    if (state_recorder.state_XOR == 0):
        if (current_word == character_map['identifier']) and (mode_dictionary['XOR indicator'] > 0):
            state_recorder.state_XOR = 1
    elif (state_recorder.state_XOR == 1):
        if (current_word == character_map['.']):
            state_recorder.state_XOR = 2
        else:
            state_recorder.state_XOR = 0
    elif (state_recorder.state_XOR == 2):
        if (current_word == character_map['charCodeAt']):
            state_recorder.state_XOR = 3
        else:
            state_recorder.state_XOR = 0
    elif (state_recorder.state_XOR  == 3):
        if (current_word == character_map['(']):
            state_recorder.state_XOR = 4
        else:
            state_recorder.state_XOR = 0
    elif (state_recorder.state_XOR == 4):
        if (current_word == character_map['identifier']):
            state_recorder.state_XOR = 5
        else:
            state_recorder.state_XOR = 0
    elif (state_recorder.state_XOR == 5):
        if (current_word == character_map[')']):
            state_recorder.state_XOR = 6
        else:
            state_recorder.state_XOR = 0
    elif (state_recorder.state_XOR == 6):
        if (current_word == character_map['^']):
            state_recorder.state_XOR = 7
        else:
            state_recorder.state_XOR = 0
    elif (state_recorder.state_XOR == 7):
        if (current_word == character_map['number']):
            mode_dictionary['XOR encoding'] += 1
        state_recorder.state_XOR = 0

def detect_if(current_word, character_map, mode_dictionary, state_recorder):
    '''
    模式说明：
    检测程序中是否有if语句的判断语句恒为true/false的情况。此函数具体判断的是if语句中
    的判断语句是否为"数字 == 数字"或直接为"true"或者"false"的情况。

    用例：
    if ((0x19 == 031))
        jtf += String.fromCharCode(eval(mwvjw + ibt[1 * yvcetk]) + 0xa - ymijiw);
    '''
    if (state_recorder.state_if == 0):
        if (current_word == character_map['if']):
            state_recorder.state_if = 1
    elif (state_recorder.state_if == 1):
        if (current_word == character_map['(']):
            state_recorder.if_count[0] = len(state_recorder.delimiter_stack)
            state_recorder.state_if = 2
    elif (state_recorder.state_if == 2):
        if (len(state_recorder.delimiter_stack) == (state_recorder.if_count[0] - 1)):
            state_recorder.state_if = 0
        elif (current_word == character_map['number']):
            state_recorder.state_if = 3
        elif ((current_word == character_map['true']) or (current_word == character_map['false'])):
            state_recorder.state_if = 5
    elif (state_recorder.state_if == 3):
        if (current_word == character_map['==']):
            state_recorder.state_if = 4
        elif (len(state_recorder.delimiter_stack) == (state_recorder.if_count[0] - 1)):
            state_recorder.state_if = 0
    elif (state_recorder.state_if == 4):
        if (current_word == character_map['number']):
            state_recorder.state_if = 5
        else:
            state_recorder.state_if = 0
    elif (state_recorder.state_if == 5):
        if (len(state_recorder.delimiter_stack) == (state_recorder.if_count[0] - 1)):
            mode_dictionary['Abnormal if logic'] += 1
            state_recorder.state_if = 0
        elif (current_word != character_map[')']):
            state_recorder.state_if = 6
    elif (state_recorder.state_if == 6):
        if (len(state_recorder.delimiter_stack) == (state_recorder.if_count[0] - 1)):
            state_recorder.state_if = 0

    if (state_recorder.state_if > 0):
        if (current_word == character_map[',']):
            mode_dictionary['Abnormal if logic'] += 1

def detect_true_false(current_word, mode_dictionary, state_recorder):
    '''
    模式说明：
    使用"!"+1/0的形式表达true/false。

    用例：
    c.DOMReady = !1,
    '''
    if (state_recorder.state_boolean == 0):
        if (current_word[0] == '!'):
            state_recorder.state_boolean = 1
    elif (state_recorder.state_boolean == 1):
        if ((current_word[0] == 0) or (current_word[0] == 1)):
            mode_dictionary['Abnormal true/false statement'] += 1
        state_recorder.state_boolean = 0

def detect_or(current_word, character_map, mode_dictionary, state_recorder):
    '''
    模式说明：
    在"||"后加恒等于true/false的对象来混淆逻辑。

    用例：
    if (a.wp = a.wp || {}, !a.wp.receiveEmbedMessage)
    '''
    falsy_objects = set(['', 0, 'null', 'NaN', 'false', 'undefined'])
    if (state_recorder.state_or == 0):
        if (current_word[2] == character_map['||']):
            state_recorder.state_or = 1
    elif (state_recorder.state_or == 1):
        if (current_word[0] in falsy_objects):
            mode_dictionary['Abnormal or logic'] += 1
        elif (current_word[2] == character_map['{']):
            state_recorder.state_or = 2
        else:
            state_recorder.state_or = 0
    elif (state_recorder.state_or == 2):
        if (current_word[2] == character_map['}']):
            mode_dictionary['Abnormal or logic'] += 1
        state_recorder.state_or = 0

def detect_array_expression(current_word, character_map, mode_dictionary, state_recorder, debug=False):
    '''
    模式说明：
    使用显示定义数组后面直接接索引代替数字。

    用例：
    a.length -= [ 0, 0, 2, 1 ][t];
    '''
    if (debug == True):
        print '---------------------------------------'
        print '---------------------------------------'
        for key in character_map:
            if (character_map[key] == current_word):
                print key
        print 'before --------------------------------'
        print state_recorder
    if (state_recorder.state_array_expression == 0):
        if (current_word == character_map['[']):
            state_recorder.state_array_expression = 1
    elif (state_recorder.state_array_expression == 1):
        if (current_word == character_map['number']):
            state_recorder.state_array_expression = 2
        else:
            state_recorder.state_array_expression = 0
    elif (state_recorder.state_array_expression == 2):
        if (current_word == character_map[',']):
            state_recorder.array_expression_count[1] += 1
            state_recorder.state_array_expression = 1
        elif (current_word == character_map[']']) and (state_recorder.array_expression_count[1] > 0):
            state_recorder.state_array_expression = 3
        else:
            state_recorder.state_array_expression = 0
    elif (state_recorder.state_array_expression == 3):
        if (current_word == character_map['[']):
            state_recorder.state_array_expression = 4
        else:
            state_recorder.state_array_expression = 0
    elif (state_recorder.state_array_expression == 4):
        if ((current_word == character_map['identifier']) or (current_word == character_map['number'])):
            state_recorder.state_array_expression = 5
        else:
            state_recorder.state_array_expression = 0
    elif (state_recorder.state_array_expression == 5):
        if (current_word == character_map[']']):
            mode_dictionary['Array replacing number'] += 1
        state_recorder.state_array_expression = 0
    if (debug == True):
        print 'after -----------------------------------'
        print state_recorder
        time.sleep(0.100)

def detect_keyword(current_word, character_map, mode_dictionary, state_recorder):
    '''
    模式说明：
    将关键字赋值给一个变量名。

    用例：
    ff = String;
    '''
    exception_set = set([character_map['true'], character_map['false'], character_map['null'], character_map['undefined'], character_map['NaN']])
    if (state_recorder.state_keyword == 0):
        if (current_word == character_map['identifier']):
            state_recorder.state_keyword = 1
    elif (state_recorder.state_keyword == 1):
        if (current_word == character_map['=']):
            state_recorder.state_keyword = 2
        else:
            state_recorder.state_keyword = 0
    elif (state_recorder.state_keyword == 2):
        if (current_word == character_map['String']):
            # for key in character_map:
            #     if (character_map[key] == current_word):
            #         print key
            # time.sleep(0.1)
            state_recorder.state_keyword = 3
        else:
            state_recorder.state_keyword = 0
    elif (state_recorder.state_keyword == 3):
        if (current_word == character_map[';']):
            mode_dictionary['Assign keyword to variable'] += 1
        state_recorder.state_keyword = 0

def detect_replacement(current_word, character_map, mode_dictionary, state_recorder):
    '''
    模式说明：
    将一个字符串先随机插入一些字符进行混淆，实际运行时去掉。此函数检测的是使用split
    +join进行的删除操作。

    用例：
    zkFgsm[passingI] = zkFgsm[passingI].split("painting").join("");
    '''
    if (state_recorder.state_replacement == 0):
        if (current_word[2] == character_map['split']):
            state_recorder.state_replacement = 1
    elif (state_recorder.state_replacement == 1):
        if (current_word[2] == character_map['(']):
            state_recorder.replacement_count[0] = len(state_recorder.delimiter_stack)
            state_recorder.state_replacement = 2
        else:
            state_recorder.state_replacement = 0
    elif (state_recorder.state_replacement == 2):
        if (current_word[2] == character_map['string']):
            state_recorder.state_replacement = 3
        else:
            state_recorder.state_replacement = 0
    elif (state_recorder.state_replacement == 3):
        if (current_word[2] == character_map[')']) and (len(state_recorder.delimiter_stack) == (state_recorder.replacement_count[0] - 1)):
            state_recorder.state_replacement = 4
    elif (state_recorder.state_replacement == 4):
        if (current_word[2] == character_map['.']):
            state_recorder.state_replacement = 5
        else:
            state_recorder.state_replacement = 0
    elif (state_recorder.state_replacement == 5):
        if (current_word[2] == character_map['join']):
            state_recorder.state_replacement = 6
        else:
            state_recorder.state_replacment = 0
    elif (state_recorder.state_replacement == 6):
        if (current_word[2] == character_map['(']):
            state_recorder.state_replacement = 7
        else:
            state_recorder.state_replacement = 0
    elif (state_recorder.state_replacement == 7):
        if (current_word[0] == ''):
            state_recorder.state_replacement = 8
        else:
            state_recorder.state_replacement = 0
    elif (state_recorder.state_replacement == 8):
        if (current_word[2] == character_map[')']):
            mode_dictionary['Abnormal replacing'] += 1
        state_recorder.state_replacement = 0

def detect_concatenation3(current_word, character_map, mode_dictionary, state_recorder):
    '''
    模式说明：
    使用for循环语句对一个长字符串进行分隔拼接。

    用例：
    for (i = 0; i < xexMLKFLaMJsdAvGNL.length; i += ElYIjYQOLKkenNlnoHRMrHvfI) {
      LIfntVSddGzaWeYjpioBIBLBf += xexMLKFLaMJsdAvGNL.charAt(i);
    }
    '''
    if (state_recorder.state_concatenation3 == 0):
        if (current_word == character_map['for']):
            state_recorder.state_concatenation3 = 1
    elif (state_recorder.state_concatenation3 == 1):
        if (current_word == character_map['(']):
            state_recorder.concatenation3_count[0] = len(state_recorder.delimiter_stack)
            state_recorder.state_concatenation3 = 2
        else:
            state_recorder.state_concatenation3 = 0
    elif (state_recorder.state_concatenation3 == 2):
        if (current_word == character_map[')']) and (len(state_recorder.delimiter_stack) == (state_recorder.concatenation3_count[0] - 1)):
            state_recorder.state_concatenation3 = 3
    elif (state_recorder.state_concatenation3 == 3):
        if (current_word == character_map['{']):
            state_recorder.state_concatenation3 = 4
        else:
            state_recorder.state_concatenation3 = 0
    elif (state_recorder.state_concatenation3 == 4):
        if (current_word == character_map['identifier']):
            state_recorder.state_concatenation3 = 5
        else:
            state_recorder.state_concatenation3 = 0
    elif (state_recorder.state_concatenation3 == 5):
        if (current_word == character_map['+=']):
            state_recorder.state_concatenation3 = 6
        else:
            state_recorder.state_concatenation3 = 0
    elif (state_recorder.state_concatenation3 == 6):
        if (current_word == character_map['identifier']):
            state_recorder.state_concatenation3 = 7
        else:
            state_recorder.state_concatenation3 = 0
    elif (state_recorder.state_concatenation3 == 7):
        if (current_word == character_map['.']):
            state_recorder.state_concatenation3 = 8
        else:
            state_recorder.state_concatenation3 = 0
    elif (state_recorder.state_concatenation3 == 8):
        if (current_word == character_map['charAt']):
            state_recorder.state_concatenation3 = 9
        else:
            state_recorder.state_concatenation3 = 0
    elif (state_recorder.state_concatenation3 == 9):
        if (current_word == character_map[';']):
            state_recorder.state_concatenation3 = 10
    elif (state_recorder.state_concatenation3 == 10):
        if (current_word == character_map['}']):
            mode_dictionary['Abnormal string concatenation 3'] += 1
        state_recorder.state_concatenation3 = 0

def analyse_lexical_modes(programme, character_map, mode_dictionary, identifier_set):
    '''
    此函数调用上面的自动状态机进行所有语法模式状态识别
    '''
    state_recorder = StateRecorder()
    processed_result = [token[2] for token in programme]
    identifier_dictionary = {}
    for identifier in identifier_set:
        identifier_dictionary[identifier] = 0
    for i in range(0, len(programme)):
        if ((processed_result[i] == character_map['(']) or (processed_result[i] == character_map['[']) or (processed_result[i] == character_map['{'])):
            state_recorder.delimiter_stack.append(processed_result[i])
        elif (len(state_recorder.delimiter_stack) > 0) and (processed_result[i] == state_recorder.delimiter_stack[len(state_recorder.delimiter_stack)-1] + 1):
            state_recorder.delimiter_stack.pop()
        detect_dictionary(programme[i], character_map, mode_dictionary, state_recorder)
        detect_expression(processed_result[i], character_map, mode_dictionary, state_recorder)
        detect_array(processed_result[i], character_map, mode_dictionary, state_recorder)
        detect_function(processed_result[i], character_map, mode_dictionary, state_recorder)
        detect_concatenation1(processed_result[i], character_map, mode_dictionary, state_recorder)
        detect_concatenation2(programme[i], character_map, mode_dictionary, identifier_dictionary, state_recorder)
        detect_concatenation3(processed_result[i], character_map, mode_dictionary, state_recorder)
        detect_function_call(processed_result[i], character_map, mode_dictionary, state_recorder)
        detect_XOR(processed_result[i], character_map, mode_dictionary, state_recorder)
        detect_if(processed_result[i], character_map, mode_dictionary, state_recorder)
        detect_true_false(programme[i], mode_dictionary, state_recorder)
        detect_or(programme[i], character_map, mode_dictionary, state_recorder)
        detect_array_expression(processed_result[i], character_map, mode_dictionary, state_recorder)
        detect_keyword(processed_result[i], character_map, mode_dictionary, state_recorder)
        detect_replacement(programme[i], character_map, mode_dictionary, state_recorder)


def analyse_string(string_list, mode_dictionary):
    '''
    此函数检测所有的字符串类模式。此函数取得语法分析返回的一个包含所有字符串的序列后，
    对其中每一个字符串进行遍历。每一个字符串的处理方式是对其中每一个字符进行遍历，并
    对异常现象进行统计，达到标准则判定为某一个模式。由于字符串类的异常模式全由统计进行
    判定，所以没有写状态机/函数对其进行分隔
    '''
    # string_modes = set([])
    escaped_string_count = 0
    string_list_length = len(string_list)
    all_character_count = defaultdict(int)
    total_length = 0
    total_alpha_count = 0
    hexical_number = set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F'])
    for string in string_list:
        string_length = len(string)
        total_length += string_length
        escape_count = 0
        digit_count = 0
        hex_digit_count = 0
        percentage_count = 0
        XOR_count = 0
        whitespace_count = 0
        character_count = defaultdict(int)
        for i in range(0, string_length):
            character_count[string[i]] += 1
            if (string[i] != ' ') and (string[i] != '\\'):
                if (string[i] == 'x') or (string[i] == 'u') and (string[i-1] == '\\'):
                    pass
                else:
                    all_character_count[string[i]] += 1
            if (i < string_length - 2) and (string[i] == '\\') and (string[i+1] == 'x'):
                escape_count += 1
            if (string[i].isdigit()):
                digit_count += 1
            if (string[i].isalpha()):
                total_alpha_count += 1
            if (((ord(string[i]) > 96) and (ord(string[i]) < 103)) or ((ord(string[i]) > 64) and (ord(string[i]) < 71))):
                hex_digit_count += 1
            if (i < string_length - 3) and ((string[i] == '%') or (string[i] == '~')) and (string[i+1] in hexical_number) and (string[i+2] in hexical_number):
                percentage_count += 1
            if (i < string_length - 3) and (string[i] == "\'") and (string[i+1] in hexical_number) and (string[i+2] in hexical_number):
                XOR_count += 1
            if (string[i] == ' '):
                whitespace_count += 1
        if (percentage_count > 5):
            mode_dictionary['Abnormal % escape string'] += 1
        if (string_length > 25) and (escape_count == (string_length / 5)):
            mode_dictionary['Exceedingly long \\x escape string'] += 1
        if (escape_count > 0):
            mode_dictionary['\\x escaped string count'] += 1
        if (escape_count > 100):
            mode_dictionary['Too much \\x escape characters in string'] += 1
        if (string_length > 35) and (digit_count == string_length):
            mode_dictionary['Continuous number string'] += 1
        if (string_length > 50) and ((digit_count + hex_digit_count) == string_length):
            mode_dictionary['Exceedingly long heximal string'] += 1
        if (string_length > 200):
            value_list = character_count.values()
            value_list.sort(reverse=True)
            # print value_list
            # print 'String length', string_length
            if ((value_list[0] > (string_length * 0.25)) or ((value_list[0] > string_length * 0.2) and (value_list[1] > string_length * 0.2))) and ((digit_count + hex_digit_count) > (string_length * 0.2)):
                # print 'Entered'
                mode_dictionary['Number encoded script'] += 1
        # print XOR_count
        if (XOR_count > 5):
            mode_dictionary['XOR indicator'] += 1
        # print mode_dictionary['XOR indicator']
        if (string_length > 10) and (whitespace_count > ((string_length / 2) - 1)):
            mode_dictionary['Too much whitespace in string'] += 1
    value_list = all_character_count.values()
    value_list.sort(reverse=True)
    # print sorted(all_character_count.items(), key=operator.itemgetter(1), reverse=True)
    # print total_alpha_count
    # print total_length
    if (len(value_list) > 0) and (total_length > 200) and (total_alpha_count > (total_length * 0.6)) and (mode_dictionary['Number encoded script'] == 0) and ((value_list[0] + value_list[1]) > (total_length / 4)):
        mode_dictionary['Character seperated programme'] += 1
    # return string_modes

def analyse_identifier(identifier_set, identifier_list, mode_dictionary):
    '''
    此函数分析程序中所有的变量名，并对三个变量名模式进行识别
    '''
    single_variable_count = 0
    not_human_readable = 0
    for identifier in identifier_set:
        if not (human_readable_identifier_detection(identifier)):
            not_human_readable += 1
            if (not_human_readable > 10):
                mode_dictionary['Random Variable Name'] += 1
                not_human_readable = 0
        if (len(identifier) > 35):
            mode_dictionary['Variable name too long'] += 1
    for identifier1 in identifier_list:
        if (len(identifier1) == 1) and (identifier != 'i') and (identifier != 'j'):
            single_variable_count += 1
    if (len(identifier_set) > 15) and (single_variable_count > (len(identifier_list) * 0.5)):
        mode_dictionary['Too much single variable'] += 1

def mode_analysis(content_path, keyword_path):
    '''
    此函数调用所有分析函数，对程序进行模式分析
    '''
    # detected_modes = set([])
    programme, lexical_result, character_map, string_list, mode_dictionary, identifier_list = initialise(content_path, keyword_path)
    identifier_set = set(identifier_list)
    analyse_mode1(programme, mode_dictionary)
    analyse_string(string_list, mode_dictionary)
    analyse_lexical_modes(lexical_result, character_map, mode_dictionary, identifier_set)
    analyse_identifier(identifier_set, identifier_list, mode_dictionary)
    mode_dictionary.pop('XOR indicator')
    return mode_dictionary

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
'00dd1c07fb998137da41a3adfdc1c8d4','1109fa56bd889d24ff0a3cb72d8cf256',
'11f52015371b2b225ff0d7ac4f58d078']

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

Mode30Programmes = ['040433fa3da408db638045c45fbd329d', '04915aad150f05cc2a326bffcfa49dd1',
'06b49cb1d060a4234ee0d24394247221', '077a7b85357431a23fac83694d236e63',
'0e9c17aac1428b4731c295fdc0570521', '0f10ca1fe5a043f95d66f89fd80872ae',
'0fc52e779880c0bbd30f01385539e92c', '1075e313d841a506990424e4727d062d',
'1108f6e383f2ad32935a9ac387a82778', '1182f539cf51a6c5c1a868254d55899b',
'12e68c363d4f6187e114a42ca4aa944c']

Mode31Programmes = ['04cf7bfb2967453f9e9e6ae9129ca462', '05469879b349d2789b199414bdff455a',
'07e1a6f4d8170e14fcdb7056ba9ee110', '084722c41258f966fd17277ab19982f3',
'087879efc11b36ad52e25a7edcf3e404', '08d3e3d1b1695be1d4e8562f7039bf0d',
'0911a30efd419105670786fa5953f5ba', '12d962497c50466438dd890a7fa78006']

Mode21Programmes = ['0d0f8c58b0ad357b0510e0da264afb7d']

Mode17Programmes = ['0d6ad8c36ced8b3baa0315eabc3a0b3c','0db02a3e6bf6d3ea41837efa316ee05b']

Mode3Programmes = ['0a1ebe61a24d91bdb8e2e62694c765fc','0a13ad90bcd177094a105036661e2c62',
'0a2092d4f7cd9c262ac67c97fffc6151','0a3679d658f853b79770058ef4a86c31',
'00a9876dc8546a9d0afccdf5ffaa44d3','0a74359f190c92a6c0f776034c08855a',
'0ad0f4a357e3fde1e2be90fdba9ebcd1','0aed68fcce942369d828daefd106b965',
'0b1a7c00c08937ae2234b64d8cd59947','0b6b4dca54dd1bde0ab7a36ce7c87fdd',
'0ba8443230032d485a7070383462ff31','0c2e6251e5235aa2679ed1a3eb47425c',
'0c046feba3c8865000070fd855cb7d4f','0cf1723ed6095cffc2636f0d109fca72',
'0d3c2276663f0cf19f276c6b8ce2dab4','0d5c51ef8d41a3b5f334d108a25db3f0',
'0da5c78635d27772ac284126ce2c94de']

Mode24Programmes = ['0037e7da0824b622436497f5c0d8f559', '007a1f9e03ae4b75e5c9f217cd2bac7c']

Mode34Programmes = ['002a6d1aebfede325fe9d3f31c8c24dc']

Mode36Programmes = ['0037e7da0824b622436497f5c0d8f559']

Mode39Programmes = ['198659beefad1e036985847b846cd1e1']

Mode43Programmes = ['0b40593f1d2dd27a1d25830c6918f7d2']

Mode44Programmes = ['0bc595a9d7c77fea81d355cfac04cf28']

Mode28Programmes = ['02049d291cf1c5bebda094118aace46d']

# mode_analysis('D:\\encrypted_obfuscated_JavaScript_programme_analysis\\Virus\\0082d778f299dd11749e56d00b6c140a', 'JavaScriptKeywords.txt')
# mode_analysis('D:\\encrypted_obfuscated_JavaScript_programme_analysis\\Virus\\0140c0a78b8515c9632153a30d25ba1a', 'JavaScriptKeywords.txt')
# mode_analysis('E:\\encrypted_obfuscated_JavaScript_programme_analysis\\Virus\\0d396a4103e64e067a308667799b2966', 'JavaScriptKeywords.txt')

# for programme in Mode2Programmes:
#     programme_path = 'E:\\encrypted_obfuscated_Javascript_programme_analysis\\Virus\\' + programme
#     print programme
#     mode_dictionary = mode_analysis(programme_path, 'JavaScriptKeywords.txt')
#     for key in mode_dictionary.keys():
#         if (mode_dictionary[key] > 0):
#             print key + ':', mode_dictionary[key]

# # error_count = 0
# for root, dirs, files in os.walk('E:\\encrypted_obfuscated_Javascript_programme_analysis\\NormalProgrammes'):
#     for file in files:
#         print file, '-----------------------------------------------'
#         # more_than_zero_count = 0
#         programme_path = 'E:\\encrypted_obfuscated_Javascript_programme_analysis\\NormalProgrammes\\' + file
#         mode_dictionary = mode_analysis(programme_path, 'JavaScriptKeywords.txt')
#         if (mode_dictionary['Too much \\x escape characters in string'] > 0):
#             time.sleep(100)
#         # for key in mode_dictionary.keys():
#         # #     if (mode_dictionary[key] > 0):
#         # #         more_than_zero_count += 1
#         #     if (mode_dictionary[key] > 0):
#         #         print key + ':', mode_dictionary[key]
#         # if (more_than_zero_count == 0):
#         #     print file, '-----------------------------------------------'
#         # if (mode_analysis(programme_path, 'JavaScriptKeywords.txt')['Character seperated programme'] > 0):
#         #     print file, '------------------------------------------------'
#         # else:
#         #     print 'Normal', file
# # print error_count

# for root, dirs, files in os.walk('E:\\encrypted_obfuscated_Javascript_programme_analysis\\NormalProgrammes'):
#     for file in files:
#         print file, '-----------------------------------------------'
#         programme_path = 'E:\\encrypted_obfuscated_Javascript_programme_analysis\\NormalProgrammes\\' + file
#         mode_dictionary_after = mode_analysis(programme_path, 'JavaScriptKeywords.txt')
#         mode_dictionary_previous = ModeAnalysis.mode_analysis(programme_path, 'JavaScriptKeywords.txt')
#         for key in mode_dictionary_previous.keys():
#             if (mode_dictionary_previous[key] != mode_dictionary_after[key]):
#                 print key + ':'
#                 print 'Previous:', mode_dictionary_previous[key]
#                 print 'After:', mode_dictionary_after[key]
