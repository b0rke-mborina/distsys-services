import json
from htsql import HTSQL
from db_conf import DB_URL

htsql = HTSQL(DB_URL)

rows = htsql.produce("/helpdesk_ticket{ tipo.tipo, categoria.nombre, estado.estado, fecha_creacion}")


class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
        return value

partitions = AutoVivification()

aguas = {} 
for row in rows:
    if not row.nombre:
        nombre = 'sin categorizar'
    else:
        nombre = row.nombre

    if not row.tipo:
        tipo = 'default'
    else:
        tipo = row.tipo

    if not row.estado:
        estado = 'indefinido'
    else:
        estado = row.estado

    if row.fecha_creacion:
        try:
            aguas[tipo, nombre, estado, row.fecha_creacion.year, row.fecha_creacion.month] += 1
        except KeyError:
            aguas[tipo, nombre, estado, row.fecha_creacion.year, row.fecha_creacion.month] = 1


for row in rows:
    if not row.nombre:
        nombre = 'sin categorizar'
    else:
        nombre = row.nombre

    if not row.tipo:
        tipo = 'default'
    else:
        tipo = row.tipo

    if not row.estado:
        estado = 'indefinido'
    else:
        estado = row.estado

    if row.fecha_creacion:
        partitions[tipo][nombre][estado][row.fecha_creacion.year][row.fecha_creacion.month] = \
                  aguas[tipo, nombre, estado, row.fecha_creacion.year, row.fecha_creacion.month]



tipos = []
for tipo in partitions:
    children = []
    for nombre in partitions[tipo]:
        subchildren = []
        for estado in partitions[tipo][nombre]:
            subsubchildren = []
            for year in partitions[tipo][nombre][estado]:
                subsubsubchildren = []
                for month in partitions[tipo][nombre][estado][year]:
                    subsubsubchildren.append( {'name': month,
                                               'size': partitions[tipo][nombre][estado][year][month] } )
                subsubchildren.append( {'name': year,
                                        'children': subsubsubchildren } )
            subchildren.append( {'name': estado,
                                 'children': subsubchildren } )
        children.append( {'name': nombre,
                          'children': subchildren } )
    tipos.append( {'name': tipo,
                   'children': children } )


tickets = {'name': 'tickets',
           'children': tipos }



with open('static/tg_sunburst.json', 'w') as f:
    f.write(json.dumps(tickets, indent=4))

