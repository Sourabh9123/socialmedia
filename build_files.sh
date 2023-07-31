

echo "Build start"

pip install -r requirements.txt
python3.10 manage.py collectstatic

echo " build end"