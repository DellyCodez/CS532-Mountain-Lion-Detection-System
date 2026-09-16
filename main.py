import subprocess

dataset_dir = "/Users/vpartain/Desktop/WIP/my_dataset"
output_model_dir = "/Users/vpartain/Desktop/Testing/mountain_lion_model"

print("Starting BirdNET Custom Classifier Training...")

try:
    subprocess.run([
        "birdnet-train",
        "--output", output_model_dir,
        "--epochs", "20",            # Lowered to 20 loops since it's a small dataset
        "--batch_size", "4",         # Small batch size so it works with fewer total chunks
        "--crop_mode", "segments",   # CRITICAL: This chops your 2 files into dozens of 3-second samples
        "--val_split", "0.25",       # Forces BirdNET to dedicate 25% of chunks to validation
        dataset_dir
    ], check=True)
    print("\n Training complete! Your custom model is saved in:", output_model_dir)

except subprocess.CalledProcessError as e:
    print("\n Training failed. Error details:", e)
