# -*- coding: utf-8 -*-

import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.externals import joblib
from ModeAnalysisRestructured import mode_analysis
from scipy.sparse import csr_matrix

def normalise_dictionary(mode_dictionary):
    if (mode_dictionary['Abnormal replacing'] > 0):
        mode_dictionary['Abnormal replacing'] = 1
    if (mode_dictionary['Abnormal string concatenation 1'] > 0):
        mode_dictionary['Abnormal string concatenation 1'] = 1
    if (mode_dictionary['Abnormal string concatenation 2'] > 0):
        mode_dictionary['Abnormal string concatenation 2'] = 1
    if (mode_dictionary['Abnormal true/false statement 1'] > 0):
        mode_dictionary['Abnormal true/false statement 1'] = 1
    if (mode_dictionary['Array replacing number'] > 0):
        mode_dictionary['Array replacing number'] = 1
    if (mode_dictionary['Assign keyword to variable'] > 0):
        mode_dictionary['Assign keyword to variable'] = 1
    if (mode_dictionary['Exceedingly long heximal string'] > 0):
        mode_dictionary['Exceedingly long heximal string'] = 1
    if (mode_dictionary['Exceedingly long \\x escape string'] > 0):
        mode_dictionary['Exceedingly long \\x escape string'] = 1
    if (mode_dictionary['Expression replacing number'] > 0):
        mode_dictionary['Experssion replacing number'] = 1
    if (mode_dictionary['Function replacing assignment'] > 1):
        mode_dictionary['Function replacing assignment'] = 1
    if (mode_dictionary['Number encoded script'] < 4):
        mode_dictionary['Number encoded script'] = mode_dictionary['Number encoded script'] / float(3)
    else:
        mode_dictionary['Number encoded script'] = 1
    # if (mode_dictionary['Random Variable Name'] > 0):
    #     mode_dictionary['Random Variable Name'] = 1
    if (mode_dictionary['Exceedingly long heximal string'] > 0):
        mode_dictionary['Exceedingly long heximal string'] = 1
    if (mode_dictionary['\\x escaped string count'] < 25):
        mode_dictionary['\\x escaped string count'] = mode_dictionary['\\x escaped string count'] / float(25)
    else:
        mode_dictionary['\\x escaped string count'] = 1
    if (mode_dictionary['Too much whitespace in string'] > 0):
        mode_dictionary['Too much whitespace in string'] = 1
    if (mode_dictionary['XOR encoding'] > 0):
        mode_dictionary['XOR encoding'] = 1
    if (mode_dictionary['Exceedingly long array'] < 4):
        mode_dictionary['Exceedingly long array'] = mode_dictionary['Exceedingly long array'] / float(3)
    else:
        mode_dictionary['Exceedingly long array'] = 1
    if (mode_dictionary['Abnormal % escape string'] > 0):
        mode_dictionary['Abnormal % escape string'] = 1
    if (mode_dictionary['Abnormal % escape string'] > 0):
        mode_dictionary['Abnormal % escape string'] = 1
    if (mode_dictionary['Abnormal function call'] < 10):
        mode_dictionary['Abnormal function call'] = mode_dictionary['Abnormal function call'] / float(10)
    else:
        mode_dictionary['Abnormal function call'] = 1
    if (mode_dictionary['Abnormal if logic'] > 0):
        mode_dictionary['Abnormal if logic'] = 1
    if (mode_dictionary['Abnormal String.fromCharCode'] > 0):
        mode_dictionary['Abnormal String.fromCharCode'] = 1
    if (mode_dictionary['Keyword in string'] < 5):
        mode_dictionary['Keyword in string'] = mode_dictionary['Keyword in string'] / float(4)
    else:
        mode_dictionary['Keyword in string'] = 1
    # if (mode_dictionary['Keyword in string'] > 0):
    #     mode_dictionary['Keyword in string'] = 1
    return mode_dictionary

