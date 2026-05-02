"""
Streamlit Subtitle System with HTML5 Video Player
Perfect Devanagari support using native HTML5 video with WebVTT
"""

import streamlit as st
import tempfile
import os
from pathlib import Path
import base64
from typing import List, Dict, Optional
from datetime import timedelta


# =====================================================
# SUBTITLE SYNCHRONIZER (Updated)
# =====================================================

class SubtitleSynchronizer:
    """Handles transcription and subtitle generation"""
    
    def __init__(self, max_chars_per_line: int = 42, max_duration: float = 5.0):
        self.max_chars_per_line = max_chars_per_line
        self.max_duration = max_duration
        self.model = None
        self.model_type = None
    
    def load_whisper_model(self, model_size: str = "base"):
        """Load standard Whisper model"""
        import whisper
        return whisper.load_model(model_size)
    
    def load_custom_model(self, model_path: str, device: str = "cpu"):
        """Load custom trained model"""
        try:
            from models.custom_model import CustomWhisperModel
            return CustomWhisperModel(model_path, device)
        except ImportError:
            st.error("Custom model module not found. Please ensure custom_model.py is in models/ directory")
            raise
    
    def transcribe_audio(self, audio_path: str, 
                        use_custom_model: bool = False,
                        custom_model_path: str = None,
                        model_size: str = "base",
                        language: Optional[str] = None) -> Dict:
        """Transcribe audio with progress tracking"""
        
        # Load appropriate model
        if use_custom_model:
            if not custom_model_path or not os.path.exists(custom_model_path):
                raise ValueError("Custom model path is invalid")
            
            if self.model is None or self.model_type != "custom":
                with st.spinner('Loading custom model...'):
                    device = "cuda" if st.session_state.get('use_gpu', False) else "cpu"
                    self.model = self.load_custom_model(custom_model_path, device)
                    self.model_type = "custom"
                    st.session_state.current_model = "custom"
        else:
            if self.model is None or st.session_state.get('current_model') != model_size:
                with st.spinner(f'Loading {model_size} model...'):
                    self.model = self.load_whisper_model(model_size)
                    self.model_type = "whisper"
                    st.session_state.current_model = model_size
        
        # Transcribe
        with st.spinner('Transcribing audio...'):
            if self.model_type == "custom":
                result = self.model.transcribe(audio_path)
            else:
                result = self.model.transcribe(
                    audio_path,
                    word_timestamps=True,
                    language=language,
                    verbose=False
                )
        
        return result
    
    def chunk_words_into_subtitles(self, segments: List[Dict]) -> List[Dict]:
        """Convert word timestamps into subtitle chunks"""
        subtitles = []
        
        for segment in segments:
            if 'words' not in segment or not segment['words']:
                subtitles.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'].strip()
                })
                continue
            
            words = segment['words']
            current_chunk = []
            chunk_start = None
            
            for i, word_info in enumerate(words):
                word = word_info.get('word', '').strip()
                if not word:
                    continue
                
                if chunk_start is None:
                    chunk_start = word_info['start']
                
                current_chunk.append(word)
                current_text = ' '.join(current_chunk).strip()
                current_duration = word_info['end'] - chunk_start
                
                # Break conditions
                is_punctuation = word[-1] in '.!?,;:।॥'
                exceeds_duration = current_duration >= self.max_duration
                exceeds_chars = len(current_text) >= self.max_chars_per_line
                is_last_word = i == len(words) - 1
                
                should_break = (is_last_word or 
                              (is_punctuation and current_duration >= 1.0) or
                              exceeds_duration or exceeds_chars)
                
                if should_break and current_chunk:
                    subtitles.append({
                        'start': chunk_start,
                        'end': word_info['end'],
                        'text': current_text
                    })
                    current_chunk = []
                    chunk_start = None
        
        return subtitles
    
    def format_timestamp(self, seconds: float, format_type: str = 'srt') -> str:
        """Format timestamp for subtitle files"""
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = int(td.total_seconds() % 60)
        millis = int((td.total_seconds() % 1) * 1000)
        
        if format_type == 'srt':
            return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
        else:  # vtt
            return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
    
    def generate_srt(self, subtitles: List[Dict]) -> str:
        """Generate SRT content"""
        content = []
        for i, sub in enumerate(subtitles, 1):
            content.append(f"{i}")
            content.append(f"{self.format_timestamp(sub['start'], 'srt')} --> "
                         f"{self.format_timestamp(sub['end'], 'srt')}")
            content.append(sub['text'])
            content.append("")
        return '\n'.join(content)
    
    def generate_vtt(self, subtitles: List[Dict]) -> str:
        """Generate VTT content with UTF-8 support"""
        content = ["WEBVTT", ""]
        for sub in subtitles:
            content.append(f"{self.format_timestamp(sub['start'], 'vtt')} --> "
                         f"{self.format_timestamp(sub['end'], 'vtt')}")
            content.append(sub['text'])
            content.append("")
        return '\n'.join(content)


