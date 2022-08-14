pushd .
cd ..
call venv\Scripts\activate.bat
python -m black -l 192 yasf test_yasf setup.py
call deactivate
popd
