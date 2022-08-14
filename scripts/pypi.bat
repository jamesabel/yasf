pushd .
cd ..
del /Q yasf.egg-info\*.*
del /Q build\*.*
del /Q dist\*.*
copy README.md yasf
copy /Y LICENSE LICENSE.txt
venv\Scripts\python.exe setup.py bdist_wheel
venv\Scripts\twine upload dist/*
popd