def dictionary_to_array(mode_dictionary):
    array_vector = []
    array_vector.append(mode_dictionary['Minimisation'])
    array_vector.append(mode_dictionary['Exceedingly long mapping'])
    array_vector.append(mode_dictionary['Keyword Concatenation'])
    array_vector.append(mode_dictionary['Exceedingly long heximal string'])
    array_vector.append(mode_dictionary['Exceedingly long \\x escape string'])
    array_vector.append(mode_dictionary['Number encoded script'])
    array_vector.append(mode_dictionary['Abnormal % escape string'])
    array_vector.append(mode_dictionary['Continuous number string'])
    array_vector.append(mode_dictionary['\\x escaped string count'])
    array_vector.append(mode_dictionary['Expression replacing number'])
    array_vector.append(mode_dictionary['Too much \\x escape characters in string'])
    array_vector.append(mode_dictionary['Exceedingly long array'])
    array_vector.append(mode_dictionary['Function replacing assignment'])
    array_vector.append(mode_dictionary['Abnormal string concatenation 1'])
    array_vector.append(mode_dictionary['Abnormal string concatenation 2'])
    array_vector.append(mode_dictionary['Abnormal string concatenation 3'])
    array_vector.append(mode_dictionary['Random Variable Name'])
    array_vector.append(mode_dictionary['Too much single variable'])
    array_vector.append(mode_dictionary['XOR encoding'])
    array_vector.append(mode_dictionary['Variable name too long'])
    array_vector.append(mode_dictionary['Too much whitespace in string'])
    array_vector.append(mode_dictionary['Character seperated programme'])
    array_vector.append(mode_dictionary['Abnormal function call'])
    array_vector.append(mode_dictionary['Abnormal if logic'])
    array_vector.append(mode_dictionary['Abnormal true/false statement 1'])
    array_vector.append(mode_dictionary['Abnormal true/false statement 2'])
    array_vector.append(mode_dictionary['Array replacing number'])
    array_vector.append(mode_dictionary['Assign keyword to variable'])
    array_vector.append(mode_dictionary['Abnormal replacing'])
    array_vector.append(mode_dictionary['Abnormal String.fromCharCode'])
    array_vector.append(mode_dictionary['Keyword in string'])
    array_vector.append(mode_dictionary['Base 64 encoding'])
    array_vector.append(mode_dictionary['Mysterious mode 1'])
    array_vector.append(mode_dictionary['Too much special characters in string'])
    array_vector.append(mode_dictionary['Special character string'])
    return array_vector


def get_data(abnormal_path, normal_path, keyword_path):
    raw_data = []
    abnormal_result_array = []
    l = []
    for root, dirs, files in os.walk(abnormal_path):
        l.extend(files)
    for f in l:
        vector = dictionary_to_array(normalise_dictionary(mode_analysis(abnormal_path + '\\' + f, keyword_path)))
        vector.append(1)
        abnormal_result_array.append(vector)
    normal_result_array = []
    for root, dirs, files in os.walk(normal_path):
        for file in files:
            programme_path = normal_path + '\\' + file
            try:
                vector = dictionary_to_array(normalise_dictionary(mode_analysis(programme_path, keyword_path)))
                vector.append(0)
                normal_result_array.append(vector)
            except:
               pass
    raw_data.extend(abnormal_result_array)
    raw_data.extend(normal_result_array)
    return raw_data

def test_model(raw_data):
    # Build DataFrame
    entry_length = len(raw_data[0])
    df = pd.DataFrame(np.array(raw_data))
    X = df.drop((entry_length - 1), axis=1)
    y = df[entry_length-1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)
    X_train_converted = csr_matrix(X_train)
    X_test_converted = csr_matrix(X_test)
    # for array_vector in X_test:
    #     X_test_converted.append(csr_matrix(array_vector))
    classifier = SVC(kernel='linear')
    # classifier = LinearSVC()
    classifier.fit(X_train_converted, y_train)
    y_pred = classifier.predict(X_test_converted)
    # print classifier.support_
    print classifier.coef_
    # print classifier.decision_function(X_test)
    print confusion_matrix(y_test, y_pred)
    print classification_report(y_test, y_pred)

def get_classifier(raw_data):
    # Build DataFrame
    entry_length = len(raw_data[0])
    df = pd.DataFrame(np.array(raw_data))
    X = df.drop((entry_length - 1), axis=1)
    y = df[entry_length-1]
    classifier = SVC(kernel='linear')
    classifier.fit(X, y)
    joblib.dump(classifier, 'prediction_obfuscation.pkl')
    return classifier

def predict_obfuscation(programme_path, keyword_path):
    classifier = joblib.load('prediction_obfuscation.pkl')
    vector = dictionary_to_array(normalise_dictionary(mode_analysis(programme_path, keyword_path)))
    vector_list = []
    vector_list.append(vector)
    prediction = classifier.predict(vector_list)
    if (prediction[0] == 1):
        return True
    else:
        return False

def get_model():
    abnormal_path = 'E:\\encrypted_obfuscated_Javascript_programme_analysis\\Model Testing\\Abnormal Train'
    normal_path = 'E:\\encrypted_obfuscated_Javascript_programme_analysis\\Model Testing\\Normal Train'
    keyword_path = 'JavaScriptKeywords.txt'
    get_classifier(get_data(abnormal_path, normal_path, keyword_path))

# test_model(get_data('E:\\encrypted_obfuscated_JavaScript_programme_analysis\\Virus', 'E:\\encrypted_obfuscated_JavaScript_programme_analysis\\NormalProgrammes', 'JavaScriptKeywords.txt'))
get_model()
