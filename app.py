import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Voice Summarizer", page_icon="🎙️")

st.title("🎙️ AI Voice Note & Meeting Summarizer")
st.write("Upload your audio file (MP3, WAV, M4A) to get instant transcription and AI key points.")

# User apni OpenAI API key yahan enter karega
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a", "ogg"])

if uploaded_file is not None and api_key:
    client = OpenAI(api_key=api_key)
    
    # Save temporary audio file
    with open("temp_audio.file", "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    if st.button("🚀 Process & Summarize Audio"):
        with st.spinner("Transcribing audio with Whisper AI..."):
            try:
                with open("temp_audio.file", "rb") as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                text = transcript.text
                
                st.success("Transcription Completed!")
                st.subheader("📝 Full Transcript")
                st.write(text)
                
                with st.spinner("Generating AI Summary..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a professional assistant. Summarize the text into 3 clear, actionable bullet points."},
                            {"role": "user", "content": text}
                        ]
                    )
                    summary = response.choices[0].message.content
                    
                    st.subheader("📌 Key Summary & Action Items")
                    st.write(summary)
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
elif uploaded_file and not api_key:
    st.warning("⚠️ Please enter your OpenAI API Key above to process the audio.")
