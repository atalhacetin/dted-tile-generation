#!/bin/bash
# This script creates a Virtual Raster (VRT) file from all .hgt files in a directory.
# It requires GDAL to be installed and accessible in your system's PATH.

# --- Configuration ---

# Set the directory containing the unzipped .hgt files.
# This should match the DEST_DIR from your unzip_files.sh script.
HGT_DIR="SRTMGL3_003_unzipped"

# Set the name for the output VRT file.
VRT_FILE="global_dem.vrt"

# --- Main Script Logic ---

echo "Creating VRT file: $VRT_FILE"
echo "From source HGT files in: $HGT_DIR"
echo ""

# Check if the source directory exists.
if [ ! -d "$HGT_DIR" ]; then
    echo "ERROR: Source directory '$HGT_DIR' not found."
    echo "Please run the unzip script first."
    exit 1
fi

# Use gdalbuildvrt to create the virtual raster.
# This command finds all .hgt files in the specified directory and mosaics them.
gdalbuildvrt "$VRT_FILE" "$HGT_DIR"/*.hgt

# Check if the command was successful by checking the exit code ($?).
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: gdalbuildvrt command failed."
    echo ""
    echo "Please make sure GDAL is installed on your system and that"
    echo "the 'gdalbuildvrt' command is available in your terminal's PATH."
    exit 1
fi

echo ""
echo "VRT file '$VRT_FILE' created successfully!"
