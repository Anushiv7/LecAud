import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports
imports = '''import streamlit as st
import os
import json
import time
from audio_recorder_streamlit import audio_recorder
'''

content = content.replace('import streamlit as st\nimport os\nimport json\nimport time\n', imports)

tab1_replacement = '''with tab1:
    st.header("Upload or Record Lecture Audio")
    st.info("Upload a lecture recording or use your microphone to begin the process.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("??? Record Audio")
        audio_bytes = audio_recorder(text="Click to record", recording_color="#e8b62c", neutral_color="#6aa36f", icon_name="microphone", icon_size="2x")
        
    with col2:
        st.subheader("?? Upload Audio")
        uploaded_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3', 'm4a', 'ogg'])
        
    audio_source = None
    
    class RecordedAudio:
        def __init__(self, data: bytes):
            self.data = data
            self.name = "recorded_audio.wav"
        def getvalue(self):
            return self.data
            
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        audio_source = RecordedAudio(audio_bytes)
        st.success("Audio recorded successfully!")
    elif uploaded_file is not None:
        st.audio(uploaded_file, format='audio/wav')
        audio_source = uploaded_file
        
    if audio_source is not None:
        if st.button("Process Audio", type="primary"):
            if not api_key:
                st.error("Please configure your Gemini API Key first.")
            else:
                try:
                    st.session_state.audio_file = audio_source.name
                    
                    with st.spinner("Validating audio..."):
                        audio_processor = AudioProcessor()
                        try:
                            is_valid = audio_processor.validate_audio_file(audio_source)
                        except ValueError as ve:
                            st.error(str(ve))
                            is_valid = False
                            
                        if is_valid:
                            with st.spinner("Transcribing audio (this may take a minute)..."):
                                transcriber = Transcriber(api_key=api_key)
                                try:
                                    transcript = transcriber.transcribe_audio(audio_source)
                                    st.session_state.transcript = transcript
                                    st.success("Transcription complete! Move to the next tab.")
                                except ValueError as ve:
                                    st.error(f"Transcription failed: {str(ve)}")
                except Exception as e:
                    st.error(f"An error occurred during audio processing: {str(e)}")
'''

content = re.sub(r'with tab1:.*?# ==========================================\n# TAB 2:', tab1_replacement + '\n# ==========================================\n# TAB 2:', content, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
