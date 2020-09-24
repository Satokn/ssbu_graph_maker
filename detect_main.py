import cv2, pickle, statistics
from matplotlib import pyplot as plt
import sys

model_filename = 'finalized_model.sav'
loaded_model = pickle.load(open(model_filename, 'rb'))

args = sys.argv
vid = cv2.VideoCapture(args[1])

if not vid.isOpened():
    raise IOError("Couldn't open webcam or video")

from damage_detect import damage_detect, convert_damage

damage, c, i, mode_damage_buffer = 0, 0, 0, 0
damage_list, damage_buffer = [], []

while vid.isOpened():
    ret, frame = vid.read()

    if ret==False:
        break

    pred_list = damage_detect(frame)
    damage = convert_damage(pred_list, damage)
    if damage is not None:
        damage_buffer.append(damage)
    
    c += 1
    if c > vid.get(cv2.CAP_PROP_FPS):
        i += 1
        try:
            mode_damage_buffer = statistics.mode(damage_buffer)
        except:
            pass
        damage_buffer = []
        c = 0
        print(f"{mode_damage_buffer}")
        damage_list.append(mode_damage_buffer)

vid.release()

x = list(range(i))
plt.plot(x, damage_list)
plt.show()
plt.close()
