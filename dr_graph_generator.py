wimport networkx as nx
import matplotlib.pyplot as plt
import os

if __name__ == "__main__":
    #Path de lectura de archivos generados con traceroute.py
    path = './All'

    #lista todos los archivos dentro de la carpeta definida en path
    files = os.listdir(path)

    #diccionario que guarda los edges y sus frecuencias/pesos de los caminos mas comunes.
    edge_dict = {}

    #Grafo dirigido que tendra todas las rutas que siguieron los paquetes.
    G = nx.DiGraph()

    #contado de ips filtradas
    filtered_counter = 0

    #forloop usado para leer todos los archivos listados en el path.
    for file_name in files:

        file_name_pieces = file_name.split('.')
        fd =  open(path+'/'+file_name, 'r')
        file = fd.read()
        file_split = file.split('\n')
        len_file_split = len(file_split)

        destination = ''
        prev = ''

        #ips que vamos a filtrar de los tres primeros registros de cada archivo que vamos a analizar.
        filter_ip = ['192.168.100.1', '192.168.10.1', '192.168.1.1',
                     '10.0.2.2', '192.168.0.1','172.21.140.1','192.168.4.1',
                     '192.168.0.254', '192.168.10.1', '192.168.1.10']

        #ip de destino que se encuentra en la primera linea del archivo generado por traceroute.py
        destination = file_split[0].rstrip('\r')

        #forloop para iterar todas las entradas del archivo generado por traceroute.py desde el primer registro del tipo 1\tIP.
        for i in range(1, len_file_split-1):
            split_line = file_split[i].split('\t')
            curr = split_line[1]
            curr = curr.rstrip('\r')

            #filtrado de cualquier current ip que no sea una ip valida.
            if curr != '*':

                #filtrado de aquellas ips en filter_ip que esten en las primeras tres lineas del archivo.
                if (i == 1 or i == 2 or i == 3) and (curr in filter_ip):
                    filtered_counter = filtered_counter + 1
                else:
                    #agrega los edges al diccionario que llevan al destino
                    if curr == destination and prev != '':
                        edge = (prev, destination.rstrip('\r') + '/' + file_name_pieces[1])
                        if edge in edge_dict:
                            edge_dict[edge] = edge_dict[edge] + 1
                        else:
                            edge_dict[edge] = 1
                    else:
                        #agrega los edges de aquellos edges que no llevan a destino
                        #en el if / positivo -> agrega toda ip seguida de otra ip en el camino del traceroute.
                        if prev != '':
                            edge = (prev, curr)
                            if edge in edge_dict:
                                edge_dict[edge] = edge_dict[edge] + 1
                            else:
                                edge_dict[edge] = 1
                        else:
                            #agrega el nodo especial que vamos a llamar 127.0.0.1 desde el cual vamos a buscar el camino mas corto.
                            if curr != destination and prev == '':
                                edge = ('127.0.0.1', curr)
                                if not edge in edge_dict:
                                    edge_dict[edge] = 0
                        prev = curr

    #Se agregan todos los edges y nodos al grafo
    for key, value in edge_dict.items():
        if value == 0:
            G.add_edge(key[0], key[1], weight=0)
        else:
            G.add_edge(key[0], key[1], weight=(1.0/float(value)))

    #se imprime el total de nodos del grafo.
    print("Nodes of graph: ")
    print(len(G.nodes()))
    #se imprime el total de edges del grafo.
    print("Edges of graph: ")
    print(len(G.edges()))
    #se imprime el total de nodos filtrados.
    print ("Filtered IPs: " + str(filtered_counter))
    #se imprimen todos los nodos que estan conectados al nodo especial 127.0.0.1
    print (G['127.0.0.1'])

    #se dibuja el grafo.
    nx.draw(G, with_labels=True)
    #nx.draw_circular(G, with_labels=True)
    plt.show()
