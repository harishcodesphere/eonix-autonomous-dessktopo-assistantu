@echo off
echo [Eonix] Installing Backend Dependencies...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python ../scripts/init_db.py
cd ..

echo [Eonix] Installing Frontend Dependencies...
cd frontend
npm install
cd ..

echo [Eonix] Installation Complete!
pause
