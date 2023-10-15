#pip install pydub argparse
import os
import argparse
from pydub import AudioSegment

def calculate_total_duration(folder_path):
    total_duration = 0  # Total duration in milliseconds

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.mp3', '.wav', '.ogg', '.flac')):  # Add more audio formats if needed
            file_path = os.path.join(folder_path, filename)

            # Load the audio file and get its duration in milliseconds
            audio = AudioSegment.from_file(file_path)
            duration = len(audio)  # Duration in milliseconds

            # Add the duration of this audio file to the total duration
            total_duration += duration

    # Convert total duration to minutes and seconds
    total_duration_seconds = total_duration / 1000
    total_minutes = total_duration_seconds // 60
    total_seconds = total_duration_seconds % 60

    return total_duration, total_minutes, total_seconds

if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Calculate the total duration of audio files in a folder")
    parser.add_argument("--path", type=str, help="Path to the folder containing audio files")

    # Parse the arguments
    args = parser.parse_args()

    # Check if the --path argument is provided
    if args.path:
        folder_path = args.path
        # Calculate the total duration
        total_duration, total_minutes, total_seconds = calculate_total_duration(folder_path)

        # Print the results
        print(f'Total duration of audio files in the folder: {total_duration} milliseconds')
        print(f'Total duration: {total_minutes} minutes and {total_seconds:.2f} seconds')
    else:
        print("Please provide a valid folder path using --path.")
