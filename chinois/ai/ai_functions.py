from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

def take_input():
    audio = Prompt.ask("[bold magenta]Do you wish to use the audio input function ? (you will have to tell your answers instead of typing)", choices=["yes", "no"], default="no" ) 
    correction = Prompt.ask("[bold magenta]Do you wish to have a correction (and gradation) of each of your answers by the AI ? ", choices=["yes", "no"], default="no")
    return audio, correction