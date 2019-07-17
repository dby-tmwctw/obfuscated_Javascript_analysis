# coding: utf-8

import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.externals import joblib
import get_vector
import LexicalProcessing
import ModeAnalysisRestructured

# 本段结束后，raw_data应当是一个二维数组，每个向量包含9个元素（8个特征值+类别）

def generate_learning_data(abnormal_path, normal_path, keyword_path):
    raw_data = []
    abnormal_result_array = []
    l = []
    for root, dirs, files in os.walk(abnormal_path):
        l.extend(files)
    for f in l:
        vector = get_vector.get_vector(abnormal_path + '\\' + f, keyword_path)
        vector.append(1)
        # 1是类别，代表有拼接
        abnormal_result_array.append(vector)
    normal_result_array = []
    for root, dirs, files in os.walk(normal_path):
        for file in files:
            programme_path = normal_path + '\\' + file
            try:
                vector = get_vector.get_vector(programme_path, keyword_path)
                vector.append(0)
                # 0是类别，代表无拼接
                normal_result_array.append(vector)
            except:
               pass
    raw_data.extend(abnormal_result_array)
    raw_data.extend(normal_result_array)
    return raw_data

def generate_classifier(raw_data):
    # Build DataFrame
    df = pd.DataFrame(np.array(raw_data))
    # index 8 是类型，drop之后就只剩下特征值
    # X是一个矩阵，含有特征值；y是向量，含有0或1，是结果
    X = df.drop(8, axis=1)
    y = df[8]
    classifier = SVC(kernel='linear')
    classifier.fit(X, y)
    joblib.dump(classifier, 'concatenation_model.pkl')
    return classifier

def load_and_predict(programme_path, keyword_path, abnormal_count, plus_equal_percentage, square_bracket_percentage, string_list):
    classifier = joblib.load('concatenation_model.pkl')
    vector = get_vector.get_vector(programme_path, keyword_path, abnormal_count, plus_equal_percentage, square_bracket_percentage, string_list)
    vector_list = []
    vector_list.append(vector)
    prediction = classifier.predict(vector_list)
    if (prediction[0] == 1):
        return True
    else:
        return False

def generate_model():
    abnormal_path = 'E:\\encrypted_obfuscated_Javascript_programme_analysis\\Abnormal String Concatenation'
    normal_path = 'E:\\encrypted_obfuscated_Javascript_programme_analysis\\Archive'
    keyword_path = 'JavaScriptKeywords.txt'
    generate_classifier(generate_learning_data(abnormal_path, normal_path, keyword_path))

def hand_written_training(abnormal_path, keyword_path):
    file_count = 0
    plus_equal_average = 0
    average_string_length_average = 0
    count_1_to_5_average = 0
    count_special_char_average = 0
    square_bracket_average = 0
    num_and_char_average = 0
    for root, dirs, files in os.walk(abnormal_path):
        file_count = len(files)
        for file in files:
            programme_path = abnormal_path + '\\' + file
            vector = get_vector.get_vector(programme_path, keyword_path)
            plus_equal_average += vector[0]
            average_string_length_average += vector[1]
            count_1_to_5_average += vector[2]
            count_special_char_average += vector[3]
            square_bracket_average += vector[4]
            num_and_char_average += vector[5]
    model = [plus_equal_average, average_string_length_average, count_1_to_5_average, count_special_char_average, square_bracket_average, num_and_char_average]
    for i in range(0, len(model)):
        model[i] = model[i] / float(file_count)
    with open('ExperimentModel', 'w') as f:
        f.write(repr(model))

def calculate_score(programme_path, keyword_path):
    model = []
    with open('ExperimentData') as f:
        model = eval(f.read())
    vector = get_vector.get_vector(programme_path, keyword_path)
    score = 0
    score += 10 * vector[6]
    score += 10 * vector[7]
    for i in range(0, 6):
        if (i == 1):
            score -= abs(vector[1] - model[i])
        else:
            score -= 5 * abs(vector[i] - model[i])
    return score
