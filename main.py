import os
import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime
import sounddevice as sd
import numpy as np
import subprocess
import threading
import time
import wavio  # Make sure to import the required library

class AudioRecorderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Recorder App")

        # Define sampling_rate and other attributes
        self.sampling_rate = 44100
        self.channels = 1
        self.record_button = ttk.Button(self.master, text="Record", command=self.start_recording)
        self.record_button.pack(pady=20)

        self.log_text = tk.Text(self.master, height=200, width=400, state=tk.DISABLED)
        self.log_text.pack()


    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.config(state=tk.DISABLED)  # Disable text widget for editing

    def record_audio(self, duration):
        recording = sd.rec(int(self.sampling_rate * duration), samplerate=self.sampling_rate, channels=self.channels, dtype='int16')
        sd.wait()
        return recording

    def save_audio(self, data, filename):
        try:
            path = "vcc2023/vcc2023_evaluation/VIVOSSPK01"
            ddir = os.path.join(os.getcwd(), path, filename)
            data_float = data.astype(np.float32) / 32767.0
            wavio.write(ddir, data_float, self.sampling_rate, sampwidth=3)
            print(f"Audio saved to {filename}")
        except Exception as e:
            print(f"Error saving audio: {e}")

    def start_recording(self):
        self.record_button.config(state=tk.DISABLED)  # Disable button during recording
        self.log_message("Recording started...")

        # Set the file name with the current date and time
        file_name = f"voice_{datetime.now().strftime('%d%m%Y_%H%M%S')}.wav"

        # Record audio for 15 seconds
        duration = 5  # seconds

        try:
            default_samplerate = sd.default.samplerate
            if default_samplerate is None:
                # Set a reasonable default sample rate
                default_samplerate = 44100

            recording = self.record_audio(duration)
            self.save_audio(recording, f"{file_name}")
            self.log_message(f"Recording saved as {file_name}")

            # Run the specified command in a separate thread after 15 seconds
            threading.Thread(target=self.run_command_after_delay, args=(file_name,), daemon=True).start()

        except Exception as e:
            self.log_message(f"Error during recording: {e}")

        # Enable the button after recording
        self.record_button.config(state=tk.NORMAL)
        self.log_message("Recording completed.")

    def run_command_after_delay(self, file_name):
        # Wait for 15 seconds before running the command
        time.sleep(2)

        # Run the specified command in a separate thread
        threading.Thread(target=self.run_command, args=(file_name,), daemon=True).start()

    def run_command(self, file_name):
        self.log_message("Executing the specified command...")

        start_time = time.time()  # Record start time

        precommand = [
            "python", "data_preprocessing/preprocess_vcc2023.py",
            "--data_directory", "vcc2023/vcc2023_evaluation",
            "--preprocessed_data_directory", "vcc2023_preprocessed/vcc2023_evaluation",
            "--speaker_ids", "VIVOSSPK01",
        ]

        # Specify the command to run
        command = [
            "python",
            "-W", "ignore::UserWarning",
            "-m", "mask_cyclegan_vc.test",
            "--name", "mask_cyclegan_vc_VIVOSSPK01_VIVOSSPK42",
            "--save_dir", "results/",
            "--preprocessed_data_dir", "vcc2023_preprocessed/vcc2023_evaluation",
            "--gpu_ids", "0",
            "--speaker_A_id", "VIVOSSPK01",
            "--speaker_B_id", "VIVOSSPK42",
            "--ckpt_dir", "results/mask_cyclegan_vc_VIVOSSPK01_VIVOSSPK42/ckpts",
            "--load_epoch", "2100",
            "--model_name", "generator_A2B"
        ]

        try:
            result = subprocess.run(precommand, check=True, capture_output=True, text=True)
            self.log_message(f"Command Output:\n{result.stdout}\n")
            # Redirect stdout and stderr to capture the command output
            result = subprocess.run(command, check=True, capture_output=True, text=True)

            # Update the log with the command output
            self.log_message(f"Command Output:\n{result.stdout}\n")

        except subprocess.CalledProcessError as e:
            # Update the log with the error message
            self.log_message(f"Error executing the command: {e}\n")

        finally:
            # Record end time and calculate execution time
            end_time = time.time()
            execution_time = end_time - start_time
            self.log_message(f"Execution Time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    root = tk.Tk()
    # root.geometry("500x500")
    root.geometry("500x500")
    app = AudioRecorderApp(root)
    root.mainloop()
