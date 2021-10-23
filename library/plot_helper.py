import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def convert_column(column):
    return column.to_list()[::-1]

def get_medal_athlete_list(df):
    athlete_name = convert_column(df['Athlete Name'])
    country_iso = convert_column(df['Country ISO'])
    dis_code = convert_column(df['Discipline Code'])
    medals_total = convert_column(df['Total'])
    medals_b = convert_column(df['Bronze'])
    medals_bs = convert_column(df['B+S'])
    output_list = list(zip(athlete_name, country_iso, dis_code, medals_total, medals_b, medals_bs))
    return output_list

def get_label_number_list(df):
    '''
    Return list of tuples from first two DataFrame columns,
    example: [('Gold', 24), ('Silver', 47), ('Bronze', 27)]
    '''
    list1 = df.iloc[:, 0].to_list()
    list2 = df.iloc[:, 1].to_list()
    output_list = list(zip(list1, list2))
    return output_list

def get_label_number_double_list(df):
    bar1 = convert_column(df['Total_x'])
    bar2 = convert_column(df['Total_y'])
    labels = convert_column(df['Country'])
    output_list = list(zip(bar1, bar2, labels))
    return output_list

def get_figsize_map(range_input, value_max):
    value_dict = {}
    for i in range(1, value_max):
        value_dict[i] = min([[np.abs(j-i), j] for j in range_input], key=lambda x: x[0])[1]
    return value_dict

def put_text(ax, patch, text, offset, va='center', fontsize=10):
    text_len = len(str(text))
    offset_text = 0.05 if text_len==1 else 0.1 if text_len==2 else 0.15
    return ax.text(patch.get_width()-offset-offset_text, 
                   patch.get_y()+patch.get_height()/2,
                   text, va=va, fontsize=fontsize)

def put_text_h(ax, patch, text, offset, va='center', fontsize=10):
    text_len = len(str(text))
    offset_text = 0.05 if text_len==1 else 0.1 if text_len==2 else 0.15
    return ax.text(text-offset-offset_text, 
                   patch.get_y()+patch.get_height()/2,
                   text, va=va, fontsize=fontsize)

def plot_medals(df):
    label_list = convert_column(df['Country'])
    value_list = df.shape[0]*[4.5]
    
    v1_list = convert_column(df['Gold'])
    v2_list = convert_column(df['Silver'])
    v3_list = convert_column(df['Bronze'])
    v4_list = convert_column(df['Total'])

    fig = plt.figure(figsize=(4, len(label_list)/4), dpi=100)
    ax = fig.add_subplot()
    bar_height = 1
    color = ['#FFFFFF' if i%2==0 else '#FAFAFA' for i in range(df.shape[0])]
    
    ax.barh(y=label_list, width=value_list, height=bar_height, color=color)
    for patch, v1, v2, v3, v4 in zip(ax.patches, v1_list, v2_list, v3_list, v4_list):
        put_text(ax, patch, v1, 3.5)
        put_text(ax, patch, v2, 2.5)
        put_text(ax, patch, v3, 1.5)
        put_text(ax, patch, v4, 0.5)
    
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none') 
    ax.spines[['top', 'bottom', 'left', 'right']].set_visible(False)

    plt.xticks([1, 2, 3, 4], ['Gold', 'Silver', 'Bronze', 'Total'])
    plt.ylim(-0.5, len(value_list) - 0.5)
    plt.xlim(0.5, 4.5)
    st.pyplot(plt)

def put_pictograme(path_img, label, shift_1, shift_2, height, value, value_height):
    img_ulr = "{}{}.png".format(path_img, label)
    img = plt.imread(img_ulr)
    extent_values = [value+shift_1, value+shift_2, value_height-height/2, value_height+height/2]
    plt.imshow(img, extent=extent_values, aspect='auto', zorder=1)
        
def plot_medalists(input_list, path_medal, path_flag, path_dis, flag=True):
    value_list = [i[3] for i in input_list]
    label_list = [i[0] for i in input_list]
    
    fig_width = max(value_list)
    fig_height = len(value_list)/2
    bar_height = 0.8
    bar_color = '#FFFFFF'
    
    fig = plt.figure(figsize=(fig_width, fig_height), dpi=100)
    ax = fig.add_subplot()
    ax.barh(y=label_list, width=value_list, height=bar_height, color=bar_color)
        
    img_medals = [ '{}{}.png'.format(path_medal, m) for m in  ['G', 'S', 'B'] ]
    img_url_g, img_url_s, img_url_b = img_medals
    img_g, img_s, img_b = plt.imread(img_url_g), plt.imread(img_url_s), plt.imread(img_url_b)

    for i, (label, label_country, label_dis, value_t, value_b, value_bs) in enumerate(input_list):
        if flag:
            put_pictograme(path_flag, label_country, 0.1, 0.9, bar_height, value_t, i)
        else:
            if len(label_dis)>1:
                put_pictograme(path_dis, label_dis[0], 0, 0.6, bar_height, value_t, i)
                put_pictograme(path_dis, label_dis[1], 0.4, 1, bar_height, value_t, i)
            else:
                put_pictograme(path_dis, label_dis[0], 0.2, 0.8, bar_height, value_t, i)

        for j in range(value_t):
            extent_values_medals = [value_t-j-0.9, value_t-j-0.1, i-bar_height/2, i+bar_height/2]
            if j<value_b:
                plt.imshow(img_b, extent=extent_values_medals, aspect='auto', zorder=1)
            elif value_b<=j<value_bs:
                plt.imshow(img_s, extent=extent_values_medals, aspect='auto', zorder=1)
            else:
                plt.imshow(img_g, extent=extent_values_medals, aspect='auto', zorder=1)
    # set ylabel lenght up to 20 characters
    plt.draw()
    ylabels_updated = []
    for ylabel in ax.get_yticklabels():
        yl_text = ylabel.get_text()
        ylabels_updated.append(yl_text if len(yl_text)<20 else yl_text[:20]+'\n'+yl_text[20:])
    ax.set_yticks(ax.get_yticks())
    ax.set_yticklabels(ylabels_updated)
    
    ax.tick_params(labelbottom=False)   
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none') 
    ax.spines[['top', 'bottom', 'right']].set_visible(False)
    plt.xlim(0, max(value_list) + 1)
    plt.ylim(-0.5, len(value_list) - 0.5)
    if fig_width>3:
        plt.tight_layout()
    st.pyplot(plt)

