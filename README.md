python3 -m venv venv

source venv/bin/activate

pip3 install google-generativeai

echo ".env" >> .gitignore

git add .gitignore

git commit -m "Remove .env from tracking"            

npm install dotenv

pip3 install python-dotenv

pip3 install flask

python3 main.py
