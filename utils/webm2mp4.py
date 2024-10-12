from converter import Converter
conv = Converter()
info = conv.probe('/home/loki/Videos/Screencasts/dataset_location.webm')

convert = conv.convert('/home/loki/Videos/Screencasts/dataset_location.webm', '/home/loki/Videos/Screencasts/dataset_location.mp4', {
    'format': 'mp4',
    'audio': {
        'codec': 'aac',
        'samplerate': 11025,
        'channels': 2
    },
    'video': {
        'codec': 'hevc',
        'width': 1436,
        'height': 1291,
        'fps': 25
    }})

for timecode in convert:
    print(f'\rConverting ({timecode:.2f}) ...')