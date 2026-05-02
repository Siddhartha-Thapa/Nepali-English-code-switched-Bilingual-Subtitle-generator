# test_model.py
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from peft import PeftModel
import torch
import librosa

def test_model(model_path, audio_path):
    # Load model
    processor = WhisperProcessor.from_pretrained("openai/whisper-small")
    base_model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
    model = PeftModel.from_pretrained(base_model, model_path)
    model = model.merge_and_unload()
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    
    # Load audio
    audio, sr = librosa.load(audio_path, sr=16000)
    
    # Process
    input_features = processor(audio, sampling_rate=16000, return_tensors="pt").input_features.to(device)
    
    # Generate
    with torch.no_grad():
        predicted_ids = model.generate(input_features)
    
    # Decode
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    
    print(f"✓ Model loaded successfully!")
    print(f"✓ Transcription: {transcription}")
    return transcription

if __name__ == "__main__":
    test_model("../models/checkpoints/whisper-nepali-final", "sample.wav")