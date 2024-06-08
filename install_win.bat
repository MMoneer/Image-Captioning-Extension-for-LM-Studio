@echo off

:: Create a new Python environment
py -m venv myenv
myenv\Scripts\activate
:: Install requirements
pip install -r requirements.txt
echo Installation complete!
