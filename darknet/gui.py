import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import cv2
import datetime
import time
from sql import *
import numpy as np
from db import Database

db = Database('db.sqlite3')

# Load Yolo
net = cv2.dnn.readNet("yolov4-tiny_best.weights", "yolov4-tiny-detector.cfg")
classes = []
with open("data/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

#width, height = 600, 400
cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

font = cv2.FONT_HERSHEY_SIMPLEX
starting_time = time.time()
frame_id = 0
label = ""
retiraCaracteres = "')(,"
semCaracteres = "')("

root = tk.Tk()
# root window title and dimension
root.title("Sistema Alerta de Medicamentos")
# Set geometry (widthxheight)
root.geometry('900x500')
root.bind('<Escape>', lambda e: root.quit())

msg = Label(root, text = "Sistema Alerta de Medicamentos").place(x = 10, y = 20)

lmain = tk.Label(root)
lmain.pack(side="left")

banco = ConectarDB()

def check_if_string_in_file(string_to_search):
    """ Verifique se alguma linha do arquivo contém a string dada """
    # Abra o arquivo no modo somente leitura
    with open('myfile.txt', 'r') as read_obj:
        # Leia todas as linhas do arquivo uma por uma
        for line in read_obj:
            # Para cada linha, verifique se a linha contém a string
            if string_to_search in line:
                return True
        return False

def show_frame():
    _, frame = cap.read()

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
            if confidence > 0.5:
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

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.7, 0.3)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y - 10), font, 0.5, color, 2)
            if check_if_string_in_file(label):
                pass
            else:
                texto = label
                arquivo = open('myfile.txt', 'a')
                arquivo.write(texto + "\n")
                arquivo.close()


    #frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(5, show_frame)

def esta_na_hora(hora, minuto, hora_atual):
  if hora_atual.hour == hora and hora_atual.minute == minuto:
    return True
  return False

def update_clock():
    now = time.strftime("%H:%M:%S")
    txtHora.configure(text=now)
    root.after(1000, update_clock)


def cadastro():

    def populate_list():
        parts_list.delete(0, END)
        for row in db.fetch():
            parts_list.insert(END, row)
    def add_item():
        if part_text.get() == '' or customer_text.get() == '':
            messagebox.showerror('Campos obrigatórios', 'Por favor, inserir todos os campos')
            return
        db.insert(part_text.get(), customer_text.get())
        parts_list.delete(0, END)
        parts_list.insert(END, (part_text.get(), customer_text.get()))
        clear_text()
        populate_list()

    def select_item(event):
        try:
            global selected_item
            index = parts_list.curselection()[0]
            selected_item = parts_list.get(index)
            # TestLogic('img/'+selected_item[1])
            part_entry.delete(0, END)
            part_entry.insert(END, selected_item[1])
            customer_entry.delete(0, END)
            customer_entry.insert(END, selected_item[2])
        except IndexError:
            pass
    def remove_item():
        db.remove(selected_item[0])
        clear_text()
        populate_list()
    def update_item():
        db.update(selected_item[0], part_text.get(), customer_text.get())
        populate_list()
    def clear_text():
        part_entry.delete(0, END)
        customer_entry.delete(0, END)
    newWindow = tk.Toplevel(root)
    # Part
    part_text = StringVar()
    part_label = Label(newWindow, text='Nome', font=('bold', 14), pady=20)
    part_label.grid(row=0, column=0, sticky=W)
    part_entry = Entry(newWindow, textvariable=part_text)
    part_entry.grid(row=0, column=1)
    # Customer
    customer_text = StringVar()
    customer_label = Label(newWindow, text='Horário', font=('bold', 14))
    customer_label.grid(row=0, column=2, sticky=W)
    customer_entry = Entry(newWindow, textvariable=customer_text)
    customer_entry.grid(row=0, column=3)
    # Parts List (Listbox)
    parts_list = Listbox(newWindow, height=8, width=50, border=0)
    parts_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
    # Create scrollbar
    scrollbar = Scrollbar(newWindow)
    scrollbar.grid(row=3, column=3)
    # Set scroll to listbox
    parts_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=parts_list.yview)
    # Bind select
    parts_list.bind('<<ListboxSelect>>', select_item)

    # Buttons
    add_btn = Button(newWindow, text='Inserir', width=12, command=add_item)
    add_btn.grid(row=2, column=0, pady=20)

    remove_btn = Button(newWindow, text='Excluir', width=12, command=remove_item)
    remove_btn.grid(row=2, column=1)

    update_btn = Button(newWindow, text='Alterar', width=12, command=update_item)
    update_btn.grid(row=2, column=2)

    clear_btn = Button(newWindow, text='Limpar', width=12, command=clear_text)
    clear_btn.grid(row=2, column=3)

    newWindow.title('Cadastro de Medicamentos')
    newWindow.geometry('700x350')

    # Populate data
    populate_list()

