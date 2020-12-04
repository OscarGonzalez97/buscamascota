#/bin/bash
cp -v buscamascota/settings.py.sample buscamascota/settings.py
cp -v .env.sample .env
echo ""
echo "This is a randomly generated secret key to put in your new .env"
KEY=$(python -c 'import random; print("".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]))')
echo "SECRET_KEY=$KEY"
echo ""
