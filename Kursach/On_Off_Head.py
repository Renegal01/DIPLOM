import cv2
import dlib
import pygame
import sys
import numpy as np


class EyeTracker:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()
        self.screen_size = (640, 480)  # Размер окна
        # Создаем новое окно с рамками, чтобы его можно было перемещать
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        pygame.display.set_caption("Eye Tracker")

        # Инициализация детектора лиц и предиктора для детекции глаз
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Загрузите файл

        # Захват видео с веб-камеры
        self.cap = cv2.VideoCapture(0)

    def get_eye_points(self, shape):
        left_eye = shape[36:42]
        right_eye = shape[42:48]
        return left_eye, right_eye

    def draw_grid(self):
        # Рисуем знаки «плюс»
        for x in range(0, self.screen_size[0], 20):  # Разметка через каждые 20 пикселей
            pygame.draw.line(self.screen, (200, 200, 200), (x, self.screen_size[1] // 2 - 10), (x, self.screen_size[1] // 2 + 10))  # Вертикальная линия
        for y in range(0, self.screen_size[1], 20):  # Разметка через каждые 20 пикселей
            pygame.draw.line(self.screen, (200, 200, 200), (self.screen_size[0] // 2 - 10, y), (self.screen_size[0] // 2 + 10, y))  # Горизонтальная линия

    def run(self):
        # Основной цикл
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            ret, frame = self.cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Обнаружение лиц
            faces = self.detector(gray)
            for face in faces:
                # Определение ключевых точек на лице
                landmarks = self.predictor(gray, face)
                landmarks_points = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(68)]

                # Получение координат глаз
                left_eye, right_eye = self.get_eye_points(landmarks_points)

                # Преобразование в массив NumPy для расчета центра глаз
                left_eye_array = np.array(left_eye)
                right_eye_array = np.array(right_eye)

                # Получение центра глаз для отображения круга
                left_eye_center = tuple(map(int, left_eye_array.mean(axis=0)))
                right_eye_center = tuple(map(int, right_eye_array.mean(axis=0)))

                # Инвертирование координат по горизонтали
                left_eye_center = (self.screen_size[0] - left_eye_center[0], left_eye_center[1])
                right_eye_center = (self.screen_size[0] - right_eye_center[0], right_eye_center[1])

                # Очистка экрана
                self.screen.fill((255, 255, 255))  # Полностью белый фон для инверсии

                # Рисуем разлиновку в виде знаков «плюс»
                self.draw_grid()

                # Рисование кругов вокруг глаз (черные точки)
                pygame.draw.circle(self.screen, (0, 0, 0), left_eye_center, 20)  # Черные точки
                pygame.draw.circle(self.screen, (0, 0, 0), right_eye_center, 20)  # Черные точки

                # Обновление дисплея
                pygame.display.update()

            # Применение инверсии изображения
            frame = cv2.flip(frame, 1)  # Инвертируем изображение по горизонтали

            # Если необходимо, выводим видео для отладки
            cv2.imshow("Video", frame)

            # Остановка программы по нажатию 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    tracker = EyeTracker()
    tracker.run()
