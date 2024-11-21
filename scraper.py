
import requests
from bs4 import BeautifulSoup
import csv
import pprint

# Solicitar búsqueda y criterio de ordenamiento
string = input('¿Qué quieres buscar? ')
order_by = input('¿Cómo quieres ordenar los productos? (titulo/precio): ').lower()

# Obtener contenido de la página
r = requests.get(f'https://listado.mercadolibre.com.co/{string.replace(" ", "-")}#D[A:{string}]')
contenido = r.content

# Procesar HTML con BeautifulSoup
soup = BeautifulSoup(contenido, 'html.parser')
alldivs = soup.find_all('div', {'class': 'poly-card'})

# Array para añadir objetos
products_array = []

for item in alldivs:
    product = {}
    title = item.find('h2', {'class': 'poly-box'})
    price = item.find('span', {'class': 'andes-money-amount--cents-superscript'})
    description = item.find('p', {'class': 'poly-description'})
    link = item.find('h2', {'class': 'poly-box'}).find('a')

    # Verificar si los elementos existen antes de acceder a sus atributos
    product['title'] = title.text if title else 'Sin título'
    product['price'] = float(price.text.replace('$', '').replace('.', '').replace(',', '.')) if price else 0.0
    product['description'] = description.text if description else 'Sin descripción'
    product['link'] = link['href'] if link else 'Sin enlace'

    products_array.append(product)

# Ordenar el array según el criterio seleccionado
if order_by == 'titulo':
    products_array.sort(key=lambda x: x['title'])
elif order_by == 'precio':
    products_array.sort(key=lambda x: x['price'])

# Mostrar resultados en consola
pprint.pprint(products_array, width=50)

# Guardar en archivo CSV
filename = f"{string.replace(' ', '_')}_productos.csv"
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'price', 'description', 'link'])
    writer.writeheader()
    for product in products_array:
        writer.writerow(product)

print(f"Los resultados se han guardado en {filename}")
    