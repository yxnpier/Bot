from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterEmpty
from telethon.errors import SessionPasswordNeededError
from datetime import datetime, timedelta
from time import sleep
from telethon.tl import types
from telethon.errors import FloodWaitError
from telethon.errors import FloodWaitError, ChatAdminRequiredError
api_id = '29348999'
api_hash = '4db5414664d8ff25568166cfc014a56c'


grupo_origen_id = -4172484199 #<----AQUI EL GRUPO  DE ORIGEN 

tu_numero_telefono = '+51998229537'

def iniciar_sesion():
    client = TelegramClient('session_name', api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        try:
            client.send_code_request(tu_numero_telefono)
            client.sign_in(tu_numero_telefono, input('Ingresa el código que has recibido: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Ingresa la contraseña de la cuenta: '))
    return client

def reenviar_mensajes(client):
    errores_impresos = set()  # Conjunto para almacenar errores ya impresos

    try:
        print("Obteniendo mensajes...")
        messages = client.iter_messages(grupo_origen_id)
        total_mensajes = 0

        chats = client.get_dialogs()
        for chat in chats:
            if chat.is_group and chat.id != grupo_origen_id:
                for message in messages:
                    if isinstance(message, types.MessageService):
                        continue
                    try:
                        client.forward_messages(chat.id, messages=message)
                        total_mensajes += 1
                    except Exception as e:
                        error_str = str(e)
                        if error_str not in errores_impresos:
                            print(f"Error al reenviar mensajes al grupo {chat.title}: {error_str}")
                            errores_impresos.add(error_str)

                print(f"mensaje reenviado al grupo {chat.title}: {total_mensajes}")
                total_mensajes = 0  # Reiniciar el contador para el próximo grupo

    except Exception as ex:
        print(f"Error general: {ex}")

if __name__ == "__main__":
    client = iniciar_sesion()
    
    while True:
        try:
            reenviar_mensajes(client)
            print("Esperar 10 minutos para reenviar mensajes nuevamente.")
            sleep(600)  # Esperar 15 minutos (900 segundos) antes de volver a reenviar mensajes
        except Exception as ex:
            print(f"Error general: {ex}")