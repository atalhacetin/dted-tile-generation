import os
import subprocess
import math
import argparse

# --- Configuration ---
SOURCE_DEM = "global_dem.vrt" 
OUTPUT_DIR = "../elevation_tiles"
TOP_LEVEL_DELTA = 60.0
TILE_WIDTH = 512
TILE_HEIGHT = 512

# --- Main Script Logic ---

def run_command(command):
    """Executes a command line process."""
    print(f"Executing: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Return Code: {e.returncode}")
        print(f"Stderr: {e.stderr}")
        print(f"Stdout: {e.stdout}")
        raise

def generate_tiles(start_level, end_level):
    """Main function to generate all elevation tiles."""
    if not os.path.exists(SOURCE_DEM):
        print(f"Error: Source DEM file not found at '{SOURCE_DEM}'")
        return

    print("Starting tile generation...")
    
    for level in range(start_level, end_level + 1):
        level_delta = TOP_LEVEL_DELTA / (2 ** level)
        num_cols = int(360 / level_delta)
        num_rows = int(180 / level_delta)
        
        print(f"\nProcessing Level {level} ({num_rows} rows, {num_cols} cols)...")

        for row in range(num_rows):
            for col in range(num_cols):
                max_lat = 90 - (row * level_delta)
                min_lat = max_lat - level_delta
                min_lon = -180 + (col * level_delta)
                max_lon = min_lon + level_delta

                level_dir = os.path.join(OUTPUT_DIR, str(level))
                row_dir = os.path.join(level_dir, str(row))
                os.makedirs(row_dir, exist_ok=True)

                output_filename = f"{row}_{col}.bil"
                output_path = os.path.join(row_dir, output_filename)
                
                temp_tif = os.path.join(row_dir, "temp_tile.tif")

                # Command 1: gdalwarp
                # FIXED: Added -dstnodata 0 to fill empty areas with 0 from the start.
                gdalwarp_cmd = (
                    f"gdalwarp -q "
                    f"-t_srs EPSG:4326 "
                    f"-dstnodata 0 "  # <-- KEY CHANGE IS HERE
                    f"-te {min_lon} {min_lat} {max_lon} {max_lat} "
                    f"-ts {TILE_WIDTH} {TILE_HEIGHT} "
                    f"-r bilinear "
                    f'"{SOURCE_DEM}" "{temp_tif}"'
                )

                # Command 2: gdal_translate
                # This correctly labels 0 as the no-data value in the final metadata.
                gdal_translate_cmd = (
                    f"gdal_translate -q "
                    f"-ot Int16 "
                    f"-of EHdr "
                    f"-a_nodata 0 "
                    f'"{temp_tif}" "{output_path}"'
                )
                
                try:
                    run_command(gdalwarp_cmd)
                    run_command(gdal_translate_cmd)
                except subprocess.CalledProcessError as e:
                    print(f"Stopping script due to error on tile {level}/{row}/{col}.")
                    return
                finally:
                    if os.path.exists(temp_tif):
                        os.remove(temp_tif)
                    if os.path.exists(f"{temp_tif}.aux.xml"):
                        os.remove(f"{temp_tif}.aux.xml")
                        
    print("\n✅ Tile generation complete!")


if __name__ == "__main__":
    # --- New: Command-line argument parsing ---
    parser = argparse.ArgumentParser(description="Generate elevation tiles for WorldWind.")
    parser.add_argument(
        "--start",
        type=int,
        default=0,
        help="The starting level to generate (inclusive, e.g., 0)."
    )
    parser.add_argument(
        "--end",
        type=int,
        default=4,
        help="The ending level to generate (inclusive, e.g., 4)."
    )
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    generate_tiles(start_level=args.start, end_level=args.end)