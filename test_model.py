import os
import subprocess
import glob
import csv

audio_to_test = "/Users/vpartain/Desktop/WIP/my_dataset/mountain_lion/*.wav"
model_file = "/Users/vpartain/Desktop/WIP/mountain_lion_model.tflite"
output_dir = "/Users/vpartain/Desktop/WIP/results"

os.makedirs(output_dir, exist_ok=True)

print("Analyzing audio file for Mountain Lion sounds...")

try:
    # Run birdnet-analyze with lower min_conf to capture raw predictions
    subprocess.run([
        "birdnet-analyze",
        "--classifier", model_file,
        "--output", output_dir,
        "--min_conf", "0.10",
        audio_to_test
    ], check=True)

    print("\nAnalysis complete!\n")

    # Locate the output file created by BirdNET
    result_files = glob.glob(os.path.join(output_dir, "*.txt")) + glob.glob(os.path.join(output_dir, "*.csv"))

    if result_files:
        result_file = result_files[0]

        mountain_lion_detected = False
        high_confidence_matches = []

        # Read tab-separated output file
        with open(result_file, "r") as f:
            reader = csv.DictReader(f, delimiter="\t")

            for row in reader:
                confidence = float(row.get("Confidence", 0))
                species = row.get("Common Name", "") or row.get("Scientific Name", "")

                # Check threshold (> 0.40)
                if confidence >= 0.40:
                    mountain_lion_detected = True
                    start_time = row.get("Start (s)", "N/A")
                    end_time = row.get("End (s)", "N/A")
                    high_confidence_matches.append((start_time, end_time, confidence, species))

        print("--- VERDICT ---")
        if mountain_lion_detected:
            print(" HIGH POSSIBILITY OF MOUNTAIN LION DETECTED! (Confidence >= 0.40)\n")
            print("Detections:")
            for start, end, conf, sp in high_confidence_matches:
                print(f" - [{start}s - {end}s] Species: {sp} | Confidence: {conf:.2%}")
        else:
            print(" NO HIGH LIKELIHOOD DETECTED (No detections above 0.40 confidence).")

    else:
        print("Analysis finished, but no output file was found.")

except subprocess.CalledProcessError as e:
    print("\nAnalysis failed. Error details:", e)