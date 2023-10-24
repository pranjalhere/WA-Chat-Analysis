import matplotlib.pyplot as plt
import streamlit as st
import preprocessing
import helper
import seaborn as sns
st.sidebar.title("Whats App Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessing.preprocess(data)

    #get unique users
    user_list=df['user'].unique().tolist();
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show Analysis Of",user_list)

    if st.sidebar.button("Show Analysis"):

        words,num_mess,number_of_media,links_number=helper.fetch_stats(selected_user,df)
        #stats area
        st.title("Top Stats Of Chat")
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_mess)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(number_of_media)
        with col4:
            st.header("No. of Links")
            st.title(links_number)

        #monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.month_time(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_time(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'])
        plt.xticks(rotation='vertical')
        plt.figure(figsize=(25, 15))
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        col1,col2=st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        heatmp=helper.heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax=sns.heatmap(heatmp)
        st.pyplot(fig)

        #finding the busy person
        if selected_user=='Overall':
            st.title("Most Busy User")
            x,new_df=helper.busy_user(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        #WordCloud
        st.title("Word Cloud")
        wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(wc)
        st.pyplot(fig)

        #Most Common words
        st.title("Most Common Words")
        most_comm_df=helper.most_commonwords(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_comm_df[0],most_comm_df[1])
        st.pyplot(fig)

        #emoji
        st.title("Emojies Analysis")
        emoji_df,number=helper.emoji_helper(selected_user,df)
        if(number!=0):
            emoji_df.columns = ["Emojies", "Count"]
            st.dataframe(emoji_df)
        else:
            st.header("No emoji found")



