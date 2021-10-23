from sql import *
import time
banco = ConectarDB()

while True:
    #usuario = ('Cetoprofeno')
    banco.inserir()
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)

    words1 = (banco.consultar_alerta())
    words2 = (banco.consultar_medicamentos())

    c = set(words1).union(set(words2))  # or c = set(list1) | set(list2)
    d = set(words1).intersection(set(words2))  # or d = set(list1) & set(list2)
    a = list(c - d)
    if not a:
        print("Ok")
    else:
        print('Falta o {0}'.format(list(c - d)))
    banco.consultar_alerta()
    banco.remover_registros()
    time.sleep(1)
