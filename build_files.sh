

echo "Build start"

pip install -r requirements.txt
py manage.py collectstatic

echo " build end"