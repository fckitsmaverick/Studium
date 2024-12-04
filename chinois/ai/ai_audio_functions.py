import sounddevice as sd
import numpy as np
import wave

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def record_audio_manual(filename, samplerate=16000):
    """
    Record audio manually, starting and stopping with keyboard input.

    Args:
        filename (str): The name of the output WAV file.
        samplerate (int): The sample rate for the recording (default: 16000 Hz).
    """

    Prompt.ask("[bold magenta]Press Enter to start recording... (say exit if you want to exit)[/bold magenta]")
    console.print("[bold green]Recording started. Press Enter to stop recording.")

    audio_data = []

    def callback(indata, frames, time, status):
        """Callback function to capture audio data."""
        if status:
            console.print(f"Status: {status}")
        audio_data.append(indata.copy())  # Append a copy of the data to the list

    # Open the input stream
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16', callback=callback):
        Prompt.ask()  # Wait for the user to press Enter to stop recording
        console.print("[bold red]Recording stopped.[/bold red]")

    # Concatenate the audio data into a single array
    audio_data = np.concatenate(audio_data, axis=0)

    # Save the recorded audio as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())
    #console.print(f"[bold magenta]Audio saved as {filename}[/bold magenta]")



# Main Program
if __name__ == "__main__":
    output_file = "manual_recording.wav"
    record_audio_manual(output_file)
