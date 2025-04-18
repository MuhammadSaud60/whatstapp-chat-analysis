import streamlit as st
import preprocess, helper

st.title('Whatsapp Chat Analyzer')


file_uploader = st.sidebar.file_uploader('Choose a File')

if file_uploader is not None:

    bytes_data = file_uploader.getvalue()

    data = bytes_data.decode('utf-8')

    df = preprocess.preprocess(data)



    # Fetch users

    user_list = df['user'].unique().tolist()
    user_list.remove('System')
    user_list.sort()
    user_list.insert(0, 'Overall')

    
    selected_user = st.sidebar.selectbox('Show Analysis WRT', user_list)

    total_msgs, words, total_mf, total_emoji = helper.fetches(selected_user, df)
    


    if st.sidebar.button('Show Analysis'):

        

        
        st.title(f'{selected_user} Stats')   


        col1, col2, col3, col4 = st.columns(4)

        

        with col1:
            st.subheader('Total Messages')
            st.title(total_msgs)

        with col2:
            st.subheader('Total Words')
            st.title(words)

        with  col3:
            st.subheader('Total Media Shared')
            st.title(total_mf)


        with  col4:
            st.subheader('Total Emojis')
            st.title(total_emoji)


        
        if selected_user == 'Overall':
    
            st.title('Top 5 Active Users')
            col1, col2 = st.columns(2)
            fig, per = helper.active_users(df)
            with col1 :
                
                st.pyplot(fig)
            
            with col2:
                st.dataframe(per)

        # Monthly Timeline
        st.title('Month Timeline')
        timeline = helper.timeline(selected_user, df)
        st.pyplot(timeline)

        #day Timeline
        st.title('Day Timeline')
        perDay = helper.per_day(selected_user, df)
        st.pyplot(perDay)

        st.title('WorldCould (Most frequent words )')
        _, fig = helper.word_cloud(selected_user, df)
        st.pyplot(fig)


else:
    st.subheader('Upload Chat text file and click show analysis.')