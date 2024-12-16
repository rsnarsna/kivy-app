import pyaudio
import wave
import threading

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10
MIC_OUTPUT_FILENAME = "mic_output.wav"
SPEAKER_OUTPUT_FILENAME = "speaker_output.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Function to record from microphone
def record_mic():
    mic_stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
    print("Recording from microphone...")
    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = mic_stream.read(CHUNK)
        frames.append(data)

    print("Finished recording from microphone.")
    mic_stream.stop_stream()
    mic_stream.close()

    # Save the recorded data as a WAV file
    wf = wave.open(MIC_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to record from speaker
def record_speaker():
    speaker_stream = audio.open(format=FORMAT, channels=CHANNELS,
                                rate=RATE, input=True,
                                frames_per_buffer=CHUNK)
    print("Recording from speaker...")
    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = speaker_stream.read(CHUNK)
        frames.append(data)

    print("Finished recording from speaker.")
    speaker_stream.stop_stream()
    speaker_stream.close()

    # Save the recorded data as a WAV file
    wf = wave.open(SPEAKER_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Create threads for recording
mic_thread = threading.Thread(target=record_mic)
speaker_thread = threading.Thread(target=record_speaker)

# Start recording
mic_thread.start()
speaker_thread.start()

# Wait for threads to finish
mic_thread.join()
speaker_thread.join()

# Terminate PyAudio
audio.terminate()