def plot_discipline_bar(input_list):
    label_list = [i[0] for i in input_list]
    number_list = [i[1] for i in input_list]
    
    figsize_dict = {1:(3,1), 4:(3, 2), 6:(5,5), 17:(8,8)}
    r_input = figsize_dict.keys()
    v_max = 23 # number unique discipline
    figsize_map  = get_figsize_map(r_input, v_max)
    figsize = figsize_dict.get(figsize_map.get(len(number_list)))
    fig = plt.figure(figsize=figsize, dpi=100)
    ax = fig.add_subplot()

    bar_width = 0.8
    bar_color = ['#009A17']
    ax.barh(y=label_list, width=number_list, height=bar_width, color=bar_color)
    for patch in ax.patches:
        put_text_h(ax, patch, patch.get_width(), -0.25, 'center', fontsize=12)
        
    ax.tick_params(labelbottom=False)   
    ax.xaxis.set_ticks_position('none')
    ax.spines[['top', 'bottom', 'right']].set_visible(False)
    st.pyplot(plt)

def plot_discipline_double(input_list):
    value1_list = [i[0] for i in input_list]
    value2_list = [i[1] for i in input_list]
    label_list = [i[2] for i in input_list]
    y_pos1 = np.arange(len(label_list)) - .2
    y_pos2 = np.arange(len(label_list)) + .2
    
    fig = plt.figure(figsize=(8, len(label_list)/2), dpi=100)
    ax = fig.add_subplot()
    ax.barh(label_list, width=value1_list, height=0.8, color='white')

    for patch, v1, v2 in zip(ax.patches, value1_list, value2_list):
        if v1==v2:
            put_text_h(ax, patch, patch.get_width(), -0.25, 'center', fontsize=12)
        else:
            put_text_h(ax, patch, v2, -0.25, 'bottom', fontsize=10)
            put_text_h(ax, patch, v1, -0.25, 'top', fontsize=10)

    ax.barh(y_pos1, width=value1_list, height=0.4, color='#009A17', label='Medals')
    ax.barh(y_pos2, width=value2_list, height=0.4, color='#104050', label='Medalists')

    ax.tick_params(labelbottom=False)   
    ax.xaxis.set_ticks_position('none')
    ax.spines[['top', 'bottom', 'right']].set_visible(False)
    # plt.legend()
    plt.ylim(-0.5, len(label_list) - 0.5)
    st.pyplot(plt)

def plot_medals_bar(input_list):
    medal_type_list = [i[0] for i in input_list]
    medal_number_list = [i[1] for i in input_list]

    fig = plt.figure(figsize=(3, 3), dpi=100)
    ax = fig.add_subplot()

    bar_width = 0.8
    bar_color = ['#FFD700', '#C0C0C0', '#CD7F32']
    ax.bar(medal_type_list, medal_number_list, width=bar_width, color=bar_color)

    for patch in ax.patches:
        ax.text(patch.get_x()+patch.get_width()/2, 
                patch.get_height()-patch.get_height()/2,
                patch.get_height() if patch.get_height()!=0 else '', 
                ha="center", fontsize=14) 
    ax.tick_params(labelleft=False)   
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')
    ax.spines[['top', 'left', 'right']].set_visible(False)
    st.pyplot(plt)

def plot_label():
    value_list = [1, 1]
    label_list = [' - medals', ' - medalists']
    color_list = ['#009A17', '#104050']
    
    fig = plt.figure(figsize=(0.5, 0.5), dpi=100)
    ax = fig.add_subplot()
    ax.barh(label_list, width=value_list, height=0.9, color=color_list)

    for patch, label in zip(ax.patches, label_list):
        ax.text(patch.get_width(), 
                patch.get_y()+patch.get_height()/2,
                label, va="center", fontsize=12)
        
    ax.tick_params(labelbottom=False, labelleft=False)   
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.spines[['top', 'bottom', 'right', 'left']].set_visible(False)
    st.pyplot(plt)