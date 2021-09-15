rm -r dist && python3.7 setup.py sdist bdist_wheel && python3.7 -m  pip uninstall pyinsect-ggianna && python3.7 -m  pip install --user  -e .
