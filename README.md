Информационная системы поддержки мобильного приложения обработки голосовых сообщений

Список необходимых для работы библиотек находится в requirements.txt.

Автоматическая установка:

```
pip install -r ./requirements.txt
```

Для предобработки звукового потока необходима библиотека kaldi:
https://kaldi-asr.org/doc/install.html

Для использования мобильного клиента локально необходим фреймворк Flutter (нужен только Flutter SDK):
https://habr.com/ru/articles/741248/


1. Обучение нейронных сетей

Так как большинство датасетов не придерживаются какой-то одной структуры, автоматизация работы с ними затруднительна.

Ниже описана схема систематизации датасета.

В директорию audio положить папку с звуковыми файлами для обучения и .csv файлом, содержащим как минимум поля:
* "path" (адрес звукового файла относительно .csv файла)
* "name" (название звукового файла)
* "speaker" (идентификатор диктора для данного файла)
* "class" (класс, к которому принадлежит звуковой файл. Если классов несколько, перечислить через запятую)

В файле prepare_data.py указать используемые для обучения файлы. Шаблон:

```
import os
import wave
import csv

conv_audio_dir = os.path.abspath("./audio/converted/") + "/"

scp_file = open("./input/data.scp", "w")
stm_file = open("./input/data.stm", "w")

X_DIR = os.path.abspath("Путь до папки с .csv") + "/"
X_CSV = open(X_DIR + "имя .csv файла", "r")
reader = csv.DictReader(X_CSV)
for row in reader:
    print("Doing " + row["path"])
    scp_file.write(row["name"] + " " + conv_audio_dir + row["name"].split(".")[0] + ".wav\n")
    os.system("ffmpeg -y -i " + X_DIR + row["path"] + " -vn -ac 1 -ar 16000 " + conv_audio_dir + row["name"].split(".")[0] + ".wav")
    with wave.open(conv_audio_dir + row["name"].split(".")[0] + ".wav") as mywav:
        duration_seconds = mywav.getnframes() / mywav.getframerate()
        stm_file.write(row["name"] + " 0 " + row["speaker"] + " 0.00 " + str(duration_seconds) + " <" + row["class"] + "> _\n")

...

X_CSV.close()

...

scp_file.close()
stm_file.close()
```

Для обучения:

```
export KALDI_ROOT=*расположение папки kaldi*
python3 ./run.py
```

Возможные действия:

* *Подготовить данные* - конвертирует указанные звуковые файлы и создает вспомогательные файлы `wrkdir/input/data.stm` и `wrkdir/input/data.scp` 

* *Извлечь коэффициенты* - использует`wrkdir/input/data.stm` и `wrkdir/input/data.scp` для создания файла `wrkdir/output/xvector.ark`, содержащий звуковые коэффициенты для указанных файлов

* *Обучить модель* - создает модель с параметрами по умолчанию, обученную на полученных коэффициентах

* *Проверить модель* - получить отчет о работе обученной модели на текущем `wrkdir/output/xvector.ark`

* *Выйти*



2. Запуск сервера

```
cd server_dir
export KALDI_ROOT=*расположение папки kaldi*
uvicorn server:app
```

3. Запуск клиента на компьютере

```
cd "Flutter client"/client
flutter run
```

Запись и воспроизведение работает только на настоящем телефоне из-за особенностей доступа к микрофону. 

На сервер отправляется файл /tmp/temp.wav. Над кнопкой посылки можно выбрать одну из доступных на сервере моделей.

Сервер должен уже работать, когда приложение запускается, чтобы оно могло получить список моделей.

Нейронные сети лучше всего спарвляются с классификацией по характеристикам голоса.

Лучше всего они будут справляться с идентификацией диктора или классификацией по тону / высоте и пр. голоса.
