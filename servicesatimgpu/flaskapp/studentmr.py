import math
import os
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import string
import pymorphy2

# определяем количество файлов в каталоге
from algorithms import remove_urls, mapper1, mapper2, reduce1, reduce2, reducer
from teachmr import teach_words, teach_name, teach_series_name, rezteacher, rezteacher, teach_alg

global scoress
scoress={}

def alg_stud():
    original= pd.DataFrame()
    df_marks = pd.DataFrame()
    rez_teach = teach_alg()
    data_folder = Path('student_dir/')
    pth = 'student_dir/'
    pattern = '.txt'
    scores = {}
    for root, dirs, files in os.walk(pth):
        for file in files:
            name_student = file[:-(len(pattern))]
            textfile = file  # текущий файл студента

            filename = data_folder / file
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
            text_clean = text_clean.replace(':', '')  # replacing hyphens with whitespace
            text_clean = text_clean.replace(';', '')  # replacing hyphens with whitespace
            text_clean = text_clean.replace('*', '')  # replacing hyphens with whitespace
            text_clean = text_clean.replace('•', '')  # replacing hyphens with whitespace
            text_clean = text_clean.replace('#', '')  # replacing hyphens with whitespace
            text_clean = text_clean.replace('»', '')  # replacing hyphens with whitespace —
            text_clean = text_clean.replace('—', '')  # replacing hyphens with whitespace
            text_clean = text_clean.replace('\xa0', ' ')  # replacing hyphens with whitespace
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
            # print(len(sentences))
            global korpus_stud
            korpus_stud = len(sentences)
            print('korpus_stud=', korpus_stud)
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
            a_to_m = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
                      'у',
                      'ф',
                      'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё']
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
            a_to_m = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
                      'у',
                      'ф',
                      'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё']
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
            global korpus, freqstud
            freqstud = 'Частота встречаемости слов студента'
            # очистка текста преподавателя применяя словарь стоп-слов используем ~
            korpus = 'Корпус студента ' + name_student
            df_stud = df1.copy()
            df_stud_clear = df_stud[~df_stud.Word.isin(df_stop.stop_ru)].reset_index(drop=True)
            df_stud_clear.rename(columns={'Word': korpus}, inplace=True)
            # print(df_stud_clear.sort_values(by ='Frequency', ascending = 0).reset_index(drop=True))
            # print(df_teach_clear.count())
            global df_stud_clear2
            df_stud_clear2 = df_stud_clear.sort_values(by='Frequency', ascending=0).reset_index(drop=True)
            df_stud_clear2.rename(columns={'Frequency': freqstud}, inplace=True)
            # print(df_stud_clear2)
            # Plotting the top 50
            # setting the figure size

            global korpus_stud_lemma
            korpus_stud_lemma = len(df_stud_clear2.index)
            print('korpus_stud_lemma=', korpus_stud_lemma)

            # with pd.ExcelWriter('static/downloads/student/Korpus_{0}.xlsx'.format(name_student)) as writer:
            with pd.ExcelWriter('static/downloads/student/Korpus_student.xlsx') as writer:
                df_stud_clear2.to_excel(writer, sheet_name='КорпусСлов')

            original= pd.concat([original, df_stud_clear2], axis=1)

            fig = plt.figure(figsize=(20, 10))
            # creating a bar plot
            ax = sns.barplot(x=korpus, y=freqstud, data=df_stud_clear2.head(50))
            # rotating the x axis labels
            ax.set_xticklabels(labels=df_stud_clear2.head(50)[korpus], rotation=75)
            # setting the title
            ax.set_title("Frequency  Student's korpus words ")
            # setting the Y-axis labels
            ax.set_ylabel(freqstud)
            # Labelling the bars in the bar graph
            for p in ax.patches:
                ax.annotate(p.get_height(), (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')
            fig.tight_layout()
            plt.savefig('static/img/rezult/rez_stud/Korpus.jpg')
            # plt.show()

            # path2 = 'rezult/rez_stud/'
            # os.chdir(path2)
            # os.rename('Korpus.jpg', 'Корпус_студента_' + name_student + '.jpg')
            # os.chdir(saved_cwd)

            # Частотный анализ слов студента в корпусе текстов преподавателя
            df_teach = teach_words()
            # print(df_teach)
            # print(df_teach)
            # print(df_teach.count())
            name_t = teach_name()

            df_stud_clear3 = df_stud_clear
            df_stud_clear3.rename(columns={korpus: 'korpusStud'}, inplace=True)
            df_teach.rename(columns={teach_series_name(): 'korpusTeach'}, inplace=True)
            # частота совпадений студента c корпусом данных
            df_student_ok = df_stud_clear3[df_stud_clear3.korpusStud.isin(df_teach.korpusTeach)].reset_index(drop=True)

            # sovpadenie='Частотное совпадение Корпуса студента ' +res+ 'с корпусом ' + name_t
            df_student_ok.rename(columns={'korpusStud': 'sovpadenie'}, inplace=True)
            df_student_ok.rename(columns={'Frequency': freqstud}, inplace=True)
            # print(df_student_ok.sort_values(by='FrStudent', ascending=0).reset_index(drop=True))
            # print(df_student_ok.count())

            # частота совпадений преподавателя c  словами студента- для определения частоты встречаемости слов у преподавателя, которые использовал студент
            df_work2 = df_teach.copy()
            df_teach_ok = df_work2[df_work2.korpusTeach.isin(df_stud_clear3.korpusStud)].reset_index(drop=True)
            df_teach_ok.rename(columns={'korpusTeach': 'sovpadenie'}, inplace=True)
            df_teach_ok.rename(columns={'Frequency': 'FrTch'}, inplace=True)

            # Объединяем частоты студента и преподавателя
            global res
            res = df_teach_ok.merge(df_student_ok)
            # print(res.sort_values(by='FrTch', ascending=0).reset_index(drop=True))
            # print(res)
            global korpus_stud_sovp
            korpus_stud_sovp = len(res.index)
            print('korpus_stud_lemma=', korpus_stud_sovp)

            x = res['sovpadenie'].values.tolist()
            res.plot(kind='bar', figsize=(25, 8))
            x_pos = [i for i, _ in enumerate(x)]
            plt.xlabel('Слово')
            plt.ylabel(freqstud)

            plt.title('Частотный анализ текста преподавателя  и студента ')
            plt.xticks(x_pos, x)
            plt.title('Частотный анализ текстов преподавателя ' + name_t + ' и студента ' + name_student)
            fig.tight_layout()
            plt.savefig('static/img/rezult/rez_teach/vs.jpg')
            # plt.show()

            # path2 = 'rezult/rez_teach/'
            # os.chdir(path2)
            # os.rename('vs.jpg', 'Частотный анализ текстов преподавателя ' + name_t + ' и студента ' + name_student + '.jpg')
            # os.chdir(saved_cwd)
            global rez_stud2
            rez_stud2 = ( name_student, korpus_stud, korpus_stud_lemma, korpus_stud_sovp)
            rez_stud = rez_stud2
            #print(textfile)
            nt = round(korpus_stud / rez_teach[0], 2)
            nk = round(korpus_stud_lemma / rez_teach[1], 2)
            nks = round(korpus_stud_sovp / rez_teach[1], 2)
            ss = round(1 / abs(math.log((korpus_stud / rez_teach[0]) / (korpus_stud_sovp / rez_teach[1]))), 3)
            new_row = {"ФИО": name_student, "Корпус слов С": korpus_stud, "Корпус лемма-слов С": korpus_stud_lemma,
                       "Совпадение слов": korpus_stud_sovp, "Коэф. норм. текста": nt, "Коэф. норм. корпуса": nk,
                       "Коэф. норм. корпуса совпадений": nks, "Коэфициент схожести": ss}
            df_marks = df_marks.append(new_row, ignore_index=True)

            scoress['{0}'.format(name_student)] = rez_stud
    #print(scoress.values())
    df1 = df_marks.set_index("ФИО")
    # print(df1)
    with pd.ExcelWriter('static/downloads/student/rezult.xlsx') as writer:
        df1.to_excel(writer, sheet_name='ТАСИ')
    with pd.ExcelWriter('static/downloads/student/studrezall.xlsx') as writer:
        original.to_excel(writer, sheet_name='ТАСИ')

    return scoress

def table_rez_all():
    alg_stud()
    rez_teach=teach_alg()
    list_of_tuples=[]
    for value in scoress.values():
            rez_student1=value
            rez_te_table = rezteacher()  # rez_teach=(korpus_teach, korpus_teach_lemma)
            #print(value)
            nt = (round(rez_student1[1] / rez_teach[0], 2),)
            nk = (round(rez_student1[2] / rez_teach[1], 2),)
            nks = (round(rez_student1[3] / rez_teach[1], 2),)
            ss =(round(1/abs(math.log((rez_student1[1] / rez_teach[0])/ (rez_student1[3] / rez_teach[1]))),3),)#(round(1 / abs(math.log((rez_student1[0] / rez_teach[0]) / (rez_student1[2] / rez_teach[1]))), 3),)
            normal_text = (nt, nk, nks, ss)
            rez =rez_student1 + normal_text[0] + normal_text[1] + normal_text[2] + normal_text[3]
            #print(rez)
            list_of_tuples.append(rez)
    return list_of_tuples



def rezstud():
    r = rez_stud2
    return r

def rezstudimage():
    r = df_stud_clear2
    return r

def namestud():
    r = korpus
    return r

def freqstudimage():
    r = freqstud
    return r

def resimage():
    r = res
    return r