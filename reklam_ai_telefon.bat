@echo off
cd /d %~dp0
streamlit run reklam_app_v2.py --server.enableCORS false --server.enableXsrfProtection false --server.headless true --server.address 0.0.0.0
pause
