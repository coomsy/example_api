
python -m venv venv

.\venv\Scripts\activate

pip3 install -r requirements.txt


Write-Host 'Visit http://127.0.0.1:5000/, CTRL+C to stop, run "python -m flask run" to start again'

$env:FLASK_APP = "main.py"
python -m flask run