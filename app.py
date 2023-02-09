# Imports ----------------------------------------------------------------------
import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
from pandas import Timestamp
from datetime import date
from matplotlib.patches import Patch

# Initialisation ----------------------------------------------------------------------
st.set_page_config(page_title="Fika", page_icon="☕",layout="wide")
df = pd.read_csv("fika_data.csv", parse_dates=[4,5])

# Sidebar ------------------------------------------------------------------------------
with st.sidebar:
    st.subheader("Choose one")
    sections = ['Kanban', 'Roadmap']
    selected_mode = st.selectbox("View Mode", sections)

# Section one: Kanban View --------------------------------------------------------------
if selected_mode == 'Kanban':
    st.title("Kanban")

    df = pd.read_csv("fika_data.csv")
    # ref: https://discuss.streamlit.io/t/is-it-possible-to-convert-dataframe-records-into-bootstrap-card/20134/4
    # ref: https://getbootstrap.com/docs/5.0/components/card/#horizontal

    card_template = """
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
                    <div class="card {} mb-3">
                        <H6 class="card-header"><b># {}: {} <br/>{}</b></h5>
                            <div class="card-body">
                                <span class="card-text">{}</span><br/>
                                <hr>
                                <span class="card-text">👥 {} - {}% Complete</span><br/>
                            </div>
                        </div>
                    </div>
            """

    tab1, tab2, tab3, tab4 = st.tabs(["Kanban", "Overview", "Add", "Edit"])

    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        df = pd.read_csv("fika_data.csv") 

        with col1:
            st.subheader("Backlog")
            df1 = df[df['status'] == 'Backlog']
            
            for index, row in df1.iterrows():
                if row['status'] == 'Backlog': temp_color = 'text-white bg-secondary'
                row['c_percent'] = int(row['c_percent']*100)
                st.markdown(card_template.format(temp_color, str(index + 1), row['product'], row['task'], row['remarks'], row['action_owner'], row['c_percent']), unsafe_allow_html=True)

        with col2:
            st.subheader("To-Do")
            df2 = df[df['status'] == 'To Do']
            
            for index, row in df2.iterrows():
                if row['status'] == 'To Do': temp_color = 'text-white bg-danger'
                st.markdown(card_template.format(temp_color, str(index + 1), row['product'], row['task'], row['remarks'], row['action_owner'], int(row['c_percent'])*100), unsafe_allow_html=True)

        with col3:
            st.subheader("In Progress")
            df3 = df[df['status'] == 'In Progress']

            for index, row in df3.iterrows():
                if row['status'] == 'In Progress': temp_color = 'text-black bg-warning'
                st.markdown(card_template.format(temp_color, str(index + 1), row['product'], row['task'], row['remarks'], row['action_owner'], int(row['c_percent'])*100), unsafe_allow_html=True)
        
        with col4:
            st.subheader("Done")
            df4 = df[df['status'] == 'Done']

            for index, row in df4.iterrows():
                if row['status'] == 'Done': temp_color = 'text-white bg-success'
                st.markdown(card_template.format(temp_color, str(index + 1), row['product'], row['task'], row['remarks'], row['action_owner'], int(row['c_percent'])*100), unsafe_allow_html=True)
            
    with tab2:
        st.subheader("Task Overview")
        df = pd.read_csv("fika_data.csv") 
        st.write(df)

    with tab3: # add task    
        cnt = 0
        st.subheader("Add Task")
        df = pd.read_csv("fika_data.csv") 

        with st.form(key='form1', clear_on_submit=True):
            c1, c2 = st.columns(2)
            inp_0 = (df.tail(1).index).start + 2 # append task id based on index

            with c1:
                inp_1 = st.text_input(label= "Product", key=cnt)
                inp_3 = st.text_input(label= "Action owner", key=cnt+2)
                inp_5 = st.date_input(label= "Start Date", key=cnt+4)
                inp_7 = st.number_input(label= "Completion %", min_value=0, max_value=100, step=10, key=cnt+6) # Add number picker
                inp_7 = inp_7/100

            with c2:
                inp_2 = st.text_input(label= "Task", key=cnt+1)
                inp_4 = st.selectbox('Status',('Backlog', 'To Do', 'In Progress', 'Done'), key=cnt+3)
                inp_6 = st.date_input(label= "End Date", key=cnt+5)
                inp_8 = st.text_input(label= "Remarks", key=cnt+7)

            submit_btn = st.form_submit_button(label='Add Task')

        if submit_btn:
            new_df = {'id':inp_0, 'product':inp_1, 'task':inp_2, 'action_owner':inp_3,
            'status':inp_4, 'start':inp_5, 'end':inp_6, 'c_percent':inp_7, 'remarks':inp_8}
            
            df = pd.concat([df, pd.DataFrame([new_df])], ignore_index=True)
            df.to_csv("fika_data.csv", index=False)
            st.success('Added!')

    with tab4: # update task
        cnt = 10
        st.subheader("Edit Task")
        df = pd.read_csv("fika_data.csv") 

        
        inp_0 = st.number_input(label= "Populate data with Task ID", min_value=1, max_value=df.tail(1)['id'].tolist()[0], key=cnt-1, 
        help='If an error is shown, the ID entered does not exist.')

        with st.form(key='form2', clear_on_submit=True):
            c3, c4 = st.columns(2)

            with c3:
                inp_1 = st.text_input(label= "Product", value = df['product'][df['id'] == inp_0].values[0], key=cnt)
                inp_3 = st.text_input(label= "Action owner", value = df['action_owner'][df['id'] == inp_0].values[0], key=cnt+2)
                inp_5 = st.date_input(label= "Start Date", key=cnt+4) # fix this, need to reformat date
                inp_7 = st.number_input(label= "Completion %", min_value=0, max_value=100, step=10, key=cnt+6) # Add number picker
                inp_7 = inp_7/100
                update_btn = st.form_submit_button(label='Update Task')

            with c4:
                inp_2 = st.text_input(label= "Task", value = df['task'][df['id'] == inp_0].values[0], key=cnt+1)
                inp_4 = st.selectbox('Status',('Backlog', 'To Do', 'In Progress', 'Done'), key=cnt+3) # fix this status select box
                inp_6 = st.date_input(label= "End Date", key=cnt+5)
                inp_8 = st.text_input(label= "Remarks", value = df['remarks'][df['id'] == inp_0].values[0], key=cnt+7)
                delete_btn = st.form_submit_button(label='Delete Task')

            if update_btn:
                df = df.drop(labels=df.index[df['id']==inp_0].tolist()[0], axis=0)

                new_df = {'id':inp_0, 'product':inp_1, 'task':inp_2, 'action_owner':inp_3,
                'status':inp_4, 'start':inp_5, 'end':inp_6, 'c_percent':inp_7, 'remarks':inp_8}
                
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
    st.title("Roadmap")

    df = pd.read_csv("fika_data.csv")

    df[['start', 'end']] = df[['start', 'end']].apply(pd.to_datetime)
    df.sort_values(by=['start'], ascending = False, inplace = True)
    df.reset_index(drop=True, inplace=True)
        
    proj_start = df.start.min() # project starts
    df['start_num'] = (df.start-proj_start).dt.days # from project start to start task
    df['end_num'] = (df.end-proj_start).dt.days # from project start to end task
    df['days_between'] = df.end_num - df.start_num # btwn start & end task
    df['curr_num'] = (df.days_between * df.c_percent)

    fig, ax = plt.subplots(1, figsize=(20,10))

    # bars
    ax.barh(df.task, df.curr_num, left=df.start_num, color='green')
    ax.barh(df.task, df.days_between, left=df.start_num, alpha=0.8, color='red')

    # texts
    for idx, row in df.iterrows():
        ax.text(row.end_num+0.1, idx, f"{int(row.c_percent*100)}%", va='center', alpha=0.8)
        ax.text(row.start_num-0.1, idx, row.task, va='center', ha='right', alpha=0.8)

    # ticks & spines
    xticks = np.arange(0, df.end_num.max()+1, 3)
    xticks_labels = pd.date_range(proj_start, end=df.end.max()).strftime("%m/%d")
    xticks_minor = np.arange(0, df.end_num.max()+1, 1)
    ax.set_xticks(xticks)
    ax.set_xticks(xticks_minor, minor=True)
    ax.set_xticklabels(xticks_labels[::3])

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