@echo off
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
if "%~1"=="" (
    echo Usage: query.bat "YOUR SQL QUERY"
    echo Example: query.bat "SELECT * FROM product_categories"
    exit /b
)
"C:\Users\abhij\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts\wren.exe" --sql "%~1"
