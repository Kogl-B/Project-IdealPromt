@echo off
echo ================================================
echo СОЗДАНИЕ ИСПОЛНЯЕМОГО ФАЙЛА LETTER GENERATOR
echo ================================================
echo.

echo Установка PyInstaller...
pip install pyinstaller
echo.

echo Создание .exe файла...
pyinstaller --onefile --windowed ^
    --name="LetterGenerator" ^
    --icon=NONE ^
    letter_generator_app.py
echo.

echo ================================================
echo Готово! Исполняемый файл находится в папке dist/
echo ================================================
pause
