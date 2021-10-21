import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import japanize_matplotlib
import xlrd
import seaborn as sns
import requests
from PIL import Image


st.title('時間帯データ可視化')

password = st.sidebar.text_input("暗証番号を入力",type='password')
if password == '00268':
    st.success('成功しました')
    data_file = st.file_uploader('Upload data',type=['xlsx','csv'])

    if data_file is not None :

        #AWS_BUCKET_URL = "https://drive.google.com/file/d/1DfRlDnuWYXeiRKUMUJpbE2C_-5BNt2FO/view?usp=sharing"
        #df = pd.read_csv(AWS_BUCKET_URL)
        df = pd.read_csv(data_file,encoding="shift-jis",parse_dates=True)

        df['計上日']= pd.to_datetime(df['計上日'])
        df['day'] = pd.DatetimeIndex(df['計上日']).day
        df['month'] = pd.DatetimeIndex(df['計上日']).month
        df['year'] = pd.DatetimeIndex(df['計上日']).year
        df.set_index('計上日',inplace=True)
        df['曜日'] = df.index.day_name()
        df['時間帯1'] = df['時間帯'].apply(lambda x: x[0:5])
        df.sort_values('時間帯1',inplace=True)
        #st.dataframe(df.head(100))

        col1 = st.sidebar
        col1.header('店舗を選択して下さい')




        data1 = df['店舗名'].unique()
        df1 = df.set_index('店舗名')
        option1 = col1.selectbox("店舗名",data1)
        df2_1 = df1.loc[option1]
        if option1 == '星置店' or '福井店':
            df2_1 = df2_1[df2_1['時間帯1']!='08:00']

        st.header('時間帯分析:')
        option2 = st.selectbox('分析したい項目を選択',
        ('客数', '売上金額(税抜)','荒利金額', '売上数量'))



        df_day = df[df['店舗名'] == option1]
        df_day = df_day.groupby(['計上日','曜日']).sum().reset_index()
        df_day_index = df_day['曜日'].unique()
        df_day_index = np.sort(df_day_index)


        df_day2 = df[df['店舗名'] == option1]
        df1_urage = df_day2.groupby(['計上日','day']).sum().reset_index()
        df1_urage_day = df1_urage.groupby('day').mean().reset_index()
        df_week = df1_urage_day['day'].unique()



        #st.dataframe(df1.head(10))

        

        df_Monday = df2_1[df2_1['曜日'] == 'Monday']
        df_Tuesday = df2_1[df2_1['曜日'] == 'Tuesday']
        df_Wednesday = df2_1[df2_1['曜日'] == 'Wednesday']
        df_Thursday = df2_1[df2_1['曜日'] == 'Thursday']
        df_Friday = df2_1[df2_1['曜日'] == 'Friday']
        df_Saturday = df2_1[df2_1['曜日'] == 'Saturday']
        df_Sunday = df2_1[df2_1['曜日'] == 'Sunday']

        df_Monday = df_Monday.groupby('時間帯1').mean().reset_index()
        df_Tuesday = df_Tuesday.groupby('時間帯1').mean().reset_index()
        df_Wednesday = df_Wednesday.groupby('時間帯1').mean().reset_index()
        df_Thursday = df_Thursday.groupby('時間帯1').mean().reset_index()
        df_Friday = df_Friday.groupby('時間帯1').mean().reset_index()
        df_Saturday = df_Saturday.groupby('時間帯1').mean().reset_index()
        df_Sunday = df_Sunday.groupby('時間帯1').mean().reset_index()


        d1 = df2_1[df2_1['day'] == 1]
        d2 = df2_1[df2_1['day'] == 10]
        d3 = df2_1[df2_1['day'] == 20]
        d4 = df2_1[df2_1['day'] == 30]
        df3 = pd.concat([d1, d2, d3 , d4],ignore_index=True)

        d5 = df2_1[df2_1['day'] != 1]
        d6 = df2_1[df2_1['day'] != 10]
        d7 = df2_1[df2_1['day'] != 20]
        d8 = df2_1[df2_1['day'] != 30]
        df4 = d8



        df2_weekday = df4[(df4['曜日'] != 'Sunday') & (df4['曜日'] != 'Saturday')]
        #st.dataframe(df2_weekday.head(100))

        df2_weekday = df2_weekday.groupby('時間帯1').mean().reset_index()
        df2_weekday.drop(0,inplace=True)
        x = df2_weekday['時間帯1']
        y = df2_weekday['客数']
        

        df_holiday = df4[(df4['曜日'] == 'Sunday') | (df4['曜日'] == 'Saturday')]
        df_holiday = df_holiday.groupby('時間帯1').mean().reset_index()
        df_holiday.drop(0,inplace=True)
        x1 = df_holiday['時間帯1']
        y1 = df_holiday['客数']

        df_tenweekday = df3[(df3['曜日'] != 'Sunday') & (df3['曜日'] != 'Saturday')]
        df_tenweekday = df_tenweekday.groupby('時間帯1').mean().reset_index()
        df_tenweekday.drop(0,inplace=True)
        x2 = df_tenweekday['時間帯1']
        y2 = df_tenweekday['客数']

        df_tenday_holiday = df3[(df3['曜日'] == 'Sunday') | (df3['曜日'] == 'Saturday')]
        df_tenday_holiday1 = df_tenday_holiday.groupby('時間帯1').mean().reset_index()
        x3 = df_tenday_holiday1['時間帯1']
        y3 = df_tenday_holiday1['客数']


        def small2(option2):
            plt.figure(figsize=(12,6))
            
            ax = plt.subplot()

            plt.style.use('fivethirtyeight')

            ax.plot(df_Monday['時間帯1'],df_Monday[option2],linewidth=1.0,marker="o",color='coral',label='月曜日')
            ax.plot(df_Tuesday['時間帯1'],df_Tuesday[option2],linewidth=1.0,marker="o",color='b',label='火曜日')
            ax.plot(df_Wednesday['時間帯1'],df_Wednesday[option2],linewidth=1.0,marker="o",color='r',label='水曜日')
            ax.plot(df_Thursday['時間帯1'],df_Thursday[option2],linewidth=1.0,marker="o",color='y',label='木曜日')
            ax.plot(df_Friday['時間帯1'],df_Friday[option2],linewidth=1.0,marker="o",color='m',label='金曜日')
            ax.plot(df_Saturday['時間帯1'],df_Saturday[option2],linewidth=1.0,marker="o",color='c',label='土曜日')
            ax.plot(df_Sunday['時間帯1'],df_Sunday[option2],linewidth=1.0,marker="o",color='k',label='日曜日')
            plt.xlabel('時間帯')
            plt.ylabel(option2)
            plt.legend(loc = 'upper right')
            plt.show()

    

        def small(option2):
            plt.figure(figsize=(12,6))
            
            ax = plt.subplot()

            plt.style.use('fivethirtyeight')

            ax.plot(df_Monday['時間帯1'],df_Monday[option2],linewidth=1.0,marker="o",color='coral',label='月曜日')
            ax.plot(df_Tuesday['時間帯1'],df_Tuesday[option2],linewidth=1.0,marker="o",color='b',label='火曜日')
            ax.plot(df_Wednesday['時間帯1'],df_Wednesday[option2],linewidth=1.0,marker="o",color='r',label='水曜日')
            ax.plot(df_Thursday['時間帯1'],df_Thursday[option2],linewidth=1.0,marker="o",color='y',label='木曜日')
            ax.plot(df_Friday['時間帯1'],df_Friday[option2],linewidth=1.0,marker="o",color='m',label='金曜日')
            ax.plot(df_Saturday['時間帯1'],df_Saturday[option2],linewidth=1.0,marker="o",color='c',label='土曜日')
            ax.plot(df_Sunday['時間帯1'],df_Sunday[option2],linewidth=1.0,marker="o",color='k',label='日曜日')
            plt.xlabel('時間帯')
            plt.ylabel(option2)
            plt.legend(loc = 'upper right')
            plt.show()

        def weekday(option2):
            dataset = []
            for day in df_day_index:
                dataset.append(df_day[df_day['曜日'] == day][option2].values)

            plt.figure(figsize=(15,6))
            ax = plt.subplot()
            ax.boxplot(dataset, labels=df_day_index)
            ax.set_ylabel(option2,fontsize=15)
            plt.show()
        #st.pyplot(fig)

        def day(option2):
            dataset_day = []
            for day1 in df_week:
                dataset_day.append(df1_urage[df1_urage['day'] == day1][option2].values)
            plt.figure(figsize=(9,6))
            ax = plt.subplot()

            ax.boxplot(dataset_day,labels=df_week)
            ax.set_ylabel(option2,fontsize=15)
            plt.show()


        def tenday(option1):
            plt.style.use('seaborn-deep')
            plt.figure(figsize=(12,6))

            plt.plot(x3,y3,linewidth=2.0,marker="o",color='r',label='土日５倍デー')
            plt.plot(x2,y2,linewidth=2.0,marker="o",color='b',label='平日５倍デー')
            plt.plot(x1,y1,linewidth=2.0,marker="o",color='g',label='土日')
            plt.plot(x,y,linewidth=2.0,marker="o",color='y',label='平日')
            plt.xlabel('時間帯')
            plt.ylabel('客数')
            plt.xticks(x)
            plt.legend(loc = 'upper right')
            plt.show()


        st.pyplot(small2(option2))
        st.set_option('deprecation.showPyplotGlobalUse', False)
        

        #st.markdown('時間帯客数分析:')
        #st.pyplot(small(option1))
        #st.set_option('deprecation.showPyplotGlobalUse', False)

    
        #st.write('平日５倍デー平均:',len(df2_3['中分類']))
        #st.write('土日平均:',len(df2_3['中分類']))
        #st.write('平日平均:',len(df2_3['中分類']))

        st.header('曜日ごと'+ option2)
        st.markdown('(売上見る方0.4⋇1e6(100万)=40万円,1.0⋇1e6=100万円,2.0⋇1e6(100万)=200万円)')
        st.pyplot(weekday(option2))

        st.header('日ごと'+ option2)
        st.markdown('(売上見る方0.4⋇1e6(100万)=40万円,1.0⋇1e6=100万円,2.0⋇1e6(100万)=200万円)')
        st.pyplot(day(option2))


        st.write('箱ひげ図を見ることで、平均値だけでは分からないデータの分布を把握することができます、ノイズのような異常値はデータ影響しない(上の○マークは特売日とか考えられる、下のは天気悪いとか売れない日を考えられる)')
        st.write('＊図の説明')
        st.image(r'https://cacco.co.jp/datascience/blog/wp-content/uploads/2021/01/%E7%AE%B1%E3%81%B2%E3%81%91%E3%82%99%E5%9B%B3%E4%BE%8B-790x480.png')


        if st.checkbox('5倍デーと平日の客数比較'):
            st.write('※平日と土日は５倍デーを含まない')
            st.pyplot(tenday(option1))
            st.set_option('deprecation.showPyplotGlobalUse', False)


        

        if st.checkbox('月こどで見たいならチェック入れてください'):
            col2 = st.sidebar
            data3 = df['month'].unique()
            data3 = np.sort(data3)

            df_month = df2_1.set_index('month')
            option3 = col2.selectbox("月こど",data3)


            df3_1 = df_month.loc[option3]

            

            #st.dataframe(df3_1.head(100))

            df_Monday = df3_1[df3_1['曜日'] == 'Monday']
            df_Tuesday = df3_1[df3_1['曜日'] == 'Tuesday']
            df_Wednesday = df3_1[df3_1['曜日'] == 'Wednesday']
            df_Thursday = df3_1[df3_1['曜日'] == 'Thursday']
            df_Friday = df3_1[df3_1['曜日'] == 'Friday']
            df_Saturday = df3_1[df3_1['曜日'] == 'Saturday']
            df_Sunday = df3_1[df3_1['曜日'] == 'Sunday']

            df_Monday = df_Monday.groupby('時間帯1').mean().reset_index()
            df_Tuesday = df_Tuesday.groupby('時間帯1').mean().reset_index()
            df_Wednesday = df_Wednesday.groupby('時間帯1').mean().reset_index()
            df_Thursday = df_Thursday.groupby('時間帯1').mean().reset_index()
            df_Friday = df_Friday.groupby('時間帯1').mean().reset_index()
            df_Saturday = df_Saturday.groupby('時間帯1').mean().reset_index()
            df_Sunday = df_Sunday.groupby('時間帯1').mean().reset_index()


            d1 = df_month[df_month['day'] == 1]
            d2 = df_month[df_month['day'] == 10]
            d3 = df_month[df_month['day'] == 20]
            d4 = df_month[df_month['day'] == 30]
            df3 = pd.concat([d1, d2, d3 , d4],ignore_index=True)

            d5 = df_month[df_month['day'] != 1]
            d6 = df_month[df_month['day'] != 10]
            d7 = df_month[df_month['day'] != 20]
            d8 = df_month[df_month['day'] != 30]
            df4 = d8



            df2_weekday = df4[(df4['曜日'] != 'Sunday') & (df4['曜日'] != 'Saturday')]
            #st.dataframe(df2_weekday.head(100))

            df2_weekday = df2_weekday.groupby('時間帯1').mean().reset_index()
            df2_weekday.drop(0,inplace=True)
            x = df2_weekday['時間帯1']
            y = df2_weekday['客数']
            

            df_holiday = df4[(df4['曜日'] == 'Sunday') | (df4['曜日'] == 'Saturday')]
            df_holiday = df_holiday.groupby('時間帯1').mean().reset_index()
            df_holiday.drop(0,inplace=True)
            x1 = df_holiday['時間帯1']
            y1 = df_holiday['客数']

            df_tenweekday = df3[(df3['曜日'] != 'Sunday') & (df3['曜日'] != 'Saturday')]
            df_tenweekday = df_tenweekday.groupby('時間帯1').mean().reset_index()
            df_tenweekday.drop(0,inplace=True)
            x2 = df_tenweekday['時間帯1']
            y2 = df_tenweekday['客数']

            df_tenday_holiday = df3[(df3['曜日'] == 'Sunday') | (df3['曜日'] == 'Saturday')]
            #df_tenday_holiday2 = df_tenday_holiday.gro
            df_tenday_holiday1 = df_tenday_holiday.groupby('時間帯1').mean().reset_index()
            x3 = df_tenday_holiday1['時間帯1']
            y3 = df_tenday_holiday1['客数']


            def small2(option2):
                plt.figure(figsize=(12,6))
                
                ax = plt.subplot()

                plt.style.use('fivethirtyeight')

                ax.plot(df_Monday['時間帯1'],df_Monday[option2],linewidth=1.0,marker="o",color='coral',label='月曜日')
                ax.plot(df_Tuesday['時間帯1'],df_Tuesday[option2],linewidth=1.0,marker="o",color='b',label='火曜日')
                ax.plot(df_Wednesday['時間帯1'],df_Wednesday[option2],linewidth=1.0,marker="o",color='r',label='水曜日')
                ax.plot(df_Thursday['時間帯1'],df_Thursday[option2],linewidth=1.0,marker="o",color='y',label='木曜日')
                ax.plot(df_Friday['時間帯1'],df_Friday[option2],linewidth=1.0,marker="o",color='m',label='金曜日')
                ax.plot(df_Saturday['時間帯1'],df_Saturday[option2],linewidth=1.0,marker="o",color='c',label='土曜日')
                ax.plot(df_Sunday['時間帯1'],df_Sunday[option2],linewidth=1.0,marker="o",color='k',label='日曜日')
                plt.xlabel('時間帯')
                plt.ylabel(option2)
                plt.legend(loc = 'upper right')
                plt.show()


            st.markdown('月の時間帯分析:')
            
            st.pyplot(small2(option2))
            st.set_option('deprecation.showPyplotGlobalUse', False)

        if st.checkbox('期間を指定'):

            col3 = st.sidebar
            data4 = df['month'].unique()
            data4 = np.sort(data4)

            df_month1 = df2_1.set_index('month')
            option3 = col3.selectbox("開始月",data4)

            df_month2 = df2_1.set_index('month')
            option4 = col3.selectbox("結束月",data4)

            df5 = df2_1[(df2_1['month'] >= option3) & (df2_1['month'] <= option4)]


            #st.dataframe(df5.head(100))

            df_Monday = df5[df5['曜日'] == 'Monday']
            df_Tuesday = df5[df5['曜日'] == 'Tuesday']
            df_Wednesday = df5[df5['曜日'] == 'Wednesday']
            df_Thursday = df5[df5['曜日'] == 'Thursday']
            df_Friday = df5[df5['曜日'] == 'Friday']
            df_Saturday = df5[df5['曜日'] == 'Saturday']
            df_Sunday = df5[df5['曜日'] == 'Sunday']

            df_Monday = df_Monday.groupby('時間帯1').mean().reset_index()
            df_Tuesday = df_Tuesday.groupby('時間帯1').mean().reset_index()
            df_Wednesday = df_Wednesday.groupby('時間帯1').mean().reset_index()
            df_Thursday = df_Thursday.groupby('時間帯1').mean().reset_index()
            df_Friday = df_Friday.groupby('時間帯1').mean().reset_index()
            df_Saturday = df_Saturday.groupby('時間帯1').mean().reset_index()
            df_Sunday = df_Sunday.groupby('時間帯1').mean().reset_index()


            d1 = df_month[df_month['day'] == 1]
            d2 = df_month[df_month['day'] == 10]
            d3 = df_month[df_month['day'] == 20]
            d4 = df_month[df_month['day'] == 30]
            df6 = pd.concat([d1, d2, d3 , d4],ignore_index=True)

            d5 = df_month[df_month['day'] != 1]
            d6 = df_month[df_month['day'] != 10]
            d7 = df_month[df_month['day'] != 20]
            d8 = df_month[df_month['day'] != 30]
            df7 = d8



            df2_weekday1 = df7[(df7['曜日'] != 'Sunday') & (df7['曜日'] != 'Saturday')]
            #st.dataframe(df2_weekday.head(100))

            df2_weekday1 = df2_weekday1.groupby('時間帯1').mean().reset_index()
            df2_weekday1.drop(0,inplace=True)
            x = df2_weekday1['時間帯1']
            y = df2_weekday1['客数']
            

            df_holiday = df4[(df4['曜日'] == 'Sunday') | (df4['曜日'] == 'Saturday')]
            df_holiday = df_holiday.groupby('時間帯1').mean().reset_index()
            df_holiday.drop(0,inplace=True)
            x1 = df_holiday['時間帯1']
            y1 = df_holiday['客数']

            df_tenweekday = df3[(df3['曜日'] != 'Sunday') & (df3['曜日'] != 'Saturday')]
            df_tenweekday = df_tenweekday.groupby('時間帯1').mean().reset_index()
            df_tenweekday.drop(0,inplace=True)
            x2 = df_tenweekday['時間帯1']
            y2 = df_tenweekday['客数']

            df_tenday_holiday = df3[(df3['曜日'] == 'Sunday') | (df3['曜日'] == 'Saturday')]
            #df_tenday_holiday2 = df_tenday_holiday.gro
            df_tenday_holiday1 = df_tenday_holiday.groupby('時間帯1').mean().reset_index()
            x3 = df_tenday_holiday1['時間帯1']
            y3 = df_tenday_holiday1['客数']


            def small3(option3):
                plt.figure(figsize=(12,6))
                
                ax = plt.subplot()

                plt.style.use('fivethirtyeight')

                ax.plot(df_Monday['時間帯1'],df_Monday[option2],linewidth=1.0,marker="o",color='coral',label='月曜日')
                ax.plot(df_Tuesday['時間帯1'],df_Tuesday[option2],linewidth=1.0,marker="o",color='b',label='火曜日')
                ax.plot(df_Wednesday['時間帯1'],df_Wednesday[option2],linewidth=1.0,marker="o",color='r',label='水曜日')
                ax.plot(df_Thursday['時間帯1'],df_Thursday[option2],linewidth=1.0,marker="o",color='y',label='木曜日')
                ax.plot(df_Friday['時間帯1'],df_Friday[option2],linewidth=1.0,marker="o",color='m',label='金曜日')
                ax.plot(df_Saturday['時間帯1'],df_Saturday[option2],linewidth=1.0,marker="o",color='c',label='土曜日')
                ax.plot(df_Sunday['時間帯1'],df_Sunday[option2],linewidth=1.0,marker="o",color='k',label='日曜日')
                plt.xlabel('時間帯')
                plt.ylabel(option2)
                plt.legend(loc = 'upper right')
                plt.show()


            st.markdown('月の時間帯分析:')
            
            st.pyplot(small3(option3))
            st.set_option('deprecation.showPyplotGlobalUse', False)


            
        
else:
    st.warning('パスワードが間違い')
