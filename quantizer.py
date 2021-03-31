from playsound import playsound
import pygame.mixer as mixer
import pygame.midi as midi
import pygame
import keyboard
import time
import os

class Player():
    def __init__(self, tempo=60, metronome=True):
        pygame.init()
        mixer.init()
        midi.quit()
        midi.init()
        mixer.set_num_channels(32)

        # Fetches Playtron from list of available MIDI input devices
        self.input = self.get_input()

        # Creates list of samples from folder "samples". Place up to 16 audio files (.mp3, .wav, etc.) in this folder.
        self.samples = self.get_samples()

        # Tempo is passed to object in BPM, and here converted to value in seconds
        self.tempo = round(tempo / 60, 1)

        # Initiates quantized session
        self.session(tempo=self.tempo, metronome=metronome)

    def play(self, samples):
        # Checks if input has a reading, extracts the midi code(s) from note(s) in signal, and plays the note(s) 
        if self.input.poll():
            signal = self.input.read(1024)
            if signal[0][0][0] == 144:
                for note in signal:
                    self.samples[note[0][1]].play()

    def session(self, tempo, metronome):
        click = mixer.Sound('click.mp3')
        count = 4
        while True:
            if count % 4 == 1:
                if metronome:
                    click.play()
            self.play(self.samples)
            count += 1
            time.sleep(tempo / 4)

            if keyboard.is_pressed('space'):
                midi.quit()
                break

    @staticmethod
    def get_input():
        # Parses available MIDI devices (input and output)
        devices = [midi.get_device_info(device) for device in range(0, midi.get_count())]

        # Locates the Playtronic input ID
        for device in devices:
            if b'Playtron' in device[1] and device[2] == 1:
                return midi.Input(devices.index(device))

    @staticmethod
    def get_samples():
        samples = {}
        files = [file for file in os.listdir('samples')]

        # This index corresponds to the inidividual MIDI note values on the Playtronic - values from 36 to 51
        i = 36
        for file in files:
            if file.endswith('.mp3') or file.endswith('.wav'):
                samples[i] = mixer.Sound(f'samples\\{file}')
                i += 1
            if i >= 52:
                break
        return samples

if __name__ == "__main__":
    play = Player()