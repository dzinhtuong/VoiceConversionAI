import tkinter as tk
from tkinter import ttk
from datetime import datetime
import sounddevice as sd
import numpy as np
import subprocess
import threading
import time

class AudioRecorderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Recorder App")

        # Create GUI elements
        self.record_button = ttk.Button(self.master, text="Record", command=self.start_recording)
        self.record_button.pack(pady=20)

        self.log_text = tk.Text(self.master, height=10, width=50, state=tk.DISABLED)
        self.log_text.pack()

    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.config(state=tk.DISABLED)  # Disable text widget for editing

    def print_input_devices(self):
        # Print information about available input devices
        input_devices = sd.query_devices(kind='input')
        self.log_message("Available Input Devices:")
        for i, device in enumerate(input_devices):
            self.log_message(f"{i + 1}. {device['name']} - Channels: {device['max_input_channels']}, Samplerate: {device['default_samplerate']} Hz")

    def start_recording(self):
        self.record_button.config(state=tk.DISABLED)  # Disable button during recording
        self.log_message("Recording started...")

        # Print information about available input devices
        self.print_input_devices()

        # Set the file name with the current date and time
        file_name = f"voice_{datetime.now().strftime('%d%m%Y_%H%M%S')}.wav"

        # Record audio for 15 seconds
        duration = 15  # seconds

        # Adjust the following line based on the correct audio device and channels
        input_device = 0  # Change this value to the index of the desired input device
        fs = sd.query_devices(input_device)['default_samplerate']
        recording = sd.rec(int(fs * duration), samplerate=fs, channels=1, dtype=np.int16, device=input_device)

        # Run the specified command in a separate thread after 15 seconds
        threading.Thread(target=self.run_command_after_delay, args=(file_name,), daemon=True).start()

        sd.wait()
        sd.write(file_name, recording, fs)
        self.log_message(f"Recording saved as {file_name}")

        # Enable the button after recording
        self.record_button.config(state=tk.NORMAL)
        self.log_message("Recording completed.")

    def run_command_after_delay(self, file_name):
        # Wait for 15 seconds before running the command
        time.sleep(15)

        # Run the specified command in a separate thread
        threading.Thread(target=self.run_command, args=(file_name,), daemon=True).start()

    def run_command(self, file_name):
        self.log_message("Executing the specified command...")

        start_time = time.time()  # Record start time

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
            "--ckpt_dir", "/data1/cycleGAN_VC3/mask_cyclegan_vc_VIVOSSPK01_VIVOSSPK42/ckpts",
            "--load_epoch", "1800",
            "--model_name", "generator_A2B",
            "--input_audio", file_name  # Pass the recorded audio file as an argument
        ]

        try:
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
    app = AudioRecorderApp(root)
    root.mainloop()
