pushd .
cd ..
call venv\Scripts\activate.bat 
mypy -m yasf
mypy -m test_yasf
call deactivate
popd
