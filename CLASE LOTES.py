import csv
import json
from datetime import datetime

class Lote:
    def __init__(self, clave: str, nombre: str, caducidad: datetime, unidades: int):
        self.clave = clave
        self.nombre = nombre
        self.caducidad = caducidad
        self.unidades = unidades

    def validar_clave(self):
        if len(self.clave) != 7:
            return False
        if not (self.clave[:3].isalpha() and self.clave[:3].isupper()):
            return False
        if self.clave[3] != '-':
            return False
        if not (self.clave[4:].isnumeric()):
            return False
        return True

    def validar_nombre(self):
        if len(self.nombre) < 5 or len(self.nombre) > 30:
            return False
        if all(c.isspace() for c in self.nombre):
            return False
        return True

    def validar_caducidad(self):
        if not isinstance(self.caducidad, datetime):
            return False
        return True

    def validar_unidades(self):
        if not isinstance(self.unidades, int):
            return False
        if self.unidades < 100 or self.unidades > 1000:
            return False
        return True

    def es_valido(self):
        return all([self.validar_clave(), self.validar_nombre(), self.validar_caducidad(), self.validar_unidades()])

def guardar_lotes_csv(lotes, archivo):
    with open(archivo, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Clave', 'Nombre', 'Caducidad', 'Unidades'])
        for lote in lotes:
            writer.writerow([lote.clave, lote.nombre, lote.caducidad.strftime('%Y-%m-%d'), lote.unidades])

def guardar_lotes_json(lotes, archivo):
    with open(archivo, 'w') as f:
        lotes_dict = [vars(lote) for lote in lotes]
        for lote_dict in lotes_dict:
            lote_dict['caducidad'] = lote_dict['caducidad'].strftime('%Y-%m-%d')
        json.dump(lotes_dict, f)

def main():
    lotes = []
    while True:
        clave = input('Ingresa la clave del lote o "X" para salir: ')
        if clave == 'X':
            break
        if any(lote.clave == clave for lote in lotes):
            print('Esa clave ya está registrada.')
            continue
        nombre = input('Ingresa el nombre del lote: ')
        caducidad_str = input('Ingresa la fecha de caducidad (YYYY-MM-DD): ')
        try:
            caducidad = datetime.strptime(caducidad_str, '%Y-%m-%d')
        except ValueError:
            print('Fecha inválida.')
            continue
        unidades_str = input('Ingresa la cantidad de unidades: ')
        try:
            unidades = int(unidades_str)
        except ValueError:
            print('Unidades inválidas.')
            continue
        lote = Lote(clave, nombre, caducidad, unidades)
        if not lote.es_valido():
            print('Datos inválidos.')
            continue
        lotes.append(lote)
    for lote in lotes:
        print(f'Clave: {lote.clave}, Nombre: {lote.nombre}, Caducidad: {lote.caducidad.strftime("%Y-%m-%d")}, Unidades: {lote.unidades}')
    guardar_lotes_csv(lotes, 'lotes.csv')
    guardar_lotes_json(lotes, 'lotes.json')

if __name__ == '__main__':
    main()