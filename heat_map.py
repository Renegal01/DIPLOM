import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from PIL import Image

# Load coordinates from the file
file_path = 'coordinates.txt'
coordinates = []
with open(file_path, 'r') as file:
    for line in file:
        x, y = line.split()
        coordinates.append((float(x), float(y)))  # Convert to float to handle decimal values

# Extract x and y values
x_coords, y_coords = zip(*coordinates)

# Create a 2D histogram for the heatmap with appropriate bin size
x_bins = np.linspace(0, 1920, 192)  # 192 bins to match resolution width-wise (can be adjusted for clarity)
y_bins = np.linspace(0, 1080, 108)  # 108 bins to match resolution height-wise (can be adjusted for clarity)
heatmap, xedges, yedges = np.histogram2d(x_coords, y_coords, bins=[x_bins, y_bins])

# Apply Gaussian filter to smooth the heatmap
heatmap = gaussian_filter(heatmap, sigma=5)

# Create the heatmap plot
plt.figure(figsize=(19.2, 10.8))
plt.imshow(heatmap.T, cmap='hot', origin='lower', extent=[0, 1920, 0, 1080])
plt.colorbar(label='Intensity')

# Add a background image
background_img = Image.open('background.png')  # Open the background image
background_img = background_img.resize((1920, 1080))  # Resize to match 1920x1080 resolution
plt.imshow(background_img, extent=[0, 1920, 0, 1080], alpha=0.5, aspect='auto')

plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')

# Display the heatmap
plt.show()
