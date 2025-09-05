@echo off
rem This script creates a Virtual Raster (VRT) file from all .hgt files in a directory.
rem It requires GDAL to be installed and accessible in your system's PATH.

rem --- Configuration ---

rem Set the directory containing the unzipped .hgt files.
rem This should match the DEST_DIR from your unzip_files.bat script.
set HGT_DIR=SRTMGL3_003_unzipped

rem Set the name for the output VRT file.
set VRT_FILE=global_dem.vrt

rem --- Main Script Logic ---

echo Creating VRT file: %VRT_FILE%
echo From source HGT files in: %HGT_DIR%
echo.

rem Check if the source directory exists.
if not exist "%HGT_DIR%" (
    echo ERROR: Source directory "%HGT_DIR%" not found.
    echo Please run the unzip script first.
    goto :eof
)

rem Use gdalbuildvrt to create the virtual raster.
rem This command finds all .hgt files in the specified directory and mosaics them.
gdalbuildvrt "%VRT_FILE%" "%HGT_DIR%\*.hgt"

rem Check if the command was successful by checking the error level.
if %errorlevel% neq 0 (
    echo.
    echo ERROR: gdalbuildvrt command failed.
    echo.
    echo Please make sure GDAL is installed on your system and that
    echo the 'gdalbuildvrt' command is available in your command prompt's PATH.
    goto :eof
)

echo.
echo VRT file "%VRT_FILE%" created successfully!
