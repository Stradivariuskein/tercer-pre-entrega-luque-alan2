import requests

# Definir la lista de rutas a probar
routes = [
    '/getTurn/',
    '/turnCreate/',
    '/turnos/',
    '/perfil/',
    '/typeSession/',
    '/cuentas/',
]

# URL base de tu aplicación
base_url = 'http://localhost:8000'  # Cambia esto a la URL correcta

# Iterar sobre las rutas y hacer solicitudes HTTP sin redirecciones
for route in routes:
    url = base_url + route
    response = requests.get(url, allow_redirects=False)  # Deshabilitar redirecciones
    status_code = response.status_code
    print(f'{url} - Status Code: {status_code}')
