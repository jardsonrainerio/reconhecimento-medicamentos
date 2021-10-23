import cv2
import numpy as np
import time
#yolov4-tiny_best.weights
# Load Yolo
net = cv2.dnn.readNet("yolov4-tiny_best.weights", "yolov4-tiny-detector.cfg")
classes = []
with open("data/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading image
cap = cv2.VideoCapture(0)


def check_if_string_in_file(string_to_search):
    """ Check if any line in the file contains given string """
    # Abra o arquivo no modo somente leitura
    with open('myfile.txt', 'r') as read_obj:
        # Leia todas as linhas do arquivo uma por uma
        for line in read_obj:
            # Para cada linha, verifique se a linha contém a string
            if string_to_search in line:
                return True
        return False


font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0
while True:
    _, frame = cap.read()
    frame_id += 1

    height, width, channels = frame.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[3] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 1.8)
                y = int(center_y - h / 1.8)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 2, color, 2)

            if check_if_string_in_file(label):
                pass
            else:
                texto = label
                arquivo = open('myfile.txt', 'a')
                arquivo.write(texto + "\n")
                arquivo.close()

    fileObj = open("Output.txt", "r")  # abre o arquivo em modo de leitura
    words1 = fileObj.read().splitlines()  # coloca o arquivo em um array
    fileObj.close()

    fileObj = open("myfile.txt", "r")  # abre o arquivo em modo de leitura
    words2 = fileObj.read().splitlines()  # coloca o arquivo em um array
    fileObj.close()

    c = set(words1).union(set(words2))  # or c = set(list1) | set(list2)
    d = set(words1).intersection(set(words2))  # or d = set(list1) & set(list2)
    a = list(c - d)
    if not a:
      print("Ok")
    else:
      print('Falta o {0}'.format(list(c - d)))
      cv2.putText(frame, str('Falta o {0}'.format(list(c - d))), (200, 50), font, 2, (0, 255, 0), 3)
            #fileVariable = open('myfile.txt', 'r+')
            #fileVariable.truncate(0)
            #fileVariable.close()

    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time
    cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 2, (0, 0, 0), 3)

    fileVariable = open('myfile.txt', 'r+')
    fileVariable.truncate(0)
    fileVariable.close()
    cv2.imshow("Image", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()