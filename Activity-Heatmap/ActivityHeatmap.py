import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


def generate_bee_activity_heatmap(video_path, output_dir='plots'):
    """Generates a heatmap of bee activity from a given video file."""
    # Extract the video filename without extension
    video_filename = os.path.splitext(os.path.basename(video_path))[0]

    # Initialize the video capture object
    cap = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    # Get video properties
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a heatmap matrix initialized to zeros
    heatmap = np.zeros((frame_height, frame_width), np.float32)

    # Initialize background subtractor
    background_subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=45)

    # Define a minimum contour area for considering as a bee
    min_bee_area = 45

    # Process each frame
    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale and blur
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

        # Apply background subtraction
        fg_mask = background_subtractor.apply(blurred_frame)

        # Threshold the mask to get binary image
        _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

        # Find contours (moving objects)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Update heatmap matrix
        for contour in contours:
            if cv2.contourArea(contour) > min_bee_area:
                x, y, w, h = cv2.boundingRect(contour)
                heatmap[y:y + h, x:x + w] += 1

    cap.release()

    # Normalize the heatmap to range 0-1
    heatmap = heatmap / np.max(heatmap)

    # Create output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Save the heatmap plot
    output_path = os.path.join(output_dir, f'{video_filename}.png')
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap, cmap='inferno', cbar=True)
    plt.title('Heatmap of Bee Activity at Beehive Entrance')
    plt.xlabel('Horizontal Position (pixels)')
    plt.ylabel('Vertical Position (pixels)')
    plt.savefig(output_path)
    plt.close()
    print(f"Heatmap saved: {output_path}")


# Set video directory and output plots directory
video_directory = '/media/aras/Data/Bee/Bee project/Video/13-4-2023/'
plots_directory = '/media/aras/Data/Bee/Bee project/Video/13-4-2023/Plots/'

# Create the output directory if it doesn't exist
os.makedirs(plots_directory, exist_ok=True)

# List all video files in the specified directory
video_files = [os.path.join(video_directory, f) for f in os.listdir(video_directory) if f.endswith('.avi')]

# Generate and save heatmaps for each video
for video_file in video_files:
    generate_bee_activity_heatmap(video_file, output_dir=plots_directory)
