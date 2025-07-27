@echo off
echo Starting Business Dashboard Application...
echo.

REM Change to the dashboard directory
cd /d "c:\DASHBOARD DEVELOPMENT"

REM Generate sample data if it doesn't exist
if not exist "sales_data.csv" (
    echo Generating sample business data...
    "C:/Users/deeps/AppData/Local/Programs/Python/Python311/python.exe" data_generator.py
    echo.
)

REM Start the dashboard
echo Launching interactive dashboard...
echo Dashboard will be available at: http://localhost:8050
echo Press Ctrl+C to stop the dashboard
echo.

"C:/Users/deeps/AppData/Local/Programs/Python/Python311/python.exe" dashboard_advanced.py

pause
