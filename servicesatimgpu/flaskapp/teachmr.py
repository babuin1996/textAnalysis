import os
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import string
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
import string
import pymorphy2
from os import path
from os import listdir
from PIL import Image
import numpy as np

from algorithms import remove_urls, mapper1, mapper2, reduce1, reduce2, reducer

data_folder = Path('teach_dir/')
pth = 'teach_dir/'
pattern = '.txt'

def teach_alg():
    saved_cwd = os.getcwd()
    path = 'teach_dir/'

    text_files = [f for f in os.listdir(path) if f.endswith('.txt')]
    rr = text_files[0]
    global name_teacher
    name_teacher = rr[:-(len('.txt'))]
    # print(name_teacher) #имя студента

    # объединяем все файлы в один
    data_folder = Path('teach_dir/')
    pth = 'teach_dir/'
    pattern = '.txt'

    filename = data_folder / rr

    file = open(filename, 'rt', encoding='utf8')
    text1 = file.read()
    file.close()
    # print(text1)
    # убираем гиперсылки
    import re

    # print(remove_urls(text1))
    text = remove_urls(text1)
    text2 = remove_urls(text1)

    text_clean = text.replace('-', ' ')  # replacing
    text_clean = text_clean.replace('.', ' ')  # replacing
    text_clean = text_clean.replace('’', '')  # replacing
    text_clean = text_clean.replace(')', '')  # replacing
    text_clean = text_clean.replace('(', '')  # replacing
    text_clean = text_clean.replace('', '')  # replacing
    text_clean = text_clean.replace('\n', ' ')  # replacing
    text_clean = text_clean.replace('\x92', '')  # replacing
    text_clean = text_clean.replace('\x94', '')  # replacing
    text_clean = text_clean.replace('\x86', '')  # replacing
    text_clean = text_clean.replace('№', '')  # replacing hyphens with whitespace \t « \xa0
    # text_clean = text_clean.replace('\xa0', ' ') #replacing
    text_clean = text_clean.replace('–', ' ')  # replacing
    text_clean = text_clean.replace('\t', ' ')  # replacing
    text_clean = text_clean.replace('«', '')  # replacing
    text_clean = text_clean.replace('»', '')  # replacing
    text_clean = text_clean.replace('—', ' ')  # replacing
    text_clean = text_clean.replace('/', ' ')  # replacing
    table = str.maketrans('', '', string.punctuation)
    text_clean = text_clean.translate(table)

    # removing numbers
    text_clean = re.sub(r'\d', '', text_clean)
    text_lower = text_clean.lower()  # lowercasing
    # len(text_lower)
    text_lower2 = text_lower.split(' ')
    text_lower3 = text_lower2
    # len(text_lower2)
    spec_chars = string.punctuation + '\n\xa0«»\t'
    text_test = " ".join([ch for ch in text_lower3 if ch not in spec_chars])

    from nltk import word_tokenize

    nltk.download('punkt')
    text_tokens = word_tokenize(text_test)

    # ##корпус слов преподавателя всего текста
    global korpus_teach
    korpus_teach = len(text_tokens)
    print('korpus_teach=', korpus_teach)
    from nltk import word_tokenize

    nltk.download('punkt')
    sentences = [word.lower() for word in text_lower3 if re.match('^[а-яА-ЯёЁ]+', word)]

    dftt = pd.DataFrame(text_tokens, columns=['Words'])
    dftt = dftt.dropna(subset=['Words'])
    # dftt
    sentences = dftt['Words'].values.tolist()
    # sentences
    # texttest = nltk.Text(sentences)
    # print(type(texttest))

    teach_all_words = pd.DataFrame(text_tokens, columns=['Words'])  # все слова преподавателя
    # print(teach_all_words)

    morph = pymorphy2.MorphAnalyzer()
    words = sentences
    normal_text = []
    for word in words:
        p = morph.parse(word)[0]
        normal_text.append(p.normal_form)
        # print(p.normal_form)
    # print(normal_text)

    # убираем все лишние слова

    shortest_word_len = 2

    result = [s for s in normal_text if len(s) > shortest_word_len]
    text_lower2 = result
    map11 = []
    map22 = []
    # a_to_m = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n', 'o','p','q','r','s','t','u','v','w','x','y','z']
    a_to_m = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
              'х',
              'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё']
    for words in text_lower2:
        if words[0][0] in a_to_m:
            map11.append(words)
        else:
            map22.append(words)
    text_lower2 = map11
    # len(text_lower2)
    text_lower = " ".join(map(str, text_lower2))

    # len(text_lower)
    # text_lower=" ".join(map(str, normal_text))
    # text_lower=normal_text
    # print(text_lower)

    # Mapper

    # Data Partition
    # Seperating the first 5000 lines and next in two seperate data frames
    text1 = text_lower[:5000]
    text2 = text_lower[5000:]

    # Making lists of the seperate data
    # Mapping words from first 5000 lines using mapper 1 in list 1

    list1 = []
    for x in mapper1(text1):
        list1.append(x)

    # Mapping words from rest of the lines using mapper 2 in list 2

    list2 = []
    for x in mapper2(text2):
        list2.append(x)

    # print(list1)
    # print(list2)

    # Merging the two lists

    final_list = list1 + list2
    # Sorting
    # Sorting the list alphabetically in ascending order
    final_list.sort()
    # len(final_list)
    # print(final_list[0])

    del final_list[0]

    # Partition of data before sending to reducer
    # Storing elements in final_list into two different lists: a-m in map1 and n-z in map2
    map1 = []
    map2 = []
    # a_to_m = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n', 'o','p','q','r','s','t','u','v','w','x','y','z']
    a_to_m = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
              'х',
              'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё']
    for words in final_list:
        if words[0][0] in a_to_m:
            map1.append(words)
        else:
            map2.append(words)

    # print(len(map1))
    # print(len(map2))

    # print(map1)
    # print(map2)

    # Reducing the first a-m list
    list3 = reduce1(map1)

    # Reducing the second n-z list
    list4 = reduce2(map2)

    # Merging the two reduced lists
    answer_list = list3 + list4

    # print(answer_list)

    # Reducer

    # Reducing the first a-m list
    list3 = reduce1(map1)

    # Reducing the second n-z list
    list4 = reduce2(map2)

    # Merging the two reduced lists
    answer_list = list3 + list4

    # Final Dataframe Vizualization
    df = pd.DataFrame(answer_list, columns=['Word', 'Frequency'])
    # df.info()
    # print(df.to_string())
    df1 = df[['Word', 'Frequency']].sort_values(ascending=False, by='Frequency')
    # print(df1)
    nltk.download('stopwords')
    russian_stopwords = stopwords.words("russian")
    stop_words_ru = pd.DataFrame(russian_stopwords)
    df_stop = stop_words_ru
    # print(df_stop)
    # очистка текста преподавателя применяя словарь стоп-слов используем ~
    df_stop.rename(columns={0: 'stop_ru'}, inplace=True)
    # print(df_stop)

    # очистка текста преподавателя применяя словарь стоп-слов используем ~
    global korp_teach, freqtch
    freqtch='Частота встречаемости слов преподавателя'
    korp_teach = 'Корпус преподавателя ' + name_teacher
    df_teach = df1.copy()
    global df_teach_clear
    df_teach_clear = df_teach[~df_teach.Word.isin(df_stop.stop_ru)].reset_index(drop=True)
    df_teach_clear.rename(columns={'Word': korp_teach}, inplace=True)
    df_teach_clear.rename(columns={'Frequency': freqtch}, inplace=True)
    # print(df_teach_clear.sort_values(by='Frequency', ascending=0).reset_index(drop=True))

    ##корпус слов лематизированный и вычещенный преподавателя
    global korpus_teach_lemma
    korpus_teach_lemma = len(df_teach_clear.index)
    print('korpus_teach_lemma=', korpus_teach_lemma)
    global df_teach_clear2
    # print(df_teach_clear.count())
    df_teach_clear2 = df_teach_clear.sort_values(by=freqtch, ascending=0).reset_index(drop=True)
    # print(df_teach_clear2)

    #with pd.ExcelWriter('static/downloads/teachers/Korpus_{0}.xlsx'.format(name_teacher)) as writer:
    with pd.ExcelWriter('static/downloads/teachers/Korpus_teacher.xlsx') as writer:
        df_teach_clear2.to_excel(writer, sheet_name='КорпусСлов')

    # Plotting the top 50
    # setting the figure size

    fig = plt.figure(figsize=(20, 10))
    # creating a bar plot
    ax = sns.barplot(x=korp_teach, y=freqtch, data=df_teach_clear2.head(20))
    # rotating the x axis labels
    ax.set_xticklabels(labels=df_teach_clear2.head(20)[korp_teach], rotation=75)
    # setting the title
    ax.set_title("Frequency  Teacher's korpus words")
    # setting the Y-axis labels
    ax.set_ylabel(freqtch)
    # Labelling the bars in the bar graph
    for p in ax.patches:
        ax.annotate(p.get_height(), (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')
    fig.tight_layout()
    plt.savefig('static/img/rezult/rez_teach/Korpus.jpg')
    #plt.show()
    # path2 = 'rezult/rez_teach/'
    # os.chdir(path2)
    # os.rename('Korpus.jpg', 'Корпус_преподавателя_'+name_teacher+'.jpg')
    # os.chdir(saved_cwd)
    global rez_teach2
    rez_teach2 = (korpus_teach, korpus_teach_lemma)
    rez_teach=rez_teach2
    return rez_teach

def rezteacher():
    r = rez_teach2
    return r




def teach_words():
    r = df_teach_clear
    return r


def teach_series_name():
    r = korp_teach
    return r


def teach_name():
    r = str(name_teacher)
    return r

def rezteachimage():
    r = df_teach_clear2
    return r

def freqtchimage():
    r = freqtch
    return r