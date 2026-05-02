"""
models/custom_model.py
Wrapper for your trained Whisper model
"""

import torch
import numpy as np
from typing import Dict, List, Optional
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CustomWhisperModel:
    """Wrapper for fine-tuned Whisper model"""
    
    def __init__(self, model_path: str, device: str = "cpu"):
        """
        Initialize the custom Whisper model
        
        Args:
            model_path: Path to the fine-tuned model directory
            device: Device to run the model on ('cpu' or 'cuda')
        """
        self.device = device
        self.model_path = model_path
        
        logger.info(f"Loading model from {model_path}")
        
        # Load processor and model
        self.processor = WhisperProcessor.from_pretrained(
            model_path,
            language="ne",
            task="transcribe"
        )
        
        self.model = WhisperForConditionalGeneration.from_pretrained(
            model_path
        ).to(device)
        
        self.model.eval()
        
        # Configure model
        self.model.config.forced_decoder_ids = None
        self.model.config.suppress_tokens = []
        
        logger.info("Model loaded successfully")
    
    def transcribe(self, audio_path: str, **kwargs) -> Dict:
        """
        Transcribe audio file - Whisper-compatible interface
        
        Args:
            audio_path: Path to audio file
            **kwargs: Additional arguments (compatibility)
            
        Returns:
            Dictionary with transcription results in Whisper format
        """
        import librosa
        
        # Load audio at 16kHz
        audio, sr = librosa.load(audio_path, sr=16000, mono=True)
        
        logger.info(f"Transcribing audio of length {len(audio)/sr:.2f}s")
        
        # Process audio
        input_features = self.processor(
            audio,
            sampling_rate=16000,
            return_tensors="pt"
        ).input_features.to(self.device)
        
        # Generate transcription
        with torch.no_grad():
            predicted_ids = self.model.generate(
                input_features,
                return_timestamps=True,  # Get word-level timestamps
                language="ne",
                task="transcribe"
            )
        
        # Decode to text
        transcription = self.processor.batch_decode(
            predicted_ids,
            skip_special_tokens=True
        )[0]
        
        # Convert to Whisper-compatible format
        result = self._format_output(transcription, audio, sr, predicted_ids)
        
        logger.info(f"Transcription complete: {len(result['segments'])} segments")
        
        return result
    
    def _format_output(self, transcription: str, audio: np.ndarray, 
                      sr: int, predicted_ids: torch.Tensor) -> Dict:
        """
        Format output to match Whisper's output structure
        
        Args:
            transcription: Full transcription text
            audio: Audio array
            sr: Sample rate
            predicted_ids: Generated token IDs
            
        Returns:
            Dictionary matching Whisper output format
        """
        # Calculate audio duration
        duration = len(audio) / sr
        
        # Split transcription into segments (simple split by sentences)
        segments = self._create_segments(transcription, duration)
        
        return {
            'text': transcription,
            'segments': segments,
            'language': 'ne'
        }
    
    def _create_segments(self, text: str, duration: float) -> List[Dict]:
        """
        Create segments with word-level timestamps
        
        Args:
            text: Full transcription text
            duration: Total audio duration
            
        Returns:
            List of segments with word timestamps
        """
        import re
        
        # Split by Devanagari sentence endings
        sentence_endings = r'[।॥?!]'
        sentences = re.split(sentence_endings, text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            sentences = [text]
        
        segments = []
        time_per_segment = duration / len(sentences)
        
        for i, sentence in enumerate(sentences):
            start_time = i * time_per_segment
            end_time = (i + 1) * time_per_segment
            
            # Split into words
            words = sentence.split()
            word_duration = time_per_segment / len(words) if words else 0
            
            word_list = []
            for j, word in enumerate(words):
                word_start = start_time + (j * word_duration)
                word_end = word_start + word_duration
                
                word_list.append({
                    'word': word,
                    'start': word_start,
                    'end': word_end,
                    'probability': 0.95  # Placeholder confidence
                })
            
            segments.append({
                'start': start_time,
                'end': end_time,
                'text': sentence,
                'words': word_list
            })
        
        return segments


class ModelLoader:
    """Factory class for loading models"""
    
    @staticmethod
    def load_model(model_type: str = "whisper", model_path: str = None, 
                   device: str = "cpu"):
        """
        Load model based on type
        
        Args:
            model_type: Type of model ('whisper' or 'custom')
            model_path: Path to model (required for custom)
            device: Device to run on
            
        Returns:
            Model instance
        """
        if model_type == "custom":
            if not model_path:
                raise ValueError("model_path required for custom model")
            return CustomWhisperModel(model_path, device)
        else:
            # Load standard Whisper
            import whisper
            return whisper.load_model("base")