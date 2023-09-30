import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import base64

# Streamlit app title
st.title("Video to GIF Converter")

# User input for uploading a video file
uploaded_video = st.file_uploader("Upload a video file:", type=["mp4", "avi", "mov"])

# Start and end time inputs for GIF creation
st.subheader("GIF Configuration")
start_time = st.number_input("Start Time (seconds):", value=0.0, step=1.0)
end_time = st.number_input("End Time (seconds):", value=10.0, step=1.0)

# Function to convert video to GIF
def convert_to_gif(video_file, start_time, end_time):
    # Create a temporary file to save the uploaded video
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
        temp_video_path = temp_video_file.name
        temp_video_file.write(video_file.read())

    # Create the video clip from the temporary file
    video_clip = VideoFileClip(temp_video_path)
    
    # Define the start and end times
    gif_clip = video_clip.subclip(start_time, end_time)
    
    # Generate the GIF and save it as a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".gif") as temp_gif_file:
        temp_gif_path = temp_gif_file.name
        gif_clip.write_gif(temp_gif_path, fps=10)

    # Return the temporary GIF file path
    return temp_gif_path

# Function to create a download link for the GIF
def get_binary_file_downloader_html(file_path, file_label):
    with open(file_path, 'rb') as f:
        bin_data = f.read()
    b64 = base64.b64encode(bin_data).decode()
    href = f'<a href="data:image/gif;base64,{b64}" download="{file_label}.gif">Download {file_label}</a>'
    return href

# Display the generated GIF and allow download
if uploaded_video:
    st.subheader("Uploaded Video:")
    st.video(uploaded_video)

    if st.button("Convert to GIF"):
        gif_path = convert_to_gif(uploaded_video, start_time, end_time)
        st.subheader("Generated GIF:")
        
        # Display the GIF using HTML <img> tag
        with open(gif_path, "rb") as f:
            st.markdown(f'<img src="data:image/gif;base64,{base64.b64encode(f.read()).decode()}" alt="generated gif">', unsafe_allow_html=True)
        
        # Allow the user to download the GIF
        st.markdown(get_binary_file_downloader_html(gif_path, "generated"), unsafe_allow_html=True)
