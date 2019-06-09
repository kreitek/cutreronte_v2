from django.conf import settings
from cutreronte.models import Dispositivo


import json
import redis
import serial
import time

SERIE_PUERTO = "/dev/ttyUSB0"
SERIE_BAUDRATE = 115200

SENAL_ENTRADA = 20
TIMEOUT_SENAL = 15

class SITUACION:
    DENTRO = 1
    FUERA = 0



class Sniffer:
    def __init__(self):
        self.macs_conocidas = []
        self.redis_db = redis.StrictRedis(host="localhost", port=6379, db=12)
        self.conectado = False

    def run(self):
        while True:
            try:
                if not self.conectado:
                    self._conectar_serie()
                self._recibir_serie()
            except (serial.serialutil.SerialException, OSError):
                self.conectado = False
            except (KeyboardInterrupt, SystemExit):
                self.ser.close()
                break
            time.sleep(0.1)

    def _recibir_serie(self):
        while self.ser.inWaiting() > 0:
            response = self.ser.read_until()  # terminator=LF, size=None Read until a termination sequence is found ('\n' by default), the sizeis exceeded or until timeout occurs.
            response = response.decode('utf-8').strip()
            if response.startswith("CLIENT,"):
                print(response)
                partes = response.split(",")
                mac = partes[1]
                beacon = partes[2]
                canal = int(partes[3])
                senal = -int(partes[4])
                # dispositivo_detectado(mac, senal, canal, beacon)

    def _conectar_serie(self):
        try:
            self.ser.close()
        except:
            pass
        while not self.conectado:
            try:
                self.ser = serial.Serial(SERIE_PUERTO, SERIE_BAUDRATE, timeout=0.5)
                self.conectado = True
            except:
                print("ERROR no se pudo abrir el puerto {}. Reintentando...".format(SERIE_PUERTO))
                time.sleep(10)


#
#
# def reiniciar_senal(redis_db):
#     for mac in redis_db.keys():
#         pl = json.loads(redis_db.get(mac).decode('utf-8'))
#         senal = pl[0]
#         canal = pl[1]
#         tiempo = pl[2]
#         situacion = pl[3]
#         beacon = pl[4]
#         ahora = time.time()
#         if situacion == SITUACION.DENTRO and ahora - tiempo > TIMEOUT_SENAL:
#             redis_db.set(mac, json.dumps([0, canal, ahora, SITUACION.FUERA, beacon]))
#             print("Dispositivo desconectado {}, canal {}, señal {}".format(mac.decode('utf-8'), canal, senal))
#             mac_str = mac.decode('utf-8')
#             for mac_conocida, nombre in macs_conocidas:
#                 if mac_str.startswith(mac_conocida):
#                     print("CONOCIDO HA SALIDO {} ({}), canal {}, señal {}, beacon {}".format(nombre, mac_str, canal, senal, beacon))
#                     break
#
#
# def print_estadisticas(redis_db):
#     n_total = 0
#     n_dentro = 0
#     for mac in redis_db.keys():
#         n_total +=1
#         pl = json.loads(redis_db.get(mac).decode('utf-8'))
#         senal = pl[0]
#         canal = pl[1]
#         tiempo = pl[2]
#         situacion = pl[3]
#         beacon = pl[4]
#
#         if situacion == SITUACION.DENTRO:
#             n_dentro +=1
#     print("{} dispositivos en total. {} dentro.".format(n_total, n_dentro))
#
#
#
# def print_redis(redis_db, corte=0):
#     n_dispositivos = 0
#     for key in redis_db.keys():
#         try:
#             pl = json.loads(redis_db.get(key).decode('utf-8'))
#             mac = key.decode('utf-8')
#             senal = pl[0]
#             canal = pl[1]
#             tiempo = pl[2]
#             situacion = pl[3]
#             beacon = pl[4]
#             if senal > corte:
#                 print("{} {} {} {}".format(mac, senal, canal, tiempo))
#                 n_dispositivos += 1
#         except:
#             redis_db.delete(key)
#     print("numero de dispositivos: {}".format(n_dispositivos))
#
#
# def leer_todo_lo_que_viene(ser):
#     try:
#         while True:
#             if ser.inWaiting() > 0:
#
#                 response = ser.read_until()  # terminator=LF, size=None Read until a termination sequence is found ('\n' by default), the sizeis exceeded or until timeout occurs.
#                 response = response.decode('utf-8').strip()
#                 print(response)
#     except (KeyboardInterrupt, SystemExit):
#         ser.close()
#
#
# def dispositivo_detectado(mac, senal, canal, beacon):
#     dispositivo = redis_db.get(mac)
#     situacion = SITUACION.FUERA
#     if dispositivo is None:
#         # print("Nuevo dispositivo {}, canal {}, señal {}".format(mac, canal, senal))
#         if senal >= SENAL_ENTRADA:
#             # print("{} ha entrado".format(mac))
#             situacion = SITUACION.DENTRO
#     else:
#         pl = json.loads(dispositivo.decode('utf-8'))
#         anterior_senal = pl[0]
#         anterior_canal = pl[1]
#         anterior_tiempo = pl[2]
#         situacion = pl[3]
#
#         if situacion == SITUACION.FUERA and senal >= SENAL_ENTRADA:
#             situacion = SITUACION.DENTRO
#             # print("Dispositivo reconectado {}, canal {}, señal {}".format(mac, canal, senal))
#     tiempo = int(time.time())
#     redis_db.set(mac, json.dumps([senal, canal, tiempo, situacion, beacon]))
#     for mac_conocida, nombre in macs_conocidas:
#         if mac.startswith(mac_conocida):
#             print("CONOCIDO {} ({}), canal {}, señal {}, beacon {}".format(nombre, mac, canal, senal, beacon))
#             break





if __name__ == '__main__':
    # leer_todo_lo_que_viene(ser)
    pass