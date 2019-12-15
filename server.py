import os

import numpy as np
from scipy.io import wavfile
import speech_recognition as sr
import librosa
from wordcloud import WordCloud, ImageColorGenerator

from flask import Flask, flash, request, redirect, url_for, render_template, Response
from werkzeug.utils import secure_filename

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import io


UPLOAD_FOLDER = os.path.join('uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload", methods=['POST'])
def upload_file():
    from werkzeug.datastructures import FileStorage
    FileStorage(request.stream).save(os.path.join(app.config['UPLOAD_FOLDER'], 'saved_file.wav'))
    os.system("sed -i '1, 4d' {}".format(os.path.join(app.config['UPLOAD_FOLDER'], 'saved_file.wav')))
    return 'OK', 200

@app.route("/test_image", methods=['GET'])
def return_test_image():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x_points = range(100)
    axis.plot(x_points, [x**2 for x in x_points])

    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')


STOPWORDS = set('''а
будем
будет
будете
будешь
буду
будут
будучи
будь
будьте
бы
был
была
были
было
быть
в
вам
вами
вас
весь
во
вот
все
всё
всего
всей
всем
всём
всеми
всему
всех
всею
всея
всю
вся
вы
да
для
до
его
едим
едят
ее
её
ей
ел
ела
ем
ему
емъ
если
ест
есть
ешь
еще
ещё
ею
же
за
и
из
или
им
ими
имъ
их
к
как
кем
ко
когда
кого
ком
кому
комья
которая
которого
которое
которой
котором
которому
которою
которую
которые
который
которым
которыми
которых
кто
меня
мне
мной
мною
мог
моги
могите
могла
могли
могло
могу
могут
мое
моё
моего
моей
моем
моём
моему
моею
можем
может
можете
можешь
мои
мой
моим
моими
моих
мочь
мою
моя
мы
на
нам
нами
нас
наса
наш
наша
наше
нашего
нашей
нашем
нашему
нашею
наши
нашим
нашими
наших
нашу
не
него
нее
неё
ней
нем
нём
нему
нет
нею
ним
ними
них
но
о
об
один
одна
одни
одним
одними
одних
одно
одного
одной
одном
одному
одною
одну
он
она
оне
они
оно
от
по
при
с
сам
сама
сами
самим
самими
самих
само
самого
самом
самому
саму
свое
своё
своего
своей
своем
своём
своему
своею
свои
свой
своим
своими
своих
свою
своя
себе
себя
собой
собою
та
так
такая
такие
таким
такими
таких
такого
такое
такой
таком
такому
такою
такую
те
тебе
тебя
тем
теми
тех
то
тобой
тобою
того
той
только
том
томах
тому
тот
тою
ту
ты
у
уже
чего
чем
чём
чему
что
чтобы
эта
эти
этим
этими
этих
это
этого
этой
этом
этому
этот
этою
эту
я'''.split('\n'))

@app.route('/get_image', methods=['GET'])
def return_wordcloud():
    r = sr.Recognizer()
    basedir = os.path.abspath(os.path.dirname(__file__))

    audio, rate = librosa.load(os.path.join(basedir, 'uploads' , 'saved_file.wav'))

    y = (np.iinfo(np.int32).max * (audio/np.abs(audio).max())).astype(np.int32)
    wavfile.write(os.path.join(basedir, app.config['UPLOAD_FOLDER'], 'speech_2.wav'), rate = rate, data = y)

#    with sr.AudioFile(os.path.join(basedir, app.config['UPLOAD_FOLDER', 'speech_2.wav') as source:

    with sr.AudioFile(os.path.join(basedir, app.config['UPLOAD_FOLDER'], 'saved_file.wav')) as source:
        audio = r.record(source)

    text = r.recognize_google(audio, language='ru_RU')
    wordcloud = WordCloud(background_color='white', max_words=20, stopwords=STOPWORDS).generate(text)

    fig = Figure()

    axis = fig.add_subplot(1, 1, 1)
    axis.imshow(wordcloud)
    axis.axis('off')

    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)

    return Response(output.getvalue(), mimetype="image/png")
