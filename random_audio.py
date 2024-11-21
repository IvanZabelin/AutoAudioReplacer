import os
import random
import ffmpeg

# Папки для видео, аудио и выходных файлов
VIDEO_FOLDER = "videos"
AUDIO_FOLDER = "audios"
OUTPUT_FOLDER = "output_videos"

# Создаем папку для выходных файлов, если ее нет
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def get_random_file(folder, extensions):
    """
    Выбирает случайный файл с указанным расширением из папки.
    """
    files = [f for f in os.listdir(folder) if f.lower().endswith(extensions)]
    if not files:
        raise ValueError(f"Файл с расширением {extensions} не найден в папке {folder}")
    return os.path.join(folder, random.choice(files))


def get_first_file(folder, extensions):
    """
    Выбирает первый файл с указанным расширением из папки.
    """
    files = [f for f in os.listdir(folder) if f.lower().endswith(extensions)]
    if not files:
        raise ValueError(f"Файл с расширением {extensions} не найден в папке {folder}")
    return os.path.join(folder, files[0])


def replace_audio(video_path, audio_path, output_path):
    """
    Заменяет аудиодорожку в видео, обрезая аудио, если оно длиннее.
    """
    # Получаем информацию о длительности видео и аудио
    video_info = ffmpeg.probe(video_path)
    audio_info = ffmpeg.probe(audio_path)
    video_duration = float(video_info['format']['duration'])
    audio_duration = float(audio_info['format']['duration'])

    # Проверяем длительность аудио и обрезаем "на лету", если оно длиннее видео
    audio_input = ffmpeg.input(audio_path)
    if audio_duration > video_duration:
        audio_input = ffmpeg.input(audio_path, ss=0, t=video_duration)

    # Заменяем аудиодорожку, не сохраняя промежуточный файл
    (
        ffmpeg
        .input(video_path)
        .output(audio_input, output_path, vcodec="copy", acodec="aac", strict="experimental")
        .run(overwrite_output=True)
    )
    print(f"Создан файл: {output_path}")


# Основной блок программы
try:
    # Выбираем случайное видео и аудио
    video_files = [os.path.join(VIDEO_FOLDER, f) for f in os.listdir(VIDEO_FOLDER) if f.lower().endswith((".mp4", ".mkv", ".avi", ".mov"))]
    audio_file = get_random_file(AUDIO_FOLDER, (".mp3", ".wav"))

    for video_file in video_files:
        output_file = os.path.join(OUTPUT_FOLDER, f"output_{os.path.basename(video_file)}")

        print(f"Выбрано видео: {video_file}")
        print(f"Выбрано аудио: {audio_file}")

        # Заменяем аудиодорожку
        replace_audio(video_file, audio_file, output_file)

except Exception as e:
    print(f"Ошибка: {e}")
