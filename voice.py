import openai
import pyaudio
import lameenc
import time
import os

def gen_rand_filename() -> str:
    return "/tmp/audio_{}.mp3".format(int(time.time()))

def record_audio() -> str:
    # Set up mp3 encoder
    encoder = lameenc.Encoder()
    encoder.set_bit_rate(128)
    encoder.set_in_sample_rate(44100)
    encoder.set_channels(2)

    # Initialize pyaudio and open audio stream
    p = pyaudio.PyAudio()
    print("Recording")
    stream = p.open(
        format=pyaudio.paInt16,
        channels=2,
        rate=44100,
        frames_per_buffer=1024,
        input=True
    )

    # Record audio
    frames = []
    try:
        while True:
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt:
        pass

    audio_data = b''.join(frames)

    # Encode audio to mp3
    mp3_data = encoder.encode(audio_data)
    mp3_data += encoder.flush()

    # Save the mp3 file
    filename = gen_rand_filename()
    with open(filename, 'wb') as f:
        f.write(mp3_data)

    # Clean up
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Recorded!")

    return filename


def get_voice_command(language:str = 'en') -> str:
    filename = record_audio()

    try:
        with open(filename, 'rb') as f:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=f
            )
            return transcript["text"]
    finally:
        os.remove(filename)
