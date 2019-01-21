
import wave
from pyaudio import *
import os

# 定义数据流块
CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

filePath = '%s/smart/app/static/audio/%s' % (os.path.abspath('..'), sys.argv[1])
p = PyAudio()
with wave.open(filePath, 'rb') as f:
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()), channels=f.getnchannels(), rate=f.getframerate(), output=True)
    data = f.readframes(CHUNK)
    while data != b'':
        stream.write(data)
        data = f.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()



