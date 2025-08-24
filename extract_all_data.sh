#!/bin/bash

# Directory containing the zip files
SRC_DIR="SRTMGL3_003"
# Directory to extract files into
DEST_DIR="SRTMGL3_003_unzipped"

# Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Extract all .zip files in the source directory to the destination directory
for zipfile in "$SRC_DIR"/*.zip; do
	echo "Extracting $zipfile to $DEST_DIR..."
	unzip -o "$zipfile" -d "$DEST_DIR"
done

echo "All files extracted to $DEST_DIR."
