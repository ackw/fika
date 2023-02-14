# Imports ----------------------------------------------------------------------
import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
from pandas import Timestamp
from datetime import date
import datetime
from matplotlib.patches import Patch

from pandas.api.types import CategoricalDtype

# Initialisation ----------------------------------------------------------------------
st.set_page_config(page_title="Fika", page_icon="☕",layout="wide")
df = pd.read_csv("fika_data.csv", parse_dates=[4,5])

# Sidebar ------------------------------------------------------------------------------
with st.sidebar:
    sections = ['Kanban', 'Roadmap']
    selected_mode = st.selectbox("View Mode", sections)

# Section one: Kanban View -------------------------------------------------------------
if selected_mode == 'Kanban':
    df = pd.read_csv("fika_data.csv")
    # ref: https://discuss.streamlit.io/t/is-it-possible-to-convert-dataframe-records-into-bootstrap-card/20134/4
    # ref: https://getbootstrap.com/docs/5.0/components/card/#horizontal

    card_temp = """
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
                    <div class="card {} mb-3">
                        <H6 class="card-header"><b> {} {} ( # {} )</b></h6>
                            <div class="card-body">
                                <span class="card-text">👥 {} <br/> 📅 {} til {} <br/> {} {}% Complete</span><br/>
                                <hr>
                                <span class="card-text">{}</span><br/>
                            </div>
                        </div>
                    </div>
            """

    tab1, tab2, tab3 = st.tabs(["Board", "Add", "Edit"])

    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        df = pd.read_csv("fika_data.csv") 
        
        with col1:
            st.subheader("Backlog")
            df1 = df[df['status'] == 'Backlog']
            df1['priority'] = df1['priority'].astype(CategoricalDtype(['Highest', 'High', 'Medium', 'Low'],ordered=True))
            df1.sort_values(by='priority', ascending=True, inplace=True)

            
            for index, row in df1.iterrows():
                if row['status'] == 'Backlog': temp_color = 'text-white bg-secondary'
                temp_remarks = ''
                temm = row['remarks'].split('\n')
                if len(temm)<2:
                    temp_remarks = row['remarks']
                else:
                    for i in range(len(temm)):
                        temp_r = temp_remarks + temm[i] + '<br/>'
                        temp_remarks = temp_r
                    temp_remarks = temp_remarks[:-5] # removing the excesss br
                
                if row['priority'] == 'Highest': temp_prio = '❗❗❗'
                elif row['priority'] == 'High': temp_prio = '❗❗'
                elif row['priority'] == 'Medium': temp_prio = '❗'
                else: temp_prio = ''

                if row['category'] == 'Food': temp_cat = '🍕'
                elif row['category'] == 'Drink': temp_cat = '🍺'
                else: temp_cat = '📦'
                
                st.markdown(card_temp.format(temp_color, temp_prio, row['task'], str(index + 1), row['action_owner'], 
                row['start'], row['end'], temp_cat, int(row['c_percent']), temp_remarks), unsafe_allow_html=True)

        with col2:
            st.subheader("To-Do")
            df2 = df[df['status'] == 'To Do']
            df2['priority'] = df2['priority'].astype(CategoricalDtype(['Highest', 'High', 'Medium', 'Low'],ordered=True))
            df2.sort_values(by='priority', ascending=True, inplace=True)

            
            for index, row in df2.iterrows():
                if row['status'] == 'To Do': temp_color = 'text-white bg-danger'
                temp_remarks = ''
                temm = row['remarks'].split('\n')
                if len(temm)<2:
                    temp_remarks = row['remarks']
                else:
                    for i in range(len(temm)):
                        temp_r = temp_remarks + temm[i] + '<br/>'
                        temp_remarks = temp_r
                    temp_remarks = temp_remarks[:-5] # removing the excesss br
                
                if row['priority'] == 'Highest': temp_prio = '❕❕❕'
                elif row['priority'] == 'High': temp_prio = '❕❕'
                elif row['priority'] == 'Medium': temp_prio = '❕'
                else: temp_prio = ''

                if row['category'] == 'Food': temp_cat = '🍕'
                elif row['category'] == 'Drink': temp_cat = '🍺'
                else: temp_cat = '📦'
                
                st.markdown(card_temp.format(temp_color, temp_prio, row['task'], str(index + 1), row['action_owner'], 
                row['start'], row['end'], temp_cat, int(row['c_percent']), temp_remarks), unsafe_allow_html=True)

        with col3:
            st.subheader("In Progress")
            df3 = df[df['status'] == 'In Progress']
            df3['priority'] = df2['priority'].astype(CategoricalDtype(['Highest', 'High', 'Medium', 'Low'],ordered=True))
            df3.sort_values(by='priority', ascending=True)

            for index, row in df3.iterrows():
                if row['status'] == 'In Progress': temp_color = 'text-black bg-warning'
                temp_remarks = ''
                temm = row['remarks'].split('\n')
                if len(temm)<2:
                    temp_remarks = row['remarks']
                else:
                    for i in range(len(temm)):
                        temp_r = temp_remarks + temm[i] + '<br/>'
                        temp_remarks = temp_r
                    temp_remarks = temp_remarks[:-5] # removing the excesss br
                
                if row['priority'] == 'Highest': temp_prio = '❗❗❗'
                elif row['priority'] == 'High': temp_prio = '❗❗'
                elif row['priority'] == 'Medium': temp_prio = '❗'
                else: temp_prio = ''

                if row['category'] == 'Food': temp_cat = '🍕'
                elif row['category'] == 'Drink': temp_cat = '🍺'
                else: temp_cat = '📦'

                st.markdown(card_temp.format(temp_color, temp_prio, row['task'], str(index + 1), row['action_owner'], 
                row['start'], row['end'], temp_cat, int(row['c_percent']), temp_remarks), unsafe_allow_html=True)            

        with col4:
            st.subheader("Done")
            df4 = df[df['status'] == 'Done']
            df4['priority'] = df4['priority'].astype(CategoricalDtype(['Highest', 'High', 'Medium', 'Low'],ordered=True))
            df4.sort_values(by='priority', ascending=True, inplace=True)

            for index, row in df4.iterrows():
                if row['status'] == 'Done': temp_color = 'text-white bg-success'
                temp_remarks = ''
                temm = row['remarks'].split('\n')
                if len(temm)<2:
                    temp_remarks = row['remarks']
                else:
                    for i in range(len(temm)):
                        temp_r = temp_remarks + temm[i] + '<br/>'
                        temp_remarks = temp_r
                    temp_remarks = temp_remarks[:-5] # removing the excesss br

                if row['priority'] == 'Highest': temp_prio = '❗❗❗'
                elif row['priority'] == 'High': temp_prio = '❗❗'
                elif row['priority'] == 'Medium': temp_prio = '❗'
                else: temp_prio = ''

                if row['category'] == 'Food': temp_cat = '🍕'
                elif row['category'] == 'Drink': temp_cat = '🍺'
                else: temp_cat = '📦'

                st.markdown(card_temp.format(temp_color, temp_prio, row['task'], str(index + 1), row['action_owner'], 
                row['start'], row['end'], temp_cat, int(row['c_percent']), temp_remarks), unsafe_allow_html=True)

    with tab2: # add task    
        cnt = 0
        st.subheader("Add Task")
        df = pd.read_csv("fika_data.csv") 

        with st.form(key='form1', clear_on_submit=True):
            c1, c2 = st.columns(2)
            inp_0 = (df.tail(1).index).start + 2 # append task id based on index

            with c1:
                inp_1 = st.text_input(label= "Task", key=cnt+1)
                inp_3 = st.selectbox('Status',('Backlog', 'To Do', 'In Progress', 'Done'), key=cnt+3)
                inp_5 = st.selectbox('Category',('Food', 'Drink'), key=cnt+5)
                inp_7 = st.date_input(label= "Start Date", key=cnt+7)
                inp_9 = st.text_area(label= "Remarks", height = 131, key=cnt+9)

                submit_btn = st.form_submit_button(label='➕ Add')
                
            with c2:
                inp_2 = st.text_input(label= "Action owner", key=cnt+2)
                inp_4 = st.selectbox('Priority',('Highest', 'High', 'Medium', 'Low'), key=cnt+4)
                inp_6 = st.number_input(label= "Completion %", min_value=0, max_value=100, step=5, key=cnt+6)
                inp_8 = st.date_input(label= "End Date", key=cnt+8)
                            
        if submit_btn:
            new_df = {'id':inp_0, 'task':inp_1, 'category':inp_5, 'action_owner':inp_2,
            'status':inp_3, 'start':inp_7, 'end':inp_8, 'c_percent':int(inp_6), 'priority':inp_4, 'remarks':inp_9}
            
            df = pd.concat([df, pd.DataFrame([new_df])], ignore_index=True)
            df.to_csv("fika_data.csv", index=False)
            st.success('Added!')

    with tab3: # update task
        cnt = 10
        st.subheader("Edit Task")
        df = pd.read_csv("fika_data.csv") 

        inp_0 = st.number_input(label= "Populate data with Task ID", min_value=1, max_value=df.tail(1)['id'].tolist()[0], key=cnt+10, 
        help='If an error is shown, the ID entered does not exist.')

        with st.form(key='form2', clear_on_submit=True):
            c3, c4 = st.columns(2)
            
            with c3:
                inp_1 = st.text_input(label= "Task", value = df['task'][df['id'] == inp_0].values[0], key=cnt+1)
                inp_3 = st.selectbox('Status',('Backlog','To Do', 'In Progress', 'Done'), index = ['Backlog', 'To Do', 'In Progress', 'Done'].index(df['status'][df['id'] == inp_0].values[0]), key=cnt+3)
                inp_5 = st.selectbox('Category',('Food', 'Drink'), index = ['Food', 'Drink'].index(df['category'][df['id'] == inp_0].values[0]), key=cnt+5)
                inp_7 = st.date_input(label= "Start Date", value=datetime.date(int(df['start'][df['id'] == inp_0].values[0].split('-')[0]),
                int(df['start'][df['id'] == inp_0].values[0].split('-')[1]),int(df['start'][df['id'] == inp_0].values[0].split('-')[2])), key=cnt+7)
                inp_9 = st.text_area(label= "Remarks", value = df['remarks'][df['id'] == inp_0].values[0], height = 131, key=cnt+9)

                update_btn = st.form_submit_button(label='💾 Update')
                delete_btn = st.form_submit_button(label='❌ Remove')

            with c4:
                inp_2 = st.text_input(label= "Action owner", value = df['action_owner'][df['id'] == inp_0].values[0], key=cnt+2)
                inp_4 = st.selectbox('Priority',('Highest', 'High', 'Medium', 'Low'), index = ['Highest', 'High', 'Medium', 'Low'].index(df['priority'][df['id'] == inp_0].values[0]), key=cnt+4)
                inp_6 = st.number_input(label= "Completion %", min_value=0, max_value=100, value = int(df['c_percent'][df['id'] == inp_0].values[0]), step=5, key=cnt+6)
                inp_8 = st.date_input(label= "End Date", value=datetime.date(int(df['end'][df['id'] == inp_0].values[0].split('-')[0]),
                int(df['end'][df['id'] == inp_0].values[0].split('-')[1]),int(df['end'][df['id'] == inp_0].values[0].split('-')[2])), key=cnt+8)

            if update_btn:
                df = df.drop(labels=df.index[df['id']==inp_0].tolist()[0], axis=0)

                new_df = {'id':inp_0, 'task':inp_1, 'category':inp_5, 'action_owner':inp_2,
                'status':inp_3, 'start':inp_7, 'end':inp_8, 'c_percent':int(inp_6), 'priority':inp_4, 'remarks':inp_9}
                
                df = pd.concat([df, pd.DataFrame([new_df])], ignore_index=True)
                df.sort_values(by=['id'], ascending = True, inplace = True)
                df.reset_index(drop=True, inplace=True)

                df.to_csv("fika_data.csv", index=False)
                st.success('Updated!')
            
            if delete_btn:
                df = df.drop(labels=df.index[df['id']==inp_0].tolist()[0], axis=0)
                df.sort_values(by=['id'], ascending = True, inplace = True)
                df.reset_index(drop=True, inplace=True)

                df.to_csv("fika_data.csv", index=False)
                st.success('Deleted!')

