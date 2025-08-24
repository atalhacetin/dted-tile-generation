import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
# Update these paths to your two .bil files
level = 1
row = 1
column = 3

file_path_1 = f"../worldwindjs/DTED0/{level}/{row}/{row}_{column}.bil"
file_path_2 = f"../elevation_tiles/{level}/{5-row}/{5-row}_{column}.bil"

# The dimensions of your tiles (e.g., 512x512)
TILE_DIMENSIONS = (512, 512)

try:
    # Read the first file's binary data into a NumPy array.
    array1 = np.fromfile(file_path_1, dtype=np.int16)
    print(f"✅ Loaded '{file_path_1}' (Total values: {array1.size})")

    # Read the second file.
    array2 = np.fromfile(file_path_2, dtype=np.int16)
    print(f"✅ Loaded '{file_path_2}' (Total values: {array2.size})")

    # --- Comparison ---
    if array1.size != array2.size:
        print("\n❌ Error: Files have different sizes and cannot be compared.")
    else:
        # --- PLOTTING LOGIC ---
        print("\n📈 Generating plots...")

        # Reshape the 1D arrays into 2D maps for plotting
        map1 = array1.reshape(TILE_DIMENSIONS)
        map2 = array2.reshape(TILE_DIMENSIONS)
        
        # Calculate the difference map
        difference_map = map1.astype(float) - map2.astype(float)

        # Create a figure with a 2x2 grid of subplots
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Elevation Tile Comparison', fontsize=16)

        # Find the min and max elevation across both tiles for a consistent color scale
        vmin = min(map1.min(), map2.min())
        vmax = max(map1.max(), map2.max())

        # 1. Plot the first tile (Original)
        im1 = axs[0, 0].imshow(map1, cmap='terrain', vmin=vmin, vmax=vmax)
        axs[0, 0].set_title('Original Tile (DTED0)')
        fig.colorbar(im1, ax=axs[0, 0], label='Elevation (meters)')

        # 2. Plot the second tile (Generated)
        im2 = axs[0, 1].imshow(map2, cmap='terrain', vmin=vmin, vmax=vmax)
        axs[0, 1].set_title('Generated Tile')
        fig.colorbar(im2, ax=axs[0, 1], label='Elevation (meters)')

        # 3. Plot the Difference Map
        im3 = axs[1, 0].imshow(difference_map, cmap='coolwarm')
        axs[1, 0].set_title('Difference Map')
        fig.colorbar(im3, ax=axs[1, 0], label='Elevation Difference (m)')
        
        # 4. Plot the Histogram of Differences
        non_zero_diffs = difference_map[difference_map != 0]
        axs[1, 1].hist(non_zero_diffs, bins=50, color='gray')
        axs[1, 1].set_title('Histogram of Differences')
        axs[1, 1].set_xlabel('Difference in Elevation (m)')
        axs[1, 1].set_ylabel('Frequency')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to make room for suptitle
        plt.show()

except FileNotFoundError as e:
    print(e)
    print(f"❌ Error: A file was not found. Please check your paths.")
except Exception as e:
    print(f"An error occurred: {e}")