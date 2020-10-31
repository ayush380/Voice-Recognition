import errno

from django.shortcuts import render
from django.http import HttpResponse
import os
import wave


# Create your views here.
from rest_framework.decorators import api_view


def home(request):
    print("in home")
    return render(request, 'index.html')


@api_view(['GET', 'POST'])
def blah(request):
    print(request.body)
    print("in Blah")
    audio_data = request.FILES.get('audio_data')
    if not os.path.exists(os.path.dirname('./Audio/file.wav')):
        try:
            os.makedirs(os.path.dirname('./Audio/file.wav'))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    # f = open('./Audio/file.wav', 'wb')
    print(type(audio_data))
    obj = wave.open(audio_data, 'r')
    audio = wave.open('./Audio/file.wav', 'wb')

    audio.setnchannels(obj.getnchannels())
    audio.setnframes(obj.getnframes())
    audio.setsampwidth(obj.getsampwidth())
    audio.setframerate(obj.getframerate())
    blob = audio_data.read()
    audio.writeframes(blob)

    print("opening file")

    from STT import  assistant
    assistant.takecommand('./Audio/file.wav')
    return HttpResponse('audio received')
