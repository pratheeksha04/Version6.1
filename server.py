from waitress import serve

from app import server

serve(server,port=8050)