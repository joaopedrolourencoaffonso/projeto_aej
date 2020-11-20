import math
import matplotlib.pyplot as plt
import sys

arquivo = str(sys.argv[1]);
media = 14;
lista = [];

print("           nome             | variancia | desvio_padrao");

somatorio = 0;
medidas = 0;

file = open(arquivo, 'r');
lines = file.readlines();
size = len(lines);
x = range(2, size - 6);

for i in x:
        temp = lines[i].split();
        if "limite" in temp:
                continue;
        else:
                medidas = medidas + 1;
                temp = temp[4].split("=");
                temp = temp[1].split("ms");
                temp = int(temp[0]);
                somatorio = somatorio + (temp - media)*(temp - media);
                lista.append(temp);
                #print(str(temp) + " " + str(medidas) + " " + str(temp - media_total)*());

variancia = somatorio / medidas;
variancia = round(variancia, 2);
desvio_padrao = math.sqrt(variancia);
desvio_padrao = round(desvio_padrao, 2);

print( arquivo + ": " + str(variancia) + " | " + str(desvio_padrao));

plt.title('Idades de um grupo', fontsize=20)
plt.xlabel('Idade', fontsize=15)
plt.ylabel('Intervalos \n', fontsize=15)
plt.tick_params(labelsize=15)
plt.hist(lista, 5, rwidth=0.9);
plt.show();
        

                        





