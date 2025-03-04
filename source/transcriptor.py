"""
Copyright (C) 2021 SE Transcriptor - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: secheaper@gmail.com
"""

# Import Libraries  
import streamlit as st
import re
import os
from main.transcribe import TranscribeVideo
from main.transcribe_yt import TranscribeYtVideo
from main.summary_to_audio import toAudio

from main.transcribe_au import TranscribeAudio
from main.helper import formatText, analyze

import secrets
from glob import glob


# Download the uploaded video file
def save_file(file):
    with open(os.path.join(os.getcwd(), file.name), 'wb') as f:
        f.write(file.getbuffer())
    return 

wittyThings = ['Hired Shakespeare to summarize your video', 'Taking advice from Charles Dickens to help you',
                                        'Shakespeare is completing the assignment', 'Do not worry, Mark Twain is on it',
                                        'Robert Frost is taking the right road to summarize your video']

# Display Image
# st.image("../media/logo/logo.gif")

st.title(":sunflower:Transcriptor!")
st.markdown("""
    Transcriptor is a summarization tool which uses video transcripts to generate a 
    concise summary for the content of any given video. Currently, Transcriptor supports
    summarization of YouTube and local video files.
""")
st.subheader("Choose a video/audio to start")
# Display Radio options
input_format = st.radio('Select an input format', ['Youtube Link', 'Upload a Video', 'Upload an Audio File (.wav)'])

# If user provides a Youtube Link
if input_format=='Youtube Link':
    # Text input box 
    youtube_link = st.text_input('Enter Youtube Link')
    # Check if its a valid youtube link
    if re.findall('(www\.youtube\.com\/watch\?v=)',youtube_link):
        # st.video(youtube_link)
        # Make a progress bar
        progress_bar = st.progress(0)
        # Decorative material
        progress_lines = secrets.choice(wittyThings)
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
        # Complete progress bar to 90
        progress_bar.progress(90)
        # Analyze sentiment
        sentiment = analyze(summary)
        # Display Summary
        st.subheader('Summary')
        st.write(formatText(summary))
        progress_bar.progress(100)
        st.markdown(f'Our analysis says that this text is **{sentiment[0]}**')

        audio_summary = toAudio()
        audio_summary.convert_to_audio(summary)
        audio_file = open("converted.mp3", 'rb')
        audio_bytes = audio_file.read()
        st.subheader("Audio of Summary")
        st.audio(audio_bytes, format = 'audio/ogg', start_time=0)
        st.balloons()
        
    
    # If user inputs an invalid Youtube link
    elif youtube_link!='':
        st.error('Please enter a valid Youtube Link!')

# If user uploads a local video    
elif input_format=='Upload a Video':
    # Browse button for uploading .mp4 files
    file = st.file_uploader('Upload a video',type=['mp4'],accept_multiple_files=False)
    if file is not None:
        # st.video(file)
        # Make a progress bar
        progress_bar = st.progress(0)
        progress_bar.progress(10)
        # Decorative material
        progress_lines = secrets.choice(wittyThings)
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
        # Complete progress bar to 90
        progress_bar.progress(90)
        # Analyze sentiment
        sentiment = analyze(summary)
        # Display Summary
        st.header('Summary')
        st.write(summary)
        progress_bar.progress(100)
        st.markdown(f'Our analysis says that this text is **{sentiment[0]}**')
        audio_summary = toAudio()
        audio_summary.convert_to_audio(summary)
        audio_file = open("converted.mp3", 'rb')
        audio_bytes = audio_file.read()
        st.subheader("Audio of Summary")
        st.balloons()
    else:
        for name in glob('*.mp4'):
            os.remove(name)

# If user uploads a local audio
elif input_format == "Upload an Audio File (.wav)":
    file = st.file_uploader('Upload an Audio File (.wav)',type=['wav'],accept_multiple_files=False)
    if file is not None:
        # Make a progress bar
        progress_bar = st.progress(0)
        progress_bar.progress(10)
        # Decorative material
        progress_lines = secrets.choice(wittyThings)
        # Wait till we run the summarization
        with st.spinner(progress_lines+' . . .'):
            progress_bar.progress(25)
            # Download the uploaded audio file
            save_file(file)
            progress_bar.progress(40)
            # Call TranscribeAudio class 
            transcribe_audio = TranscribeAudio()
            progress_bar.progress(60)
            # Get summary
            summary = transcribe_audio.transcribe_audio(os.path.join(os.getcwd(), file.name))
        # Complete progress bar to 100
        progress_bar.progress(100)
        # Analyze sentiment
        sentiment = analyze(summary)
        # Display Summary
        st.subheader('Summary')
        st.write(summary)
        st.markdown(f'Our analysis says that this text is **{sentiment[0]}**')
        audio_summary = toAudio()
        audio_summary.convert_to_audio(summary)
        audio_file = open("converted.mp3", 'rb')
        audio_bytes = audio_file.read()
        st.subheader("Audio of Summary")
        st.audio(audio_bytes, format = 'audio/ogg', start_time=0)
        st.balloons()
    else:
        for name in glob('*.wav'):
            os.remove(name)
