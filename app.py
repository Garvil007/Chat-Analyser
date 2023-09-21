import streamlit as st
import processor
import formater
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Chat Analyser \n (Your Best Companion for Chat Auditing)")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    # st.write(bytes_data)
    info = bytes_data.decode('utf-8')
    # st.text(info)

    data = processor.processors(info)

    users = data['user'].unique().tolist()
    users.remove('group_notification')
    users.sort()
    users.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt ", users)

    if st.sidebar.button("Show Analysis"):

        no_message,words, media_msg, links = formater.fetch_data(selected_user, data)
        st.title("Top Statistics")
        op1, op2, op3, op4 = st.columns(4)
        with op1:
            st.header("Total Messages")
            st.title(no_message)
            st.balloons()

        with op2:
            st.header("Total words")
            st.title(words)

        with op3:
            st.header("Media Shared")
            st.title(media_msg)

        with op4:
            st.header("Links Shared")
            st.title(links)


        # monthly timeline
        st.title("Monthy Timeline ")
        timeline = formater.timeline_month(selected_user, data)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'], color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Daily Timeline
        st.title("Daily Timeline ")
        dtimeline = formater.timeline_daily(selected_user, data)
        fig, ax = plt.subplots()
        ax.plot(dtimeline['day'], dtimeline['messages'], color='grey')
        st.pyplot(fig)

        #weekly activity
        st.title('Activity Map')
        op1, op2 = st.columns(2)

        with op1:
            st.header("Most active day")
            active_day = formater.activity_map_weekly(selected_user, data)
            fig, ax = plt.subplots()
            ax.bar(active_day.index, active_day.values, color='green')
            plt.xticks(rotation=60)
            st.pyplot(fig)

        with op2:
            st.header("Most active month")
            active_month = formater.activity_map_monthly(selected_user, data)
            fig, ax = plt.subplots()
            ax.bar(active_month.index, active_month.values, color='orange')
            plt.xticks(rotation=60)
            st.pyplot(fig)

        #heatmap
        st.title("Weekly Activity Map")
        activity_map = formater.heatmap(selected_user, data)
        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_map)
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.title('Most Busy Users ')
            most_busy, new_data = formater.most_busy(data)
            fig, ax = plt.subplots()

            op1, op2 = st.columns(2)

            with op1:
                ax.bar(most_busy.index, most_busy.values, color='red')
                plt.xticks(rotation=60)
                # fig2 = most_busy.plot(kind='bar')
                st.pyplot(fig)

            with op2:
                st.dataframe(new_data)


        st.title("Word Cloud")
        df_wc = formater.word_cloud(selected_user, data)
        fig2, ax2 = plt.subplots()
        ax2.imshow(df_wc)
        st.pyplot(fig2)

        mst_comm_df = formater.common_words(selected_user, data)
        st.title("Most Common Words")
        fig, ax = plt.subplots()

        ax.barh(mst_comm_df[0], mst_comm_df[1], color='aqua')
        st.pyplot(fig)

        st.dataframe(mst_comm_df)

        # emojis
        emoji_df = formater.emoji_count(selected_user, data)
        # emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
        st.title("Emoji Analysis")

        op1, op2, op3 = st.columns(3)
        with op1:
            st.dataframe(emoji_df)

        with op2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(10), labels=emoji_df[0].head(10), autopct="%0.2f")
            st.pyplot(fig)

        with op3:
             ad = 0
             if selected_user != 'overall':
                 for i in emoji_df[1]:
                     ad = ad + i
             st.title(ad)
             st.write('Emojis shared')