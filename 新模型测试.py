import os

from transformers import pipeline

缓存目录 = os.path.dirname(os.path.abspath(__file__))

transcriber = pipeline(
    "automatic-speech-recognition",
    model="BELLE-2/Belle-whisper-large-v3-turbo-zh",
    cache_dir=缓存目录
)

transcriber.model.config.forced_decoder_ids = (
    transcriber.tokenizer.get_decoder_prompt_ids(
        language="zh",
        task="transcribe"
    )
)

transcription = transcriber("my_audio.wav")
