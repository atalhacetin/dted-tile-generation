# DTED Tile Generation

Utilities to build a multi-level set of elevation tiles (BIL/ENVI) from SRTMGL3 v3 source data for use in viewers like NASA WorldWind, plus a comparison helper.

## Contents

| File | Purpose |
|------|---------|
| `extract_all_data.bat` / `extract_all_data.sh` | Unzip all downloaded SRTM `*.hgt.zip` archives into `SRTMGL3_003_unzipped/` |
| `create_vrt_from_hgt_files.bat` | Build `global_dem.vrt` (virtual mosaic of all `.hgt` files) using `gdalbuildvrt` |
| `global_dem.vrt` | Virtual raster (generated) used as the DEM source for tiling |
| `generate_dted_tiles.py` | Generate a level pyramid of 512×512 Int16 `.bil` tiles with 0 as NoData |
| `compare_dted_tiles.py` | Visual + histogram comparison between a generated tile and an existing DTED/WorldWind tile |

## Workflow Overview

1. Download SRTMGL3 (v003) 3 arc-second zip files into `SRTMGL3_003/` (already present in this repo structure placeholder).
2. Extract all archives into `SRTMGL3_003_unzipped/`.
3. Build a global virtual raster `global_dem.vrt` from the extracted `.hgt` files.
4. Run tile generation for desired levels (default 0–4) producing `../elevation_tiles/<level>/<row>/<row>_<col>.bil`.
5. Optionally compare a generated tile with an original DTED0/WorldWind tile to validate alignment and values.

## Detailed Steps

### 1. Extract Source Data

Windows (CMD):
```cmd
extract_all_data.bat
```

Linux / macOS:
```bash
chmod +x extract_all_data.sh
./extract_all_data.sh
```
Result: directory `SRTMGL3_003_unzipped/` containing many `.hgt` files.

### 2. Build Virtual Raster

Windows (provided batch):
```cmd
create_vrt_from_hgt_files.bat
```

Any platform (manual command):
```bash
gdalbuildvrt global_dem.vrt SRTMGL3_003_unzipped/*.hgt
```
This produces `global_dem.vrt` (referenced by the Python tiler).

### 3. Generate Tile Pyramid

Script parameters (see `generate_dted_tiles.py`):
- `SOURCE_DEM`: input (default `global_dem.vrt`)
- `OUTPUT_DIR`: relative output root (default `../elevation_tiles`)
- `TOP_LEVEL_DELTA`: angular span (degrees) of level 0 tiles (60.0)
- `TILE_WIDTH` / `TILE_HEIGHT`: output raster size per tile (512×512)

Run (example, all defaults levels 0–4):
```bash
python generate_dted_tiles.py --start 0 --end 4
```
Generate only level 2:
```bash
python generate_dted_tiles.py --start 2 --end 2
```

Output tree example:
```
../elevation_tiles/
  0/0/0_0.bil
  0/1/1_0.bil
  1/0/0_0.bil
  1/0/0_1.bil
  ...
```
Each tile has sidecar header files automatically created by GDAL (`.hdr`, etc.).

### 4. Tile Geometry Logic

For level L:
```
level_delta = TOP_LEVEL_DELTA / (2^L)
num_cols = 360 / level_delta
num_rows = 180 / level_delta
```
Bounds of (row, col):
```
max_lat = 90  - row * level_delta
min_lat = max_lat - level_delta
min_lon = -180 + col * level_delta
max_lon = min_lon + level_delta
```
Resampling performed with:
```
gdalwarp -t_srs EPSG:4326 -dstnodata 0 -te min_lon min_lat max_lon max_lat -ts 512 512 -r bilinear
```
Then translated to Int16 BIL with:
```
gdal_translate -ot Int16 -of EHdr -a_nodata 0
```
Zero (0) is consistently treated as NoData.

### 5. Compare Tiles (Optional)

Edit `level`, `row`, `column` constants in `compare_dted_tiles.py` to point at a generated and an original reference tile. Then:
```bash
python compare_dted_tiles.py
```
You will see:
- Original tile
- Generated tile
- Difference map (signed)
- Histogram of non-zero differences

Adjust the second file path logic (`5-row`) if your level has more or fewer rows—this was tailored for a small sample range.

## Requirements

Mandatory:
- GDAL (CLI tools: `gdalbuildvrt`, `gdalwarp`, `gdal_translate`) in PATH
- Python 3.8+

Python packages (install manually):
```bash
pip install numpy matplotlib
```
`numpy` is used implicitly by the comparison script; `matplotlib` only for visualization.

## Notes
- Output directory is outside repo root (`../elevation_tiles`). Adjust `OUTPUT_DIR` if you prefer an in-repo folder.
- Consider compressing intermediate `temp_tile.tif` creation if disk I/O becomes a bottleneck (e.g., add `-co COMPRESS=DEFLATE`).
- You may post-process to generate overviews or convert to Cloud Optimized GeoTIFF depending on downstream consumers.