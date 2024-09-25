import socket
import threading
import sys
import pickle
import os

class Cliente():
    def __init__(self, host="localhost", port=7000):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((str(host), int(port)))

            msg_recv = threading.Thread(target=self.msg_recv)
            msg_recv.daemon = True
            msg_recv.start()

            while True:
               
                msg = input('cliente> ')
                if msg != 'salir':
                    if msg.startswith('get '):
                        archivo = msg.split(' ')[1]
                        self.enviar_comando(msg)
                    else:
                        self.enviar_comando(msg)
                else:
                    self.sock.close()
                    sys.exit()
        except:
            print("Error al conectar el socket")

    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(1028)
                if data:
                    data = pickle.loads(data)

                    if isinstance(data, bytes):
                        archivo = input("Ingrese el nombre para guardar el archivo: ")
                        self.guardar_archivo(archivo, data)
                    else:
                        print(data)
            except:
                pass

    def enviar_comando(self, msg):
        try:
            self.sock.send(pickle.dumps(msg))
        except:
            print("Error al enviar el mensaje")

    def guardar_archivo(self, archivo, contenido):
        # Crear carpeta 'download' si no existe
        carpeta = os.path.join(os.getcwd(), "download")
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Guardar el archivo en la carpeta 'download'
        ruta_archivo = os.path.join(carpeta, archivo)
        with open(ruta_archivo, 'wb') as f:
            f.write(contenido)
        print(f"Archivo guardado como {ruta_archivo}")

cliente = Cliente()