# =====================================================
# HTML5 VIDEO PLAYER
# =====================================================

def create_html5_video_player(video_path: str, vtt_path: str, 
                              width: str = "100%", height: str = "auto") -> str:
    """
    Create HTML5 video player with embedded VTT subtitles
    Perfect Devanagari support!
    """
    
    # Read video file and encode to base64
    with open(video_path, 'rb') as video_file:
        video_bytes = video_file.read()
        video_base64 = base64.b64encode(video_bytes).decode()
    
    # Read VTT file and encode to base64
    with open(vtt_path, 'r', encoding='utf-8') as vtt_file:
        vtt_content = vtt_file.read()
        vtt_base64 = base64.b64encode(vtt_content.encode('utf-8')).decode()
    
    # Create HTML with embedded video and subtitles
    html_code = f"""
    <div style="width: {width}; margin: auto;">
        <video id="video-player" width="100%" height="{height}" controls crossorigin="anonymous">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            <track label="Nepali" kind="subtitles" srclang="ne" 
                   src="data:text/vtt;base64,{vtt_base64}" default>
            Your browser does not support the video tag.
        </video>
        
        <style>
            video::cue {{
                background-color: rgba(0, 0, 0, 0.8);
                color: white;
                font-size: 24px;
                font-family: 'Noto Sans Devanagari', 'Noto Sans', Arial, sans-serif;
                text-align: center;
                padding: 8px;
            }}
            
            #video-player {{
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
        </style>
        
        <script>
            // Ensure subtitles are shown by default
            const video = document.getElementById('video-player');
            const tracks = video.textTracks;
            
            if (tracks.length > 0) {{
                tracks[0].mode = 'showing';
            }}
        </script>
    </div>
    """
    
    return html_code


def create_video_player_with_external_vtt(video_filename: str, vtt_filename: str) -> str:
    """
    Alternative: Create player with external VTT file references
    Use this if base64 encoding causes issues with large files
    """
    
    html_code = f"""
    <div style="width: 100%; margin: auto;">
        <video id="video-player" width="100%" controls crossorigin="anonymous">
            <source src="{video_filename}" type="video/mp4">
            <track label="Nepali" kind="subtitles" srclang="ne" 
                   src="{vtt_filename}" default>
            Your browser does not support the video tag.
        </video>
        
        <style>
            video::cue {{
                background-color: rgba(0, 0, 0, 0.85);
                color: #ffffff;
                font-size: 22px;
                font-family: 'Noto Sans Devanagari', 'Noto Sans', Arial, sans-serif;
                text-align: center;
                padding: 10px 20px;
                line-height: 1.4;
            }}
            
            video::cue(.large) {{
                font-size: 28px;
            }}
            
            #video-player {{
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                background: #000;
            }}
        </style>
        
        <script>
            const video = document.getElementById('video-player');
            
            // Enable subtitles by default
            video.addEventListener('loadedmetadata', function() {{
                const tracks = video.textTracks;
                if (tracks.length > 0) {{
                    tracks[0].mode = 'showing';
                }}
            }});
        </script>
    </div>
    """
    
    return html_code


# =====================================================
# STREAMLIT APP
# =====================================================

def init_session_state():
    """Initialize session state variables"""
    if 'subtitles' not in st.session_state:
        st.session_state.subtitles = None
    if 'vtt_path' not in st.session_state:
        st.session_state.vtt_path = None
    if 'video_path' not in st.session_state:
        st.session_state.video_path = None
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False


