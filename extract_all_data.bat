@echo off
rem Sets the script to not show the commands as they are executed.

rem Directory containing the zip files
set SRC_DIR=SRTMGL3_003
rem Directory to extract files into
set DEST_DIR=SRTMGL3_003_unzipped

rem Create the destination directory if it doesn't exist.
if not exist "%DEST_DIR%" (
    echo Creating directory: %DEST_DIR%
    mkdir "%DEST_DIR%"
)

rem Extract all .zip files in the source directory to the destination directory.
echo Starting extraction...
for %%f in ("%SRC_DIR%\*.zip") do (
    echo Extracting "%%f" to "%DEST_DIR%\"
    rem Use PowerShell's Expand-Archive command to unzip the files.
    rem The -Force parameter overwrites existing files, similar to unzip -o.
    powershell -command "Expand-Archive -Path '%%f' -DestinationPath '%DEST_DIR%' -Force"
)

echo.
echo All files extracted to "%DEST_DIR%".