import sklearn, cv2
from sklearn.linear_model import LogisticRegression
import numpy as np

def damage_detect(frame):
    from detect_main import loaded_model

    x, y = [131, 146, 159], 245
    h, w = 20, 16
    frame = cv2.resize(frame, (512, 288))
    frame_trim = [frame[y:y+h, i:i+w] for i in x]

    gray = [cv2.cvtColor(i, cv2.COLOR_BGR2GRAY) for i in frame_trim]
    edge = [cv2.Canny(i, 50, 110) for i in gray]
    inv = [cv2.bitwise_not(i) for i in edge]
    cell_nparray = np.array(inv)

    test = cell_nparray.reshape(-1, 320).astype(np.float32)
    pred = loaded_model.predict(test)

    return pred

def convert_damage(pred_list, damage):
    pred_list = list(pred_list)
    for x in pred_list:
        if x.isdigit():
            break
        pred_list.remove("n")

    try:
        damage = int("".join(pred_list))
    except:
        damage = None

    return damage