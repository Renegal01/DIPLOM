import tkinter as tk
import subprocess
import sys
from screen_recorder import toggle_screen_recording  # Импортируем функцию из screen_recorder.py

# Глобальная переменная для отслеживания состояния
is_tracking = False
process = None  # Переменная для хранения процесса трекера

def toggle_eye_tracker():
    global is_tracking, process

    if not is_tracking:
        process = subprocess.Popen([sys.executable, "On_Off_Head.py"])
        button.config(text="Отключить отображение головы")
    else:
        if process:
            process.terminate()  # Останавливаем процесс
            process = None
        button.config(text="Отобразить положение головы")

    is_tracking = not is_tracking  # Переключаем состояние

def start_stop_recording():
    if toggle_screen_recording():  # Запускаем или останавливаем запись
        recording_button.config(text="Остановить запись")
    else:
        recording_button.config(text="Записать экран")

# Создаем основное окно
root = tk.Tk()
root.title("Eye Tracker Interface")
root.geometry("300x200")

# Создаем кнопку для отображения головы
button = tk.Button(root, text="Отобразить положение головы", command=toggle_eye_tracker)
button.pack(pady=20)

# Создаем кнопку для записи экрана
recording_button = tk.Button(root, text="Записать экран", command=start_stop_recording)
recording_button.pack(pady=20)

# Запуск главного цикла приложения
root.mainloop()
