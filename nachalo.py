import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('suevey.csv')  # https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey


def Bayes():
    return False


ft_names = df.columns.tolist()
# это массив с названиями столбцов
#for column in ft_names:
    #print(column)
    #print(df[column].value_counts(dropna=False))

df = df.rename(columns={'Age': 'age'})
df.age = df.age[df.age.isin(range(15, 100))]  # с помщью хитропопных манипуляций я смогла отфилтровать
# (сама не поняла что написала) ыыыыыыыы

male = "Male,M,m,Man,Make,cis male,Male,maile,Mail,msle,Male,Male-ish,Male (CIS),Cis Man,Cis Male,Malr"
female = "Female,femail,female,F,f,Woman, Cis Female,woman,Female,Femake,Female (cis),cis-female/femme,"
df.Gender = pd.Series(map(lambda a: 'M' if (a in male) else 'F' if (a in female) else 'HZ', df.Gender))
#print(df['Gender'].value_counts(dropna=False)) #вывести гендеры

df.work_interfere = pd.Series(map(lambda a: 0 if (a == "Never")
                                        else 1 if (a == "Rarely")
                                        else 2 if (a == "Sometimes")
                                        else 3 if (a == "Often") else 'NaN', df.work_interfere))
#print(df['work_interfere'].value_counts(dropna=False))

polezno = ['6-25', '26-100', '100-500', '1-5', '500-1000', 'More than 1000']
df.no_employees = pd.Series(map(lambda a: 0 if (a == polezno[0])
                                     else 1 if (a == polezno[1])
                                     else 2 if (a == polezno[2])
                                     else 3 if (a == polezno[3])
                                     else 4 if (a == polezno[4])
                                     else 5 if (a == polezno[5]) else 'NaN', df.no_employees))
polezno_leave = ['Very easy', 'Somewhat easy', "Don't know", 'Somewhat difficult', 'Very difficult']
df.leave = pd.Series(map(lambda a: 0 if (a == polezno_leave[0])
                              else 1 if (a == polezno_leave[1])
                              else 2 if (a == polezno_leave[2])
                              else 3 if (a == polezno_leave[3])
                              else 4 if (a == polezno_leave[4]) else 'NaN', df.leave))

polizno_bin = ['self_employed', 'family_history', 'treatment', 'remote_work', 'tech_company',
               'benefits', 'care_options', 'wellness_program', 'seek_help', 'anonymity',
               'mental_health_consequence', 'phys_health_consequence', 'coworkers', 'supervisor',
               'mental_health_interview', 'phys_health_interview', 'mental_vs_physical', 'obs_consequence']

for i in polizno_bin:
    df[i] = pd.Series(map(lambda a: 0 if (a == "No") else 1 if (a == "Yes") else 'nan', df[i]))
    #print(df[i].value_counts(dropna=False))

df.to_csv(r'..\newsurvey.csv', index=False)
#_______________________________________________________________________
# статистический анализ
print('_______________________________________________________________________')
print('СЧИТАЕМ ДИСПЕРСИЮ')
print('_______________________________________________________________________')
df1 = pd.read_csv('newsurvey.csv')
#df1.drop(columns = df1.columns[0], axis=1, inplace=True)
colum_name = df1.columns.tolist()
#print(colum_name)
colum_name.remove('Timestamp')
colum_name.remove('Gender')
colum_name.remove('Country')
colum_name.remove('state')
colum_name.remove('comments')
#print(colum_name)

for i in colum_name:
    k = "'" + i + "': "
    print("%10s %-30s %5.5f" % ("Дисперсия столбца", k, df1[i].std()))
#("Дисперсия столбца ", "'", i, "': ", df1[i].std(), sep='')       print("%50s %15.5f" % (k, df1[i].std()))

print()
#_______________________________________________________________________
#СЧИТАЕМ ДОЛИ
print('_______________________________________________________________________')
print('СЧИТАЕМ ДОЛИ')
print('_______________________________________________________________________')
'''
test_list = pd.Series(df1.age.value_counts(dropna=False))
count_people = sum(test_list.values)
kl = pd.Series(test_list.keys()) #сколько всего человек
doli_age = pd.Series(map(lambda a, b: b/count_people, kl, test_list.values)) #формула
#print(doli_age)
#test_dict = pd.DataFrame([kl[i], doli_age[i]] for i in range(len(kl))) #словарь где индекс это 0,1,2
test_dict = pd.DataFrame(doli_age, columns=['doli']) #соединяем в словарь
test_dict.index = kl
test_dict.index.name = 'age'
print(test_dict)
'''

#part2.index.name = 'ind'
#print(colum_name)
colum_name2 = colum_name.copy()
colum_name2.remove('no_employees')
colum_name2.remove('age')
colum_name2.remove('leave')
colum_name2.remove('work_interfere')

#print(part2)
help = {}
doli_y_n_nan = pd.DataFrame(help)
doli_age = pd.DataFrame(help)
doli_no_employees = pd.DataFrame(help)
doli_leave = pd.DataFrame(help)
doli_work_interfere = pd.DataFrame(help)

for i in colum_name:
    print("Доли", df1.groupby(i).size()/len(df1))
    doli = pd.DataFrame(df.groupby(i).size() / len(df), columns=[i])  # запись просматриваемого столбика
    if i in colum_name2:
        doli_y_n_nan = pd.concat([doli_y_n_nan, doli], axis=1)  # добавления просматриваемого столбца
    if i == 'age':
        doli_age = pd.concat([doli_age, doli], axis=1)
    if i == 'no_employees':
        doli_no_employees = pd.concat([doli_no_employees, doli], axis=1)
    if i == 'leave':
        doli_leave = pd.concat([doli_leave, doli], axis=1)
    if i == 'work_interfere':
        doli_work_interfere = pd.concat([doli_work_interfere, doli], axis=1)
    print()

print(doli_y_n_nan)
'''# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', 10)'''
print(doli_y_n_nan)

print(df1.describe()) # жирная статистика чтобы было

#---------------------------------------------------------
# поиск полей
#---------------------------------------------------------












#print(df1.describe().loc[['std']])

######print(df['age'].value_counts(dropna=False))
#######print(df.age.nunique())

#plt.plot(kl, list(test_list.values()))
#df1['age'].plot.hist(bins=df.age.nunique())
#df1['age'].plot.hist(bins=len(df['age'].value_counts(dropna=False)), label='age')
plt.show()

#####print(df1.groupby('age').size())

num_emp = 1000
age_le20 = 250
age_bw31_45 = 400
age_bw20_30 = 300
age_gt45 = 50

gen_m = 500
gen_f = 400
gen_x = 100

com_le500 = 700
com_gt500 = 300

gen_m_bw20_30 = 1
age_bw20_30_com_le500 = 1
com_le500_gen_m = 1
age_bw20_30_gen_m_com_le500 = 1
# условно решим, что когда вероятность > .5, то все так и есть
p_m_a30_le500 = gen_m / num_emp * age_bw20_30 / num_emp * com_le500 / num_emp
norm_c = (gen_m + age_bw20_30 + com_le500 - gen_m_bw20_30 - age_bw20_30_com_le500 - com_le500_gen_m -
          age_bw20_30_gen_m_com_le500) / num_emp

# features = df.drop('treatment', 1)
# labels = df['treatment']
