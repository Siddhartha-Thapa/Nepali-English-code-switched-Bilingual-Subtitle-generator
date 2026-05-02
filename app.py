"""
Streamlit Subtitle System with HTML5 Video Player
Perfect Devanagari support using native HTML5 video with WebVTT
Premium Light Theme Professional UI Design
"""

import streamlit as st
import tempfile
import os
from pathlib import Path
import base64
from typing import List, Dict, Optional
from datetime import timedelta
from utils.bilingual import bilingualize_word


# =====================================================
# CUSTOM CSS STYLING - PREMIUM LIGHT THEME
# =====================================================

def inject_custom_css():
    """Inject premium light theme professional CSS styling"""
    st.markdown("""
    <style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;500;600;700;800;900&family=Montserrat:wght@300;400;500;600;700;800&family=Raleway:wght@300;400;500;600;700;800&display=swap');
    
    /* Root Variables - Premium Light Color Palette */
    :root {
        --primary: #6366F1;
        --primary-light: #818CF8;
        --primary-dark: #4F46E5;
        --secondary: #EC4899;
        --accent: #06B6D4;
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
        
        --bg-primary: #FFFFFF;
        --bg-secondary: #F9FAFB;
        --bg-tertiary: #F3F4F6;
        --bg-elevated: #FFFFFF;
        
        --text-primary: #111827;
        --text-secondary: #6B7280;
        --text-muted: #9CA3AF;
        
        --border-light: #E5E7EB;
        --border-medium: #D1D5DB;
        --border-dark: #9CA3AF;
        
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
        --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
        --shadow-lg: 0 10px 30px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 50px rgba(0, 0, 0, 0.12);
        
        --glow-primary: rgba(99, 102, 241, 0.2);
        --glow-accent: rgba(6, 182, 212, 0.2);
    }
    
    /* Global Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #F9FAFB 0%, #FFFFFF 50%, #F3F4F6 100%);
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Subtle Background Pattern */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 20%, rgba(99, 102, 241, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(6, 182, 212, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(236, 72, 153, 0.02) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Container */
    .main .block-container {
        padding: 3rem 2rem;
        max-width: 1400px;
        position: relative;
        z-index: 1;
    }
    
    /* Hide Sidebar Completely */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Adjust main content to full width */
    .main {
        margin-left: 0 !important;
    }
    
    /* Hero Header */
    h1 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        font-size: 4rem !important;
        background: linear-gradient(135deg, #6366F1 0%, #06B6D4 50%, #EC4899 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center !important;
        letter-spacing: -0.03em;
        margin-bottom: 1rem !important;
        animation: gradientShift 8s ease infinite;
        filter: drop-shadow(0 2px 8px rgba(99, 102, 241, 0.15));
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Subtitle */
    .subtitle {
        font-family: 'Raleway', sans-serif;
        font-size: 1.3rem;
        font-weight: 400;
        color: var(--text-secondary);
        text-align: center;
        margin-bottom: 3rem;
        letter-spacing: 0.02em;
    }
    
    /* Section Headers */
    h2 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        color: var(--text-primary) !important;
        margin-bottom: 1.5rem !important;
        letter-spacing: -0.02em;
        position: relative;
        padding-left: 1.5rem;
    }
    
    h2::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 5px;
        height: 70%;
        background: linear-gradient(180deg, var(--primary) 0%, var(--accent) 100%);
        border-radius: 10px;
        box-shadow: 0 0 12px var(--glow-primary);
    }
    
    h3 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        color: var(--text-primary) !important;
        margin-bottom: 1rem !important;
    }
    
    /* Premium Card */
    .premium-card {
        background: var(--bg-elevated);
        border-radius: 24px;
        padding: 2.5rem;
        border: 1px solid var(--border-light);
        box-shadow: var(--shadow-lg);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .premium-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, 
            transparent, 
            var(--primary) 20%, 
            var(--accent) 50%, 
            var(--primary) 80%, 
            transparent);
        opacity: 0.8;
    }
    
    .premium-card:hover {
        transform: translateY(-4px);
        border-color: var(--border-medium);
        box-shadow: var(--shadow-xl);
    }
    
    /* File Uploader */
    .stFileUploader {
        background: transparent !important;
        border: none !important;
    }
    
    .stFileUploader > div {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.04) 0%, rgba(6, 182, 212, 0.04) 100%) !important;
        border: 2px dashed var(--primary) !important;
        border-radius: 20px !important;
        padding: 4rem 3rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
    }
    
    .stFileUploader > div::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.05) 0%, transparent 70%);
        animation: rotateBg 20s linear infinite;
        pointer-events: none;
    }
    
    @keyframes rotateBg {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .stFileUploader > div:hover {
        border-color: var(--accent) !important;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(6, 182, 212, 0.06) 100%) !important;
        transform: translateY(-2px);
        box-shadow: 
            0 12px 30px rgba(99, 102, 241, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
    }
    
    .stFileUploader label {
        color: var(--text-primary) !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Primary Buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
        color: white !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        padding: 1rem 3rem !important;
        border: none !important;
        border-radius: 16px !important;
        box-shadow: 
            var(--shadow-md),
            0 4px 20px var(--glow-primary) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.02em;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button[kind="primary"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.6s;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 
            var(--shadow-lg),
            0 8px 30px var(--glow-primary) !important;
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%) !important;
    }
    
    .stButton > button[kind="primary"]:hover::before {
        left: 100%;
    }
    
    .stButton > button[kind="primary"]:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    
    /* Download Buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(6, 182, 212, 0.08) 100%) !important;
        border: 2px solid var(--primary) !important;
        color: var(--primary) !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        border-radius: 14px !important;
        padding: 0.9rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }
    
    .stDownloadButton > button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
        border-radius: 50%;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(6, 182, 212, 0.12) 100%) !important;
        border-color: var(--primary-dark) !important;
        color: var(--primary-dark) !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-md), 0 4px 20px var(--glow-primary) !important;
    }
    
    .stDownloadButton > button:hover::after {
        width: 300px;
        height: 300px;
    }
    
    /* Metrics */
    .stMetric {
        background: linear-gradient(135deg, var(--bg-elevated) 0%, var(--bg-secondary) 100%) !important;
        padding: 2rem !important;
        border-radius: 20px !important;
        border: 1px solid var(--border-light) !important;
        box-shadow: var(--shadow-md) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
    }
    
    .stMetric::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.08) 0%, transparent 70%);
        pointer-events: none;
        border-radius: 50%;
    }
    
    .stMetric:hover {
        transform: translateY(-4px);
        border-color: var(--border-medium);
        box-shadow: var(--shadow-lg), 0 4px 20px var(--glow-primary);
    }
    
    .stMetric label {
        color: var(--text-muted) !important;
        font-family: 'Raleway', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Input Fields */
    .stSelectbox, .stSlider, .stTextInput, .stCheckbox {
        margin-bottom: 1.5rem;
    }
    
    .stSelectbox label, .stSlider label, .stTextInput label, .stCheckbox label {
        color: var(--text-primary) !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    input, select, textarea {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-family: 'Poppins', sans-serif !important;
        padding: 0.8rem 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    input:focus, select:focus, textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px var(--glow-primary), var(--shadow-sm) !important;
        outline: none !important;
        background: white !important;
    }
    
    /* Checkbox */
    .stCheckbox {
        background: var(--bg-secondary);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid var(--border-light);
        transition: all 0.3s ease;
    }
    
    .stCheckbox:hover {
        border-color: var(--border-medium);
        background: var(--bg-elevated);
        box-shadow: var(--shadow-sm);
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%) !important;
        height: 4px !important;
        border-radius: 10px !important;
    }
    
    .stSlider > div > div > div > div {
        background: white !important;
        border: 2px solid var(--primary) !important;
        box-shadow: 0 2px 8px var(--glow-primary) !important;
    }
    
    /* Alert Messages */
    .stSuccess, .stInfo, .stWarning, .stError {
        background: var(--bg-elevated) !important;
        border-radius: 16px !important;
        border: 1px solid !important;
        border-left: 4px solid !important;
        padding: 1.2rem 1.5rem !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .stSuccess {
        border-color: rgba(16, 185, 129, 0.3) !important;
        border-left-color: var(--success) !important;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, var(--bg-elevated) 100%) !important;
        color: #065F46 !important;
    }
    
    .stInfo {
        border-color: rgba(6, 182, 212, 0.3) !important;
        border-left-color: var(--accent) !important;
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, var(--bg-elevated) 100%) !important;
        color: #155E75 !important;
    }
    
    .stWarning {
        border-color: rgba(245, 158, 11, 0.3) !important;
        border-left-color: var(--warning) !important;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, var(--bg-elevated) 100%) !important;
        color: #92400E !important;
    }
    
    .stError {
        border-color: rgba(239, 68, 68, 0.3) !important;
        border-left-color: var(--error) !important;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, var(--bg-elevated) 100%) !important;
        color: #991B1B !important;
    }
    
    /* Divider */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, 
            transparent, 
            var(--primary) 20%, 
            var(--accent) 50%, 
            var(--primary) 80%, 
            transparent) !important;
        margin: 3rem 0 !important;
        border-radius: 10px;
        opacity: 0.3;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--bg-secondary) !important;
        border-radius: 14px !important;
        border: 1px solid var(--border-light) !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        padding: 1.2rem 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--bg-elevated) !important;
        border-color: var(--border-medium) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    .streamlit-expanderContent {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 0 0 14px 14px !important;
        padding: 1.5rem !important;
        border-top: none !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: var(--primary) !important;
        border-right-color: var(--accent) !important;
    }
    
    /* Code */
    code {
        background: var(--bg-secondary) !important;
        color: var(--primary-dark) !important;
        font-family: 'Courier New', monospace !important;
        padding: 0.3rem 0.6rem !important;
        border-radius: 6px !important;
        border: 1px solid var(--border-light) !important;
        font-size: 0.9rem !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        border-radius: 10px;
        border: 2px solid var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem 0 2rem 0;
        color: var(--text-muted);
        font-family: 'Raleway', sans-serif;
        font-size: 0.95rem;
        border-top: 1px solid var(--border-light);
        margin-top: 4rem;
    }
    
    .footer-brand {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1.2rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    /* Feature Card */
    .feature-card {
        background: var(--bg-elevated);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid var(--border-light);
        transition: all 0.3s ease;
        height: 100%;
        box-shadow: var(--shadow-sm);
    }
    
    .feature-card:hover {
        border-color: var(--border-medium);
        transform: translateY(-4px);
        box-shadow: var(--shadow-md);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .feature-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1.2rem;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        font-family: 'Poppins', sans-serif;
        font-weight: 400;
        font-size: 0.95rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Responsive */
    @media (max-width: 768px) {
        h1 {
            font-size: 2.5rem !important;
        }
        
        .premium-card {
            padding: 1.5rem;
        }
        
        .stFileUploader > div {
            padding: 2rem 1.5rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# =====================================================
# SUBTITLE SYNCHRONIZER
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
                
                processed_word = bilingualize_word(word)
                current_chunk.append(processed_word)

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
# HTML5 VIDEO PLAYER - PREMIUM LIGHT
# =====================================================

def create_html5_video_player(video_path: str, vtt_path: str, 
                              width: str = "100%", height: str = "auto") -> str:
    """
    Create premium HTML5 video player with embedded VTT subtitles
    Perfect Devanagari support with professional light styling!
    """
    
    # Read video file and encode to base64
    with open(video_path, 'rb') as video_file:
        video_bytes = video_file.read()
        video_base64 = base64.b64encode(video_bytes).decode()
    
    # Read VTT file and encode to base64
    with open(vtt_path, 'r', encoding='utf-8') as vtt_file:
        vtt_content = vtt_file.read()
        vtt_base64 = base64.b64encode(vtt_content.encode('utf-8')).decode()
    
    # Create HTML with embedded video and subtitles - PREMIUM LIGHT STYLING
    html_code = f"""
    <div style="width: {width}; margin: auto; position: relative;">
        <video id="video-player" width="100%" height="{height}" controls crossorigin="anonymous">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            <track label="Nepali" kind="subtitles" srclang="ne" 
                   src="data:text/vtt;base64,{vtt_base64}" default>
            Your browser does not support the video tag.
        </video>
        
        <style>
            /* Premium light subtitle styling */
            video::cue {{
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(249, 250, 251, 0.95) 100%);
                color: #111827;
                font-size: 28px;
                font-family: 'Noto Sans Devanagari', 'Noto Sans', 'Poppins', Arial, sans-serif;
                text-align: center;
                padding: 14px 24px;
                border-radius: 10px;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(99, 102, 241, 0.2);
                box-shadow: 
                    0 8px 32px rgba(0, 0, 0, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 1);
                font-weight: 500;
                letter-spacing: 0.01em;
            }}
            
            /* Premium video player container */
            #video-player {{
                border-radius: 24px;
                box-shadow: 
                    0 20px 60px rgba(0, 0, 0, 0.12),
                    0 0 0 1px rgba(229, 231, 235, 1),
                    0 4px 20px rgba(99, 102, 241, 0.1);
                background: #000;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            
            #video-player:hover {{
                box-shadow: 
                    0 25px 70px rgba(0, 0, 0, 0.15),
                    0 0 0 1px rgba(209, 213, 219, 1),
                    0 8px 30px rgba(99, 102, 241, 0.2);
                transform: translateY(-2px);
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
        page_title="Subtitle Sync Pro",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Inject Custom CSS
    inject_custom_css()
    
    init_session_state()
    
    # Hero Header
    st.markdown("""
    <h1>🎬 वाणी Verse</h1>
    <div class="subtitle">Let your words flow</div>
    """, unsafe_allow_html=True)
    
    # Main Upload Section
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("## 📤 Upload Your Media")
    
    uploaded_file = st.file_uploader(
        "Drag and drop your video or audio file here",
        type=['mp4', 'avi', 'mov', 'mkv', 'wav', 'mp3', 'm4a', 'flac'],
        help="Supported formats: MP4, AVI, MOV, MKV, WAV, MP3, M4A, FLAC"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file:
        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.read())
            input_file_path = tmp_file.name
        
        # Determine file type
        file_ext = Path(uploaded_file.name).suffix.lower()
        is_audio_only = file_ext in ['.wav', '.mp3', '.m4a', '.flac']
        
        st.success(f"✅ Successfully uploaded: **{uploaded_file.name}**")
        
        # File Info Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📦 File Size", f"{uploaded_file.size / 1024 / 1024:.2f} MB")
        
        with col2:
            file_type = "🎵 Audio Only" if is_audio_only else "🎬 Video"
            st.metric("📁 Type", file_type)
        
        with col3:
            st.metric("📝 Format", file_ext.upper().replace('.', ''))
        
        st.divider()
        
        # Settings Section
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("## ⚙️ Configuration Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🤖 Model Settings")
            
            try:
                from models.custom_model import CustomWhisperModel
                CUSTOM_MODEL_AVAILABLE = True
            except ImportError:
                CUSTOM_MODEL_AVAILABLE = False
            
            use_custom_model = st.checkbox(
                "🔧 Use Custom Trained Model",
                value=CUSTOM_MODEL_AVAILABLE,
                disabled=not CUSTOM_MODEL_AVAILABLE,
                help="Enable to use your fine-tuned Whisper model for better accuracy"
            )
            
            if use_custom_model:
                custom_model_path = st.text_input(
                    "📂 Model Path",
                    value="./models/checkpoints/whisper-nepali-final",
                    help="Enter the path to your fine-tuned model directory"
                )
                
                use_gpu = st.checkbox(
                    "⚡ Enable GPU Acceleration",
                    value=False,
                    help="Use GPU for faster inference (requires CUDA)"
                )
                st.session_state.use_gpu = use_gpu
                
                if custom_model_path and not os.path.exists(custom_model_path):
                    st.error("⚠️ Model path does not exist!")
            else:
                model_size = st.selectbox(
                    "🎯 Whisper Model Size",
                    ["tiny", "base", "small", "medium", "large"],
                    index=1,
                    help="Larger models provide better accuracy but are slower"
                )
                custom_model_path = None
        
        with col2:
            st.markdown("### 📝 Subtitle Settings")
            
            max_chars = st.slider(
                "📏 Max Characters Per Line", 
                min_value=20, 
                max_value=80, 
                value=42,
                help="Maximum number of characters allowed per subtitle line"
            )
            
            max_duration = st.slider(
                "⏱️ Max Duration (seconds)", 
                min_value=2.0, 
                max_value=10.0, 
                value=5.0, 
                step=0.5,
                help="Maximum duration for each subtitle segment"
            )
            
            font_size = st.slider(
                "🔤 Subtitle Font Size (px)", 
                min_value=16, 
                max_value=36, 
                value=24,
                help="Font size for subtitle display"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Generate Button
        st.markdown("<br>", unsafe_allow_html=True)
        
        button_label = "🚀 Generate Subtitles" + (" (Audio Mode)" if is_audio_only else " (Video Mode)")
        
        if st.button(button_label, type="primary", use_container_width=True):
            st.session_state.processing_complete = False
            
            try:
                # Step 1: Transcribe
                syncer = SubtitleSynchronizer(
                    max_chars_per_line=max_chars,
                    max_duration=max_duration
                )
                
                with st.spinner("🎤 Transcribing audio... This may take a few moments."):
                    result = syncer.transcribe_audio(
                        input_file_path,
                        use_custom_model=use_custom_model,
                        custom_model_path=custom_model_path if use_custom_model else None,
                        model_size=model_size if not use_custom_model else None,
                        language=None  # Auto-detect
                    )
                
                st.success("✅ Transcription completed successfully!")
                
                # Step 2: Generate subtitles
                with st.spinner("✂️ Generating subtitle segments..."):
                    subtitles = syncer.chunk_words_into_subtitles(result['segments'])
                    st.session_state.subtitles = subtitles
                
                st.success(f"✅ Generated **{len(subtitles)}** subtitle segments!")
                
                # Step 3: Create VTT file
                vtt_content = syncer.generate_vtt(subtitles)
                
                # Save VTT file
                vtt_path = tempfile.NamedTemporaryFile(delete=False, suffix='.vtt', mode='w', encoding='utf-8')
                vtt_path.write(vtt_content)
                vtt_path.close()
                
                st.session_state.vtt_path = vtt_path.name
                st.session_state.video_path = input_file_path if not is_audio_only else None
                st.session_state.processing_complete = True
                
                st.success("✅ Subtitles are ready for download!")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                import traceback
                with st.expander("🔍 View Error Details"):
                    st.code(traceback.format_exc())
                st.session_state.processing_complete = False
        
        # Display results
        if st.session_state.processing_complete:
            st.divider()
            
            # Show video player with subtitles
            if st.session_state.video_path and os.path.exists(st.session_state.video_path):
                st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                st.markdown("## 🎬 Video Preview with Subtitles")
                
                st.info("💡 The video player below features native HTML5 subtitle support with perfect Devanagari rendering. You can toggle subtitles using the player controls.")
                
                # Create HTML5 player
                html_player = create_html5_video_player(
                    st.session_state.video_path,
                    st.session_state.vtt_path,
                    width="100%"
                )
                
                # Display the player
                st.components.v1.html(html_player, height=650, scrolling=False)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.divider()
                
                # Download options
                st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                st.markdown("## ⬇️ Download Your Files")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Original video
                    with open(st.session_state.video_path, 'rb') as f:
                        video_bytes = f.read()
                    st.download_button(
                        "📥 Download Video",
                        video_bytes,
                        file_name="video.mp4",
                        mime="video/mp4",
                        use_container_width=True,
                        help="Download the original video file"
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
                            use_container_width=True,
                            help="Download subtitles in SRT format"
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
                            use_container_width=True,
                            help="Download subtitles in WebVTT format"
                        )
                
                st.info("ℹ️ **Note:** The video file is downloaded without burned-in subtitles. Use the VTT/SRT files with video players that support external subtitles, or use video editing software to permanently burn them into the video.")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Audio only - show subtitle files
            elif st.session_state.subtitles:
                st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                st.markdown("## 📝 Transcription Complete")
                st.success("✅ Audio file has been successfully processed!")
                
                st.divider()
                st.markdown("### ⬇️ Download Your Subtitle Files")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    syncer = SubtitleSynchronizer()
                    srt_content = syncer.generate_srt(st.session_state.subtitles)
                    st.download_button(
                        "📥 Download SRT",
                        srt_content,
                        file_name="subtitles.srt",
                        mime="text/plain",
                        use_container_width=True,
                        help="Download subtitles in SRT format"
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
                            use_container_width=True,
                            help="Download subtitles in WebVTT format"
                        )
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Subtitle preview
            if st.session_state.subtitles:
                st.divider()
                
                st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                st.markdown("## 📝 Subtitle Preview")
                
                with st.expander("👁️ View All Subtitle Segments", expanded=False):
                    for i, sub in enumerate(st.session_state.subtitles, 1):
                        st.markdown(f"""
                        <div style="margin-bottom: 1rem; padding: 1rem; background: var(--bg-secondary); border-radius: 12px; border-left: 3px solid var(--primary); box-shadow: var(--shadow-sm);">
                            <div style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.3rem;">
                                <strong>#{i}</strong> • {sub['start']:.2f}s - {sub['end']:.2f}s
                            </div>
                            <div style="color: var(--text-primary); font-size: 1.05rem;">
                                {sub['text']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Welcome Section with Features
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("## 👋 Welcome to वाणी Verse")
        st.markdown("""
        <p style="color: var(--text-secondary); font-size: 1.1rem; line-height: 1.8; margin-bottom: 2rem;">
        Transform your videos and audio files with AI-powered subtitle generation. 
        Our system provides perfect Devanagari support with decent accuracy.
        </p>
        """, unsafe_allow_html=True)
        
        # Features Grid
        st.markdown("### ✨ Key Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Decent Accuracy</div>
                <div class="feature-description">
                    AI-powered transcription with word-level timestamps for precise subtitle synchronization
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🌐</div>
                <div class="feature-title">Devanagari Support</div>
                <div class="feature-description">
                    Native HTML5 rendering with perfect Unicode support for Nepali and Hindi scripts
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Fast Processing</div>
                <div class="feature-description">
                    Optimized Whisper models with optional GPU acceleration for quick results
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🎬</div>
                <div class="feature-title">Multi-Format</div>
                <div class="feature-description">
                    Support for MP4, AVI, MOV, MKV videos and WAV, MP3, M4A, FLAC audio files
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📥</div>
                <div class="feature-title">Export Options</div>
                <div class="feature-description">
                    Download subtitles in both SRT and VTT formats for maximum compatibility
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🔧</div>
                <div class="feature-title">Customizable</div>
                <div class="feature-description">
                    Fine-tune subtitle duration, character limits, and use custom-trained models
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Quick Start Guide
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("## 🚀 Quick Start Guide")
        
        st.markdown("""
        <div style="color: var(--text-secondary); font-size: 1rem; line-height: 1.8;">
        
        **Step 1:** Upload your video or audio file using the file uploader above
        
        **Step 2:** Configure your preferred settings (model type, subtitle parameters)
        
        **Step 3:** Click the "Generate Subtitles" button and wait for processing
        
        **Step 4:** Preview your video with subtitles in the HTML5 player
        
        **Step 5:** Download the subtitle files (SRT/VTT) and original video
        
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.divider()
    st.markdown("""
    <div class="footer">
        <div class="footer-brand">वाणी Verse</div>
        <div style="margin-bottom: 0.5rem;">
            "Let Your Words Flow" 
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()