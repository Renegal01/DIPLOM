import cv2
import pyautogui
import numpy as np
from tkinter.filedialog import asksaveasfilename
import threading

# Глобальные переменные для отслеживания состояния записи
is_recording = False
video_writer = None
recording_thread = None

def toggle_screen_recording():
    global is_recording, video_writer, recording_thread

    if not is_recording:
        # Запрашиваем путь для сохранения файла
        file_path = asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])
        if file_path:
            # Получаем разрешение экрана
            screen_size = pyautogui.size()

            # Создаем VideoWriter для записи экрана
            video_writer = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc(*'XVID'), 20.0, screen_size)

            is_recording = True  # Установка состояния записи
            recording_thread = threading.Thread(target=start_recording)
            recording_thread.start()  # Запускаем запись в отдельном потоке
            print("Начата запись...")
            return True  # Успешный старт записи
    else:
        stop_recording()
        print("Запись остановлена.")
        return False  # Остановка записи

def start_recording():
    global video_writer, is_recording

    # Цикл записи экрана
    while is_recording:
        # Захватываем скриншот экрана
        screenshot = pyautogui.screenshot()

        # Преобразуем скриншот в массив numpy
        frame = np.array(screenshot)

        # Преобразуем цвета из RGB в BGR (для OpenCV)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Проверяем, что размеры кадра соответствуют ожидаемым
        frame = cv2.resize(frame, pyautogui.size())

        # Записываем кадр в файл
        video_writer.write(frame)

    # Освобождаем VideoWriter после завершения записи
    video_writer.release()

def stop_recording():
    global video_writer, is_recording
    is_recording = False  # Остановка записи

    if recording_thread and recording_thread.is_alive():
        recording_thread.join()  # Ожидаем завершения потока

    if video_writer:
        video_writer.release()  # Освобождаем ресурсы
        video_writer = None

def run_recorder():
    toggle_screen_recording()

