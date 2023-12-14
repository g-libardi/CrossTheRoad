import wave
import pyaudio
import threading
import numpy as np

def _play_sound(filename, volume=1.0):
    # Open the file in read mode
    wf = wave.open(filename, 'rb')

    # Create an audio object
    p = pyaudio.PyAudio()

    # Open a stream on the audio object
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read data from the file
    data = wf.readframes(1024)

    # Play the sound by writing the data to the stream
    while data != b'':
        # Convert data to numpy array
        np_data = np.frombuffer(data, dtype=np.int16)

        # Adjust volume
        np_data = (np_data * volume).astype(np.int16)

        # Convert numpy array back to bytes
        data = np_data.tobytes()

        stream.write(data)
        data = wf.readframes(1024)

    # Close the stream
    stream.stop_stream()
    stream.close()

    # Terminate the audio object
    p.terminate()

# Call the function with the path to your .wav file
def play_sound(filename, volume=1.0):
    # Create a thread
    thread = threading.Thread(target=_play_sound, args=(filename, volume), daemon=True)
    # Start the thread
    thread.start()
    
def _play_sound_loop(filename, volume=1.0):
    # Open the file in read mode
    wf = wave.open(filename, 'rb')

    # Create an audio object
    p = pyaudio.PyAudio()

    # Open a stream on the audio object
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Loop indefinitely
    while True:
        # Read data from the file
        data = wf.readframes(1024)

        # Play the sound by writing the data to the stream
        while data != b'':
            # Convert data to numpy array
            np_data = np.frombuffer(data, dtype=np.int16)

            # Adjust volume
            np_data = (np_data * volume).astype(np.int16)

            # Convert numpy array back to bytes
            data = np_data.tobytes()

            stream.write(data)
            data = wf.readframes(1024)

        # Rewind the file to the beginning
        wf.rewind()

def play_sound_loop(filename, volume=1.0):
    # Create a thread
    loop_thread = threading.Thread(target=_play_sound_loop, args=(filename, volume), daemon=True)
    # Start the thread
    loop_thread.start()
