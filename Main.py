import os
import datetime
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Ámbitos que permitirán acceso de edición a los videos de YouTube
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def authenticate_youtube():
    creds = None

    # El archivo 'token.json' almacena el token de acceso de la sesión
    if os.path.exists('token.json'):
        creds, _ = google.auth.load_credentials_from_file('token.json', SCOPES)
    
    # Si no hay credenciales o son inválidas, solicitamos autenticación.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Guardamos las credenciales en 'token.json'
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    return build('youtube', 'v3', credentials=creds)

def update_video_title(youtube, video_id):
    try:
        # Obtenemos la fecha actual
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Obtenemos la información del video actual
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()
        video_snippet = response["items"][0]["snippet"]

        # Actualizamos el título con la fecha
        new_title = f"{video_snippet['title']} - {current_date}"
        video_snippet["title"] = new_title

        # Actualizamos el video con el nuevo título
        update_request = youtube.videos().update(part="snippet", body={
            "id": video_id,
            "snippet": video_snippet
        })
        update_request.execute()

        print(f"Título del video actualizado a: {new_title}")

    except HttpError as e:
        print(f"Ocurrió un error: {e}")
        return None

if __name__ == "__main__":
    # Autenticamos la API de YouTube
    youtube = authenticate_youtube()

    # ID del video que quieres actualizar
    video_id = "VIDEO_ID"

    # Actualizamos el título del video
    update_video_title(youtube, video_id)
