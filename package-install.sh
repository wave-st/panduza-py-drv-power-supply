tar_filepath=`readlink -f ./dist/panduza*.tar.gz`
echo "Update from : $tar_filepath"
python3 setup.py sdist bdist_wheel
pip install --upgrade --ignore-installed $tar_filepath
