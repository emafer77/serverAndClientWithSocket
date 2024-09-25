import socket
import threading
import sys
import os
import pickle

class Servidor():

    def __init__(self, host="localhost", port=7000):
        self.clientes = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)

        # Hilos para aceptar y procesar las conexiones
        aceptar = threading.Thread(target=self.aceptarCon)
        procesar = threading.Thread(target=self.procesarCon)

        aceptar.daemon = True
        aceptar.start()

        procesar.daemon = True
        procesar.start()

        try:
            while True:
                msg = input('-> ')
                if msg == 'salir':
                    break
                self.sock.close()
                sys.exit()
        except:
            self.sock.close()
            sys.exit()

    def msg_to_all(self, msg, cliente):
        for c in self.clientes:
            try:
                if c != cliente:
                    c.send(msg)
            except:
                self.clientes.remove(c)

    def aceptarCon(self):
        print("Aceptando conexiones...")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clientes.append(conn)
            except:
                pass

    def procesarCon(self):
        print("Procesando conexiones...")
        while True:
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c.recv(1024)
                        if data:
                            self.procesar_comando(data, c)
                    except:
                        pass

    def procesar_comando(self, data, cliente):
        comando = pickle.loads(data).strip()

        if comando == "lsFiles":
            self.listar_archivos(cliente)
        elif comando.startswith("get "):
            archivo = comando[4:].strip()
            self.enviar_archivo(archivo, cliente)

    def listar_archivos(self, cliente):
        carpeta = os.path.join(os.getcwd(), "Files")
        if os.path.exists(carpeta):
            archivos = os.listdir(carpeta)
            mensaje = "\n".join(archivos)
        else:
            mensaje = "Carpeta 'Files' no encontrada."
        cliente.send(pickle.dumps(mensaje))

    def enviar_archivo(self, archivo, cliente):
        ruta_archivo = os.path.join(os.getcwd(), "Files", archivo)
        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, 'rb') as f:
                contenido = f.read()
            cliente.send(pickle.dumps(f"ENVIANDO ARCHIVO {archivo}"))
            cliente.send(pickle.dumps(contenido))
        else:
            cliente.send(pickle.dumps(f"Archivo {archivo} no encontrado."))

server = Servidor()
