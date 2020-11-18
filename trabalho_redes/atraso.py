#import sys, webbrowser, requests, bs4
#import os
#import subprocess
import sys

lista = [0,0,0,0,0,0,0,0,0];

def main():
        file_name = str(sys.argv[1]);
        file = open(file_name, 'r');
        lines = file.readlines();
        size = len(lines);
        x = range(2, size - 8);
        for i in x:
                temp = lines[i].split();
                if "limite" in temp:
                        continue;
                else:
                        temp = temp[4].split("=");
                        temp = temp[1].split("ms");
                        temp = int(temp[0]);

                        if temp < 10:
                                lista[0] = lista[0] + 1;

                        elif temp < 20 and temp > 10:
                                lista[1] = lista[1] + 1;

                        elif temp < 30 and temp > 20:
                                lista[2] = lista[2] + 1;

                        elif temp < 40 and temp > 30:
                                lista[3] = lista[3] + 1;

                        elif temp < 50 and temp > 60:
                                lista[4] = lista[4] + 1;

                        elif temp < 60 and temp > 70:
                                lista[5] = lista[5] + 1;

                        elif temp < 70 and temp > 80:
                                lista[6] = lista[6] + 1;

                        elif temp < 80 and temp > 90:
                                lista[7] = lista[7] + 1;

                        else:
                                lista[8] = lista[8] + 1;

        print(lista);

if __name__ == '__main__':
    main()

