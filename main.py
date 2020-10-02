import cv2, pickle, statistics, sys
from matplotlib import pyplot as plt
import datetime as dt

#load train model
model_filename = 'finalized_model.sav'
loaded_model = pickle.load(open(model_filename, 'rb'))

args = sys.argv
vid = cv2.VideoCapture(args[1])

if not vid.isOpened():
    raise IOError("Couldn't open webcam or video")

vid_frame = vid.get(cv2.CAP_PROP_FRAME_COUNT)
vid_fps = vid.get(cv2.CAP_PROP_FPS)
vid_sec = vid_frame / vid_fps

#detect damage
from damage_detect import damage_detect, convert_damage, chk_proper_damage

p1_damage, p2_damage, c, i, p1_mode_damage_buffer, p2_mode_damage_buffer, p1_prev_damage, p2_prev_damage = 0, 0, 0, 0, 0, 0, 0, 0
p1_damage_list, p1_damage_buffer, p2_damage_list, p2_damage_buffer = [], [], [], []

while vid.isOpened():
    ret, frame = vid.read()

    if ret==False:
        break

    #detect damage every frame
    pred_list = damage_detect(frame)
    p1_damage = convert_damage(pred_list[:3], p1_damage)
    p2_damage = convert_damage(pred_list[3:], p2_damage)
    if p1_damage is not None:
        p1_damage_buffer.append(p1_damage)
    if p2_damage is not None:
        p2_damage_buffer.append(p2_damage)
    
    #append damage every second
    c += 1
    if c > vid.get(cv2.CAP_PROP_FPS):
        i += 1
        c = 0

        try:
            p1_mode_damage_buffer = statistics.mode(p1_damage_buffer)
        except:
            pass

        try:
            p2_mode_damage_buffer = statistics.mode(p2_damage_buffer)
        except:
            pass

        p1_damage_buffer, p2_damage_buffer = [], []
        p1_mode_damage_buffer = chk_proper_damage(p1_mode_damage_buffer, p1_prev_damage)
        p2_mode_damage_buffer = chk_proper_damage(p2_mode_damage_buffer, p2_prev_damage)
        p1_prev_damage = p1_mode_damage_buffer
        p2_prev_damage = p2_mode_damage_buffer
        p1_damage_list.append(p1_mode_damage_buffer)
        p2_damage_list.append(p2_mode_damage_buffer)

    #print progress
    prog_value = vid.get(cv2.CAP_PROP_POS_FRAMES)/vid.get(cv2.CAP_PROP_FRAME_COUNT)*100
    prog_bar = "".join(["=" for x in range(int(prog_value//5))] + [" " for x in range(int(20-prog_value//5))])
    print("\r" + f"{prog_value:.1f}% |{prog_bar}|", end="")

#convert xlabel to MM:SS
x = [f"{t//60:02}:{t%60:02}" for t in range(i)]

#show figure
ticks = 30
plt.xticks(range(0, len(x), ticks), x[::ticks])
plt.xlabel("time")
plt.ylabel("damage")
plt.plot(x, p1_damage_list)
plt.plot(x, p2_damage_list)
plt.show()

#exit
vid.release()
sys.exit()