# Section two: Roadmap View ------------------------------------------------------------
# ref: https://towardsdatascience.com/gantt-charts-with-pythons-matplotlib-395b7af72d72

elif selected_mode == 'Roadmap':
    df = pd.read_csv("fika_data.csv")

    df[['start', 'end']] = df[['start', 'end']].apply(pd.to_datetime)
    df.sort_values(by=['start'], ascending = False, inplace = True)
    df.reset_index(drop=True, inplace=True)
    
    proj_start = df.start.min() # project starts
    df['start_num'] = (df.start-proj_start).dt.days # from project start to start task
    df['end_num'] = (df.end-proj_start).dt.days # from project start to end task
    df['days_between'] = df.end_num - df.start_num # btwn start & end task
    df['curr_num'] = (df.days_between * ((df.c_percent)/100))

    fig, ax = plt.subplots(1, figsize=(20,10))

    # bars
    ax.barh(df.task, df.curr_num, left=df.start_num, color='green')
    ax.barh(df.task, df.days_between, left=df.start_num, alpha=0.8, color='red')

    # texts
    for idx, row in df.iterrows():
        ax.text(row.end_num+0.1, idx, f"{int(row.c_percent)}%", va='center', alpha=0.8)
        ax.text(row.start_num-0.1, idx, row.task, va='center', ha='right', alpha=0.8)

    # ticks & spines
    xticks = np.arange(0, df.end_num.max()+1, 14)
    xticks_labels = pd.date_range(proj_start, end=df.end.max()).strftime("%d/%m")
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks_labels[::14])
    
    ax.yaxis.set_ticklabels([])
    ax.tick_params(axis='y', which='both', left=False)

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['left'].set_position(('outward', 10))
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # today line
    today = pd.Timestamp(date.today())
    today = today - proj_start

    ax.axvline(today.days, color='red', lw=1, alpha=0.7)
    ax.text(today.days, len(df)+0.5, 'Today', ha='center', color='blue')

    st.pyplot(fig)