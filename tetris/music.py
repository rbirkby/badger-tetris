"""
Tetris theme - (Korobeiniki)
Connect a piezo buzzer or speaker to a GPIO pin.
More songs available at https://github.com/robsoncouto/arduino-songs

Original C code by Robson Couto, 2019
Converted to MicroPython for Raspberry Pi Pico
"""

import time

from machine import PWM, Pin

# Musical note definitions (frequencies in Hz)
NOTE_B0 = 31
NOTE_C1 = 33
NOTE_CS1 = 35
NOTE_D1 = 37
NOTE_DS1 = 39
NOTE_E1 = 41
NOTE_F1 = 44
NOTE_FS1 = 46
NOTE_G1 = 49
NOTE_GS1 = 52
NOTE_A1 = 55
NOTE_AS1 = 58
NOTE_B1 = 62
NOTE_C2 = 65
NOTE_CS2 = 69
NOTE_D2 = 73
NOTE_DS2 = 78
NOTE_E2 = 82
NOTE_F2 = 87
NOTE_FS2 = 93
NOTE_G2 = 98
NOTE_GS2 = 104
NOTE_A2 = 110
NOTE_AS2 = 117
NOTE_B2 = 123
NOTE_C3 = 131
NOTE_CS3 = 139
NOTE_D3 = 147
NOTE_DS3 = 156
NOTE_E3 = 165
NOTE_F3 = 175
NOTE_FS3 = 185
NOTE_G3 = 196
NOTE_GS3 = 208
NOTE_A3 = 220
NOTE_AS3 = 233
NOTE_B3 = 247
NOTE_C4 = 262
NOTE_CS4 = 277
NOTE_D4 = 294
NOTE_DS4 = 311
NOTE_E4 = 330
NOTE_F4 = 349
NOTE_FS4 = 370
NOTE_G4 = 392
NOTE_GS4 = 415
NOTE_A4 = 440
NOTE_AS4 = 466
NOTE_B4 = 494
NOTE_C5 = 523
NOTE_CS5 = 554
NOTE_D5 = 587
NOTE_DS5 = 622
NOTE_E5 = 659
NOTE_F5 = 698
NOTE_FS5 = 740
NOTE_G5 = 784
NOTE_GS5 = 831
NOTE_A5 = 880
NOTE_AS5 = 932
NOTE_B5 = 988
NOTE_C6 = 1047
NOTE_CS6 = 1109
NOTE_D6 = 1175
NOTE_DS6 = 1245
NOTE_E6 = 1319
NOTE_F6 = 1397
NOTE_FS6 = 1480
NOTE_G6 = 1568
NOTE_GS6 = 1661
NOTE_A6 = 1760
NOTE_AS6 = 1865
NOTE_B6 = 1976
NOTE_C7 = 2093
NOTE_CS7 = 2217
NOTE_D7 = 2349
NOTE_DS7 = 2489
NOTE_E7 = 2637
NOTE_F7 = 2794
NOTE_FS7 = 2960
NOTE_G7 = 3136
NOTE_GS7 = 3322
NOTE_A7 = 3520
NOTE_AS7 = 3729
NOTE_B7 = 3951
NOTE_C8 = 4186
NOTE_CS8 = 4435
NOTE_D8 = 4699
NOTE_DS8 = 4978
REST = 0

# Change this to make the song slower or faster
tempo = 144