def task():
    banco.inserir()
    words1 = (banco.consultar_alerta())
    words2 = (banco.consultar_medicamentos())

    c = set(words1).union(set(words2))  # or c = set(list1) | set(list2)
    d = set(words1).intersection(set(words2))  # or d = set(list1) & set(list2)
    a = list(c - d)
    banco.remover_registros()
    #print(d)
    nomeMedic = ''.join(map(str, c - d))
    for i in retiraCaracteres:
        nomeMedic = nomeMedic.replace(i, '')
    #print(nomeMedic)
    if not a:
        #print("Ok")
        txt1.configure(text="")
        txt2.configure(text="Monitorando")
        txt3.configure(text="")
        load = Image.open("checked.png")
        render = ImageTk.PhotoImage(load)
        img = Label(image=render)
        img.image = render
        img.place(x=710, y=230)
    else:
       #print('Falta o {0}'.format(list(c - d)))
       reduzido = ''.join(map(str, c - d))
       for i in semCaracteres:
           reduzido = reduzido.replace(i, '')
       #print(reduzido[:-1])
       txt1.configure(text="Faltando")
       txt2.configure(text=reduzido[:-1])
       load = Image.open("alarm.png")
       render = ImageTk.PhotoImage(load)
       img = Label(image=render)
       img.image = render
       img.place(x=710, y=230)

    fileVariable = open('myfile.txt', 'r+')
    fileVariable.truncate(0)
    fileVariable.close()
    nowHour = time.strftime("%H:%M")

    hora = (banco.consultar_hora(nowHour))
    if hora:
        for row in hora:
            hora_string = row[2]
            nome = row[1]
            hora = int(hora_string.split(':')[0])
            minuto = int(hora_string.split(':')[1])
            now = datetime.datetime.now()
        if esta_na_hora(hora, minuto, now):
            if (nomeMedic != nome):
                print("ALERTA " + nome )
                txt2.configure(text="Tomar o Medicamento")
                load = Image.open("bell.png")
                render = ImageTk.PhotoImage(load)
                img = Label(image=render)
                img.image = render
                img.place(x=710, y=230)
                txt3.configure(text=nome)

    root.after(2000, task)  # reschedule event in 2 seconds

root.after(2000, task)


monitor = Label(root, text="Monitor de Medicamentos").place(x=670, y=80)

txtHora = Label(root, text="", font=('Helvetica', 28), fg='red')
txtHora.place(x=670, y=10)

txt1 = Label(root, text="", font=('Helvetica', 12))
txt1.place(x=670, y=110)

txt2 = Label(root, text="", font=('Helvetica', 12))
txt2.place(x=670, y=140)

txt3 = Label(root, text="")
txt3.place(x=670, y=300)

exit_button = Button(root, text="Cadastro", command=cadastro)
exit_button.place(x=700, y=400, width=150, height=30)

exit_button = Button(root, text="Sair", command=root.destroy)
exit_button.place(x=700, y=450, width=150, height=30)

update_clock()
show_frame()
root.mainloop()
