# imports ----------------------------------------------------------------------
import streamlit as st
import pandas as pd

# ref this for gantt chart https://towardsdatascience.com/gantt-charts-with-pythons-matplotlib-395b7af72d72
import matplotlib.pyplot as plt
import numpy as np
from pandas import Timestamp

# Initialisation ----------------------------------------------------------------------

st.set_page_config(
    page_title="Fika",
    page_icon="👌",
    layout="centered"
)

# Datasets
df = pd.read_csv("fika_data.csv", parse_dates=[4,5])

# Sidebar ------------------------------------------------------------------------------
with st.sidebar:
    st.subheader("Choose a Feature")
    sections = ['Kanban', 'Roadmap']
    selected_sect = st.selectbox("View Mode", sections)

# Section one: Kanban View --------------------------------------------------------------

if selected_sect == 'Kanban':
    st.title("Kanban")
    # st.subheader("Let's guess your MBTI...")
    # user_input = st.text_input(value="", label= "Enter some text here" , help = "Type something here, then press the Enter!")

    df = pd.read_csv("fika_data.csv") # added in case df values are changed in roadmap mode.
    # for card bootstrap ux: https://discuss.streamlit.io/t/is-it-possible-to-convert-dataframe-records-into-bootstrap-card/20134/4


    tab1, tab2, tab3 = st.tabs(["Kanban", "Overview", "Add Task"])

    with tab1:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Backlog")
            st.write(df[df['status'] == 'Backlog'])

        with col2:
            st.subheader("To-Do")
            st.write(df[df['status'] == 'To Do'])

        with col3:
            st.subheader("In Progress")
            st.write(df[df['status'] == 'In Progress'])
        
        with col4:
            st.subheader("Done")
            st.write(df[df['status'] == 'Done'])
            
    with tab2:
        st.subheader("Task Overview")
        st.write(df)

    with tab3:
        # form
        cnt=0

        st.subheader("New Task")

        form = st.form(key='form1', clear_on_submit=True)

        inp_0 = (df.tail(1).index).start + 2 # append task id based on index
        inp_1 = form.text_input(label= "Product", key=cnt)
        inp_2 = form.text_input(label= "Task", key=cnt+1)
        inp_3 = form.text_input(label= "Action owner", key=cnt+2)
        # inp_4 = form.text_input(label= "Status", key=cnt+3)
        inp_4 = form.selectbox('Status?',('Backlog', 'To Do', 'In Progress', 'Done'), key=cnt+3)
        inp_5 = form.date_input(label= "Start Date", key=cnt+4)
        inp_6 = form.date_input(label= "End Date", key=cnt+5)
        inp_7 = form.text_input(label= "Completion %", key=cnt+6) # Add number picker

        submit_btn = form.form_submit_button(label='Add')

        if submit_btn:
            new_df = {'id':inp_0, 'product':inp_1, 'task':inp_2, 'action_owner':inp_3,
            'status':inp_4, 'start':inp_5, 'end':inp_6, 'c_percent':inp_7}
            st.write(new_df)
            df = pd.concat([df, pd.DataFrame([new_df])], ignore_index=True)
            df.to_csv("fika_data.csv", index=False)

# Section two: Timeline View ------------------------------------------------------------

elif selected_sect == 'Roadmap':
    st.title("Roadmap")

    df = pd.read_csv("fika_data.csv")
    # Selection Dropdown - To implement for product type
    # https://towardsdatascience.com/gantt-charts-with-pythons-matplotlib-395b7af72d72

    df[['start', 'end']] = df[['start', 'end']].apply(pd.to_datetime)
    # project start date
    proj_start = df.start.min()
    # number of days from project start to task start
    df['start_num'] = (df.start-proj_start).dt.days
    # number of days from project start to end of tasks
    df['end_num'] = (df.end-proj_start).dt.days
    # days between start and end of each task
    df['days_start_to_end'] = df.end_num - df.start_num
    df['current_num'] = (df.days_start_to_end * df.c_percent)



    from matplotlib.patches import Patch

    fig, ax = plt.subplots(1, figsize=(16,6))
    # bars
    ax.barh(df.task, df.current_num, left=df.start_num, color='orange')
    ax.barh(df.task, df.days_start_to_end, left=df.start_num, alpha=0.5, color='orange')
    # texts
    for idx, row in df.iterrows():
        ax.text(row.end_num+0.1, idx, 
                f"{int(row.c_percent*100)}%", 
                va='center', alpha=0.8)


    ##### TICKS #####
    xticks = np.arange(0, df.end_num.max()+1, 3)
    xticks_labels = pd.date_range(proj_start, end=df.end.max()).strftime("%m/%d")
    xticks_minor = np.arange(0, df.end_num.max()+1, 1)
    ax.set_xticks(xticks)
    ax.set_xticks(xticks_minor, minor=True)
    ax.set_xticklabels(xticks_labels[::3])

    st.pyplot(fig)