def main():
    st.set_page_config(
        page_title="Subtitle Sync System",
        page_icon="🎬",
        layout="wide"
    )
    
    init_session_state()
    
    # Header
    st.title("🎬 Subtitle Synchronization System")
    st.markdown("*HTML5 Video Player with Native Devanagari Support*")
    st.divider()
    
    # Sidebar - Settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Model Selection
        st.subheader("🤖 Model Selection")
        
        try:
            from models.custom_model import CustomWhisperModel
            CUSTOM_MODEL_AVAILABLE = True
        except ImportError:
            CUSTOM_MODEL_AVAILABLE = False
        
        use_custom_model = st.checkbox(
            "Use Custom Trained Model",
            value=CUSTOM_MODEL_AVAILABLE,
            disabled=not CUSTOM_MODEL_AVAILABLE,
            help="Use your fine-tuned Whisper model"
        )
        
        if use_custom_model:
            custom_model_path = st.text_input(
                "Model Path",
                value="./models/checkpoints/whisper-nepali-final",
                help="Path to your fine-tuned model directory"
            )
            
            use_gpu = st.checkbox(
                "Use GPU",
                value=False,
                help="Use GPU for faster inference"
            )
            st.session_state.use_gpu = use_gpu
            
            if custom_model_path and not os.path.exists(custom_model_path):
                st.error("⚠️ Model path does not exist!")
        else:
            model_size = st.selectbox(
                "Whisper Model",
                ["tiny", "base", "small", "medium", "large"],
                index=1,
                help="Larger models are more accurate but slower"
            )
            custom_model_path = None
        
        st.divider()
        
        language = st.selectbox(
            "Language",
            ["Auto-detect", "Nepali", "English", "Hindi"],
            index=1 if use_custom_model else 0
        )
        
        language_code = {
            "Auto-detect": None,
            "Nepali": "ne",
            "English": "en",
            "Hindi": "hi"
        }.get(language, None)
        
        st.divider()
        
        st.subheader("📝 Subtitle Settings")
        max_chars = st.slider("Max chars per line", 20, 80, 42)
        max_duration = st.slider("Max duration (sec)", 2.0, 10.0, 5.0, 0.5)
        
        st.divider()
        
        st.subheader("🎨 Subtitle Style")
        font_size = st.slider("Font size (px)", 16, 36, 24)
        
        st.info("💡 Subtitles use native HTML5 rendering with perfect Devanagari support!")
    
    # Main content
    st.header("📤 Upload Media File")
    
    uploaded_file = st.file_uploader(
        "Choose a video or audio file",
        type=['mp4', 'avi', 'mov', 'mkv', 'wav', 'mp3', 'm4a', 'flac'],
        help="Video: MP4, AVI, MOV, MKV | Audio: WAV, MP3, M4A, FLAC"
    )
    
    if uploaded_file:
        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.read())
            input_file_path = tmp_file.name
        
        # Determine file type
        file_ext = Path(uploaded_file.name).suffix.lower()
        is_audio_only = file_ext in ['.wav', '.mp3', '.m4a', '.flac']
        
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("File Size", f"{uploaded_file.size / 1024 / 1024:.2f} MB")
        
        with col2:
            model_name = "Custom Model" if use_custom_model else f"Whisper {model_size}"
            st.metric("Model", model_name)
        
        with col3:
            file_type = "Audio Only" if is_audio_only else "Video"
            st.metric("Type", file_type)
        
        # Processing button
        if st.button("🚀 Generate Subtitles" + (" (Audio Only)" if is_audio_only else ""), 
                     type="primary", use_container_width=True):
            st.session_state.processing_complete = False
            
            try:
                # Step 1: Transcribe
                syncer = SubtitleSynchronizer(
                    max_chars_per_line=max_chars,
                    max_duration=max_duration
                )
                
                with st.spinner("🎤 Transcribing audio..."):
                    result = syncer.transcribe_audio(
                        input_file_path,
                        use_custom_model=use_custom_model,
                        custom_model_path=custom_model_path if use_custom_model else None,
                        model_size=model_size if not use_custom_model else None,
                        language=language_code
                    )
                
                st.success("✅ Transcription complete!")
                
                # Step 2: Generate subtitles
                with st.spinner("✂️ Generating subtitles..."):
                    subtitles = syncer.chunk_words_into_subtitles(result['segments'])
                    st.session_state.subtitles = subtitles
                
                st.success(f"✅ Generated {len(subtitles)} subtitle segments!")
                
                # Step 3: Create VTT file
                vtt_content = syncer.generate_vtt(subtitles)
                
                # Save VTT file
                vtt_path = tempfile.NamedTemporaryFile(delete=False, suffix='.vtt', mode='w', encoding='utf-8')
                vtt_path.write(vtt_content)
                vtt_path.close()
                
                st.session_state.vtt_path = vtt_path.name
                st.session_state.video_path = input_file_path if not is_audio_only else None
                st.session_state.processing_complete = True
                
                st.success("✅ Subtitles ready!")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
                st.session_state.processing_complete = False
        
        # Display results
        if st.session_state.processing_complete:
            st.divider()
            
            # Show video player with subtitles
            if st.session_state.video_path and os.path.exists(st.session_state.video_path):
                st.header("🎬 Video with Devanagari Subtitles")
                
                st.info("💡 The video player below has native HTML5 subtitle support. "
                       "Devanagari text will display perfectly!")
                
                # Create HTML5 player
                html_player = create_html5_video_player(
                    st.session_state.video_path,
                    st.session_state.vtt_path,
                    width="100%"
                )
                
                # Display the player
                st.components.v1.html(html_player, height=600, scrolling=False)
                
                st.divider()
                
                # Download options
                st.subheader("⬇️ Download Options")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Original video
                    with open(st.session_state.video_path, 'rb') as f:
                        video_bytes = f.read()
                    st.download_button(
                        "📥 Download Video (Original)",
                        video_bytes,
                        file_name="video.mp4",
                        mime="video/mp4",
                        use_container_width=True,
                        help="Download original video (no burned subtitles)"
                    )
                
                with col2:
                    if st.session_state.subtitles:
                        syncer = SubtitleSynchronizer()
                        srt_content = syncer.generate_srt(st.session_state.subtitles)
                        st.download_button(
                            "📥 Download SRT",
                            srt_content,
                            file_name="subtitles.srt",
                            mime="text/plain",
                            use_container_width=True
                        )
                
                with col3:
                    if st.session_state.vtt_path:
                        with open(st.session_state.vtt_path, 'r', encoding='utf-8') as f:
                            vtt_content = f.read()
                        st.download_button(
                            "📥 Download VTT",
                            vtt_content,
                            file_name="subtitles.vtt",
                            mime="text/vtt",
                            use_container_width=True
                        )
                
                st.info("ℹ️ **Note**: The video downloads without burned-in subtitles. "
                       "Use the VTT/SRT files with video players that support external subtitles, "
                       "or use video editing software to burn them permanently.")
            
            # Audio only - show subtitle files
            elif st.session_state.subtitles:
                st.header("📝 Transcription Complete")
                st.info("Audio file processed. Download subtitle files below.")
                
                st.divider()
                st.subheader("⬇️ Download Subtitle Files")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    syncer = SubtitleSynchronizer()
                    srt_content = syncer.generate_srt(st.session_state.subtitles)
                    st.download_button(
                        "📥 Download SRT",
                        srt_content,
                        file_name="subtitles.srt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    if st.session_state.vtt_path:
                        with open(st.session_state.vtt_path, 'r', encoding='utf-8') as f:
                            vtt_content = f.read()
                        st.download_button(
                            "📥 Download VTT",
                            vtt_content,
                            file_name="subtitles.vtt",
                            mime="text/vtt",
                            use_container_width=True
                        )
            
            # Subtitle preview
            if st.session_state.subtitles:
                st.divider()
                st.subheader("📝 Subtitle Preview")
                
                with st.expander("View all subtitles", expanded=False):
                    for i, sub in enumerate(st.session_state.subtitles, 1):
                        st.markdown(f"""
                        **{i}.** `{sub['start']:.2f}s - {sub['end']:.2f}s`  
                        {sub['text']}
                        """)
    
    else:
        # Show instructions
        st.info("""
        ### 📋 How to use:
        
        1. **Configure** model settings in the sidebar
        2. **Upload** your video or audio file
        3. **Click** "Generate Subtitles" button
        4. **Watch** video with perfect Devanagari subtitle display!
        5. **Download** subtitle files for use in other players
        
        ### ✨ Features:
        
        - **Perfect Devanagari Display**: Native HTML5 video player with UTF-8 support
        - **No Font Installation Required**: Works out of the box!
        - **Audio + Video Support**: Process both file types
        - **Custom Model Support**: Use your fine-tuned Nepali Whisper model
        - **Multiple Formats**: SRT and VTT subtitle files
        - **Professional Player**: Built-in video controls
        
        ### 🎯 Advantages of HTML5 Player:
        
        ✅ Perfect Unicode/Devanagari rendering  
        ✅ No font installation needed  
        ✅ Works in any modern browser  
        ✅ Native subtitle controls  
        ✅ Responsive and mobile-friendly  
        ✅ Can toggle subtitles on/off  
        """)
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            Made with ❤️ using Streamlit | HTML5 Video Player with Devanagari Support
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()