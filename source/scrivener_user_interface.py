"""
Copyright (c) 2021 Anshul Patel
This code is licensed under MIT license (see LICENSE.MD for details)

@author: Scrivener
"""

# Import Libraries
import streamlit as st
import re
import os
from main.transcribe import TranscribeVideo
from main.transcribe_yt import TranscribeYtVideo
import secrets
from glob import glob


# Download the uploaded video file
def save_file(file):
    with open(os.path.join(os.getcwd(), file.name), 'wb') as f:
        f.write(file.getbuffer())
    return 

# Display Image
# st.image("../media/logo/logo.gif")

st.title(":sunflower:Transcriptor!")
st.markdown("""
    Transcriptor is a summarization tool which uses video transcripts to generate a 
    concise summary for the content of any given video. Currently, Transcriptor supports
    summarization of YouTube and local video files.
""")
st.subheader("Choose a video to start")
# Display Radio options
input_format = st.radio('Choose your input format', ['Youtube Link', 'Upload a Video'])

# If user provides a Youtube Link
if input_format=='Youtube Link':
    # Text input box 
    youtube_link = st.text_input('Enter Youtube Link')
    # Check if its a valid youtube link
    if re.findall('(www\.youtube\.com\/watch\?v=)',youtube_link):
        st.video(youtube_link)
        # Make a progress bar
        progress_bar = st.progress(0)
        # Decorative material
        progress_lines = secrets.choice(['Hired Shakespeare to summarize your video', 'Taking advice from Charles Dickens to help you',
                                        'Shakespeare is completing the assignment', 'Do not worry, Mark Twain is on it',
                                        'Robert Frost is taking the right road to summarize your video'])
        progress_bar.progress(10)
        
        # Wait till we run the summarization
        with st.spinner(progress_lines+' . . .'):
            progress_bar.progress(25)
            # Call TranscribeYtVideo class 
            transcribe_video = TranscribeYtVideo(youtube_link)
            progress_bar.progress(40)
            # Get summary
            summary = transcribe_video.transcribe_yt_video()
            progress_bar.progress(80)
        # Complete progress bar to 100
        progress_bar.progress(100)
        # Display Summary
        st.header('Summary')
        st.write(summary)
        
    
    # If user inputs an invalid Youtube link
    elif youtube_link!='':
        st.error('Please enter a valid Youtube Link!')

# If user uploads a local video    
elif input_format=='Upload a Video':
    # Browse button for uploading .mp4 files
    file = st.file_uploader('Upload a video',type=['mp4'],accept_multiple_files=False)
    if file is not None:
        st.video(file)
        # Make a progress bar
        progress_bar = st.progress(0)
        progress_bar.progress(10)
        # Decorative material
        progress_lines = secrets.choice(['Hired Shakespeare to summarize your video', 'Taking advice from Charles Dickens to help you',
                                        'Shakespeare is completing the assignment', 'Do not worry, Mark Twain is on it',
                                        'Robert Frost is taking the right road to summarize your video'])
        # Wait till we run the summarization
        with st.spinner(progress_lines+' . . .'):
            progress_bar.progress(25)
            # Download the uploaded video file
            save_file(file)
            progress_bar.progress(40)
            # Call TranscribeVideo class 
            transcribe_video = TranscribeVideo()
            progress_bar.progress(60)
            # Get summary
            summary = transcribe_video.transcribe_video(os.path.join(os.getcwd(), file.name))
        # Complete progress bar to 100
        progress_bar.progress(100)
        # Display Summary
        st.header('Summary')
        st.write(summary)
    else:
        for name in glob('*.mp4'):
            os.remove(name)
