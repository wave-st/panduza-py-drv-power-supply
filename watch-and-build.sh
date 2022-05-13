inotifywait -e close_write,moved_to,create -m -r panduza_drv_power_supply |
while read -r directory events filename; do
    echo "++++++++++++++++++ Change on $filename"

    # Suppose here that only one package is in the directory
    tar_filepath=`readlink -f ./dist/panduza_*.tar.gz`
    echo "Update from : $tar_filepath"
    python3 setup.py sdist bdist_wheel
    pip install --upgrade --ignore-installed $tar_filepath

done

