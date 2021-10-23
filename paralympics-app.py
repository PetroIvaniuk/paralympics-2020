import streamlit as st
import pandas as pd
from  library.plot_helper import get_medal_athlete_list, get_label_number_list, get_label_number_double_list
from  library.plot_helper import (plot_medals, plot_medalists, plot_discipline_bar, 
                                  plot_discipline_double, plot_medals_bar, plot_label)

def main():
    pages = {
        "Country":page_first,
        "Discipline":page_second,
        "Top Medalists": page_third,
        "Medals": page_fourth,
        "About": page_fifth,
    }

    st.set_page_config(page_title='Tokyo 2020 Paralympics', layout="wide")
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    _, col01, _ = st.columns((2, 2, 2))
    with col01:
        st.title('Tokyo 2020 Paralympics')
        page = st.radio('', tuple(pages.keys()))
    pages[page]()

def page_first():
    with st.container():
        _, col11, _ = st.columns((1, 3, 1))
        with col11:
            countries_unique = sorted(df_medalists['Country'].unique())
            selected_country = st.selectbox(label='Select a Country:', 
                                            options=countries_unique, 
                                            index=82)
            df_medalists_selected = df_medalists[(df_medalists['Country']==selected_country)]
            df_medalists_athlete_selected = df_medalists_athlete[(df_medalists_athlete['Country']==selected_country)]
            df_medals_selected = df_medals_total[(df_medals_total['Country']==selected_country)]

        _, col121, _, col122, _ = st.columns((1, 1, 0.1, 1, 1))
        with col121:
            st.subheader('{} Medals:   '.format(selected_country))
            df_medals_country = df_medals_selected[['Gold','Silver', 'Bronze']].T.reset_index()
            medals_country_list = get_label_number_list(df_medals_country)
            plot_medals_bar(medals_country_list)

        with col122:
            st.subheader('{} Medalists:'.format(selected_country))
            df_medalists_country = df_medalists_selected[['Gold','Silver', 'Bronze']].T.sum(axis=1).reset_index()
            medalists_country_list = get_label_number_list(df_medalists_country)
            plot_medals_bar(medalists_country_list)

        _, col131, _ = st.columns((2, 2, 2))
        with col131:
            st.subheader('All Medalists from {} by Discipline:'.format(selected_country))
            df_medalists_discipline = df_medalists_selected.groupby(['Discipline'])['Total'].sum().reset_index()\
                                                                                            .sort_values('Total')
            medal_discipline_list = get_label_number_list(df_medalists_discipline)
            medal_discipline_list = [('\n'.join(i[0].split(' ')), i[1]) for i in medal_discipline_list]
            plot_discipline_bar(medal_discipline_list)

            st.subheader('All Medalists from {}:'.format(selected_country))
            medalists_list = get_medal_athlete_list(df_medalists_athlete_selected)
            plot_medalists(medalists_list, img_path_medal, img_path_flag, img_path_dis, flag=False)
            st.write('* Two pictograms on the plot mean the athlete won medals in two separate disciplines.')

def page_second():
    with st.container():

        _, col21, _ = st.columns((1, 3, 1))
        with col21:
            disciplines_unique = sorted(df_medalists['Discipline'].unique())
            selected_discipline = st.selectbox(label='Select a Discipline:', 
                                            options=disciplines_unique, 
                                            index=0)

        _, col22, _ = st.columns((3, 1, 3))
        with col22:
            plot_label()

        _, col23, _ = st.columns((1, 3, 1))
        with col23:
            cols_gr_sort = ['Gold', 'Silver', 'Bronze', 'Total']
            cols_medal_rename = {'Gold Medal':'Gold', 'Silver Medal':'Silver', 'Bronze Medal':'Bronze'}
            df_dis_medalists = df_medalists[df_medalists['Discipline']==selected_discipline]\
                                            .groupby('Country')[cols_gr_sort]\
                                            .sum().sort_values('Total', ascending=False).reset_index()

            df_dis_medals = df_medals[df_medals['Discipline']==selected_discipline]\
                                            .pivot_table('medal_code', 'Country', 'medal_type', 'count')\
                                            .fillna(0).astype(int)
            df_dis_medals['Total'] = df_dis_medals.sum(axis=1)
            df_dis_medals = df_dis_medals.rename(columns=cols_medal_rename) 

            df_dis = df_dis_medals.merge(df_dis_medalists, right_on='Country', left_on='Country')\
                                  .sort_values('Total_x', ascending=False).reset_index(drop=True)

            discipline_country_list = get_label_number_double_list(df_dis)
            plot_discipline_double(discipline_country_list)

def page_third():
    with st.container():
        _, col31, _ = st.columns((1, 2, 1))
        with col31:
            medalists_top_list = get_medal_athlete_list(df_medalists_athlete[df_medalists_athlete['Total']>3])
            plot_medalists(medalists_top_list, img_path_medal, img_path_flag, img_path_dis, flag=True)
            st.write('* All Top Paralympic Medalists who won more than 3 medals.')

def page_fourth():
    with st.container():
        _, col41, _ = st.columns((1, 2, 1))
        with col41:
            plot_medals(df_medals_total)

def page_fifth():
    with st.container():
        _, col51, _ = st.columns((2, 2, 2))
        with col51:
            st.write(
                """
                Thanks for checking out my app! It was built entirely using 
                [matplotlib](https://matplotlib.org/) and 
                [Tokyo 2020 Paralympics](https://www.kaggle.com/piterfm/tokyo-2020-paralympics) data.
                
                This application is a dashboard that runs an analysis of Tokyo 2020 Paralympics results.
                You can find all medals and medalists distributions with the possibility 
                to look into country and/or discipline. 

                Flags pictures from [SOURCE FLAGS](https://github.com/linuxmint/flags).

                If you are interested in sport data you can check 
                [Tokyo 2020 Olympics](https://www.kaggle.com/piterfm/tokyo-2020-olympics) and 
                [Olympic Games, 1986-2018](https://www.kaggle.com/piterfm/olympic-games-medals-19862018)

                I hope you enjoy!

                #### **Contacts:**
                [![](https://img.shields.io/badge/GitHub-Follow-informational)](https://github.com/PetroIvaniuk)

                [![](https://img.shields.io/badge/Linkedin-Connect-informational)](https://www.linkedin.com/in/petro-ivaniuk-68a89432/)
                ###### © Petro Ivaniuk, 2021

                """)

if __name__ == "__main__":

    path_medals = 'data/medals.pkl'
    path_medals_total = 'data/medals_total.csv'
    path_medalists = 'data/medalists.pkl'
    path_medalists_athlete = 'data/medalists_athlete.pkl'

    img_path_flag = 'img/icon_flags/'
    img_path_medal = 'img/medals/'
    img_path_dis = 'img/paralympic/'

    df_medals = pd.read_pickle(path_medals)
    df_medals_total = pd.read_csv(path_medals_total)
    df_medalists = pd.read_pickle(path_medalists)
    df_medalists_athlete = pd.read_pickle(path_medalists_athlete)

    main()