# Notes of the melody followed by the duration.
# A 4 means a quarter note, 8 an eighth, 16 sixteenth, so on
# Negative numbers are used to represent dotted notes,
# so -4 means a dotted quarter note, that is, a quarter plus an eighth
melody = [
    # Based on the arrangement at https://www.flutetunes.com/tunes.php?id=192
    NOTE_E5,
    4,
    NOTE_B4,
    8,
    NOTE_C5,
    8,
    NOTE_D5,
    4,
    NOTE_C5,
    8,
    NOTE_B4,
    8,
    NOTE_A4,
    4,
    NOTE_A4,
    8,
    NOTE_C5,
    8,
    NOTE_E5,
    4,
    NOTE_D5,
    8,
    NOTE_C5,
    8,
    NOTE_B4,
    -4,
    NOTE_C5,
    8,
    NOTE_D5,
    4,
    NOTE_E5,
    4,
    NOTE_C5,
    4,
    NOTE_A4,
    4,
    NOTE_A4,
    8,
    NOTE_A4,
    4,
    NOTE_B4,
    8,
    NOTE_C5,
    8,
    NOTE_D5,
    -4,
    NOTE_F5,
    8,
    NOTE_A5,
    4,
    NOTE_G5,
    8,
    NOTE_F5,
    8,
    NOTE_E5,
    -4,
    NOTE_C5,
    8,
    NOTE_E5,
    4,
    NOTE_D5,
    8,
    NOTE_C5,
    8,
    NOTE_B4,
    4,
    NOTE_B4,
    8,
    NOTE_C5,
    8,
    NOTE_D5,
    4,
    NOTE_E5,
    4,
    NOTE_C5,
    4,
    NOTE_A4,
    4,
    NOTE_A4,
    4,
    REST,
    4,
    NOTE_E5,
    4,
    NOTE_B4,
    8,
    NOTE_C5,
    8,
    NOTE_D5,
    4,
    NOTE_C5,
    8,
    NOTE_B4,
    8,
    NOTE_A4,
    4,
    NOTE_A4,
    8,
    NOTE_C5,
    8,
    NOTE_E5,
    4,
    NOTE_D5,
    8,
    NOTE_C5,
    8,
    NOTE_B4,
    -4,
    NOTE_C5,
    8,
    NOTE_D5,
    4,
    NOTE_E5,
    4,
    NOTE_C5,
    4,
    NOTE_A4,
    4,
    NOTE_A4,
    8,
    NOTE_A4,
    4,
    NOTE_B4,
    8,
    NOTE_C5,
    8,
    NOTE_D5,
    -4,
    NOTE_F5,
    8,
    NOTE_A5,
    4,
    NOTE_G5,
    8,
    NOTE_F5,
    8,
    NOTE_E5,
    -4,
    NOTE_C5,
    8,
    NOTE_E5,
    4,
    NOTE_D5,
    8,
    NOTE_C5,
    8,
    NOTE_B4,
    4,
    NOTE_B4,
    8,
    NOTE_C5,
    8,
    NOTE_D5,
    4,
    NOTE_E5,
    4,
    NOTE_C5,
    4,
    NOTE_A4,
    4,
    NOTE_A4,
    4,
    REST,
    4,
    NOTE_E5,
    2,
    NOTE_C5,
    2,
    NOTE_D5,
    2,
    NOTE_B4,
    2,
    NOTE_C5,
    2,
    NOTE_A4,
    2,
    NOTE_GS4,
    2,
    NOTE_B4,
    4,
    REST,
    8,
    NOTE_E5,
    2,
    NOTE_C5,
    2,
    NOTE_D5,
    2,
    NOTE_B4,
    2,
    NOTE_C5,
    4,
    NOTE_E5,
    4,
    NOTE_A5,
    2,
    NOTE_GS5,
    2,
]

# Calculate the number of notes
notes = len(melody) // 2

# Calculate the duration of a whole note in ms (60s/tempo)*4 beats
wholenote = (60000 * 4) // tempo


def play_song(buzzer_pin=15):
    """
    Play the Tetris theme song.

    Args:
        buzzer_pin: GPIO pin number for the piezo buzzer (default: 15)
    """
    pwm = PWM(Pin(buzzer_pin))

    try:
        # Iterate over the notes of the melody
        # The array is twice the number of notes (notes + durations)
        for i in range(0, len(melody), 2):
            # Calculate the duration of each note
            divider = melody[i + 1]

            if divider > 0:
                # Regular note, just proceed
                note_duration = wholenote // divider
            else:
                # Dotted notes are represented with negative durations
                note_duration = wholenote // abs(divider)
                note_duration = int(note_duration * 1.5)  # Increase duration by half for dotted notes

            # Play the note for 90% of the duration, leaving 10% as a pause
            note_freq = melody[i]

            if note_freq == 0:
                # REST - no sound
                pwm.duty_u16(0)
            else:
                # Play the note
                pwm.freq(note_freq)
                pwm.duty_u16(32768)  # 50% duty cycle

            # Wait for 90% of the duration
            time.sleep_ms(int(note_duration * 0.9))

            # Stop the waveform generation before the next note (10% pause)
            pwm.duty_u16(0)
            time.sleep_ms(int(note_duration * 0.1))

    finally:
        pwm.deinit()


# Example usage:
# play_song(15)  # Use GPIO 15 for buzzer
