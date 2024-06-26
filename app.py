import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

# Define sections
def home():
    st.title("Welcome to WhatsApp Chat Analyzer")
    st.markdown("""
        ## Product Description
        The WhatsApp Chat Analyzer is a powerful tool designed to help you gain insights from your WhatsApp chat data. By simply uploading your chat file, you can explore various metrics and visualizations that reveal patterns and trends in your conversations.

        ## Features
        - **Total Messages**: Count the total number of messages exchanged.
        - **Word Analysis**: Analyze the total words used in the chat.
        - **Media Analysis**: Count the number of media files shared.
        - **Link Analysis**: Count the number of links shared.
        - **Sentiment Analysis**: Understand the sentiment of the conversation.
        - **Emoji Analysis**: Analyze the emojis used in the chat.
        - **Monthly Timeline**: Visualize the number of messages sent each month.
        - **Daily Timeline**: See daily message trends.
        - **Activity Maps**: Discover the most active days and months.
        - **Word Clouds**: Generate word clouds to see the most frequently used words.
        - **Common Words**: Identify the most common words in the chat.
        - **Busy Users**: Find out who is the most active user in the group.

        ## How to Use It
        1. **Upload File**: Choose your WhatsApp chat file (in `.txt` format) from the sidebar.
        2. **Select User**: Select the user for whom you want to see the analysis or choose 'Overall' for group analysis.
        3. **View Analysis**: Click on 'Show Analysis' to view detailed insights and visualizations.

        ## Restrictions
        - The app currently supports only `.txt` files exported from WhatsApp.
        - Ensure the chat file is not too large to avoid performance issues.

        ## Memory Size
        - The app can handle files up to 200MB efficiently.
        - Larger files may take more time to process and could impact performance.

        ## Privacy and Security
        - **Data Privacy**: Your uploaded chat data is processed locally and not stored on any server.
        - **Security**: The app does not share your data with third parties. All processing is done in-memory and the data is discarded after the session ends.
        
        Enjoy analyzing your WhatsApp conversations with our interactive tools!
    """)

    # Add images
    image_path1 = "Designer.png"
    image_path = "downloadfile.jpg" # Update with the correct path to your image
    st.image(image_path, caption="WhatsApp Chat Analysis", width=400)
    st.image(image_path1, caption="WhatsApp Chat Analysis", width=400)

def analyze():
    st.title("WhatsApp Chat Analysis")
    st.sidebar.title("WhatsApp Chat Analyzer")
    uploaded_file = st.sidebar.file_uploader("Choose a file")

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)

        # fetch unique users
        user_list = df['user'].unique().tolist()
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

        if st.sidebar.button("Show Analysis"):
            # Stats Area
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
            st.title("Top Statistics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.title(words)
            with col3:
                st.header("Media Shared")
                st.title(num_media_messages)
            with col4:
                st.header("Links Shared")
                st.title(num_links)

            st.title("Sentiment Analysis")
            sentiment_df = helper.sentiment_analysis(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(sentiment_df['sentiment_label'], sentiment_df['message'], color=['red', 'blue', 'green'])
            st.pyplot(fig)

            # Emoji analysis
            st.title("Emoji Analysis")
            emoji_df = helper.emoji_helper(selected_user, df)
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
                st.pyplot(fig)

            # Monthly timeline
            st.title("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # Daily timeline
            st.title("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # Activity map
            st.title('Activity Map')
            col1, col2 = st.columns(2)

            with col1:
                st.header("Most Busy Day")
                busy_day = helper.week_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most Busy Month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            st.title("Weekly Activity Map")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)

            # Finding the busiest users in the group (Group level)
            if selected_user == 'Overall':
                st.title('Most Busy Users')
                x, new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots()

                col1, col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values, color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)

            # WordCloud
            st.title("Wordcloud")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            # Most common words
            most_common_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation='vertical')

            st.title('Most Common Words')
            st.pyplot(fig)

            # Emoji analysis (repeated)
            st.title("Emoji Analysis")
            emoji_df = helper.emoji_helper(selected_user, df)
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
                st.pyplot(fig)

def about_us():
    st.title("About Us")
    st.markdown("""
        ## About Our Team
        We are a group of passionate data scientists and software engineers dedicated to making data analysis accessible and useful for everyone. Our WhatsApp Chat Analyzer project aims to provide users with insightful analytics from their chat data in an easy-to-use interface.

        ## Our Mission
        Our mission is to empower users to gain meaningful insights from their conversations and help them understand their communication patterns better.

        ## Contact Us
        If you have any questions or feedback, feel free to reach out to us at:
        - Email: officialamit558@gmail.com.com
        - Phone: 6201793724
        - Address: Jawahar Lal Nehru Marg, Jhalana Gram, Malviya Nagar, Jaipur, Rajasthan 302017
        
        Follow us on social media:
        - Twitter: [@whatsapp_analyzer](https://twitter.com/whatsapp_analyzer)
        - LinkedIn: [WhatsApp Chat Analyzer](https://www.linkedin.com/company/whatsapp-chat-analyzer)

        Thank you for using our WhatsApp Chat Analyzer tool!
    """)

# Sidebar navigation
st.sidebar.title(" Whatsapp Chat Analyzer")
page = st.sidebar.radio("Go to", ["Home", "Analyze", "About Us"])

# Display the selected section
if page == "Home":
    home()
elif page == "Analyze":
    analyze()
elif page == "About Us":
    about_us()

