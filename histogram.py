import matplotlib.pyplot as plt
import sys
import csv
import time
import pandas as pd
import json

path_tsv = sys.argv[1]
k = sys.argv[2]
k = int(k)

ACS = [
	"Matematica",
	"Probabilidade e estatistica",
	"Ciencia da computacao",
	"Astronomia",
	"Fisica",
	"Quimica",
	"Geociencias",
	"Oceanografia"
]
ACS = [x.upper() for x in ACS]
if path_tsv.split('.')[1] != 'tsv':
    print("O input não é .tsv")
    sys.exit(1)



start = time.time()
try:
    with open(path_tsv) as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        keylist = next(rd)
        keylist.pop(0)
        d = {}
        for i in keylist:
            d[i] = 0
        
        counter = 1
        soma = 0
        print("[+] Processando dados do TSV...")
        for row in rd:
            soma = 0
            for i in range(0, len(row)-1):
                # print(row[i])
                if list(d.keys())[i] in ACS:
                    # print(list(d.keys())[i])
                    d[list(d.keys())[i]] += int(row[i+1])
                

        
except FileNotFoundError:
    print(f"Arquivo {path_tsv} não encontrado.")
    sys.exit(1)



print("[+] Arrumando os dados para o gráfico...")

d = {k: v for k, v in d.items() if v != 0}

valores = list(d.values())

# Converter a lista de valores para inteiros
valores_int = [int(i) for i in valores]

bins = list(range(0, max(valores_int) + int(k), int(k)))  # Cria uma lista de bins de 0 até o máximo de seus dados, de k em k
labels = [f'{i}-{i+int(k)-1}' for i in bins[:-1]]  # Cria rótulos para cada bin

# Usar pd.cut para dividir seus dados em bins e contar a frequência de cada bin
valores_series = pd.Series(valores_int)  # Transforma a lista em uma Series do pandas
valores_bins = pd.cut(valores_series, bins=bins, labels=labels, include_lowest=True)
freq_counts = valores_bins.value_counts().sort_index()

data = freq_counts.to_dict()

data = {k: v for k, v in data.items() if v != 0}

keys = list(data.keys())
values = list(data.values())

print("[+] Gerando o gráfico...")

print(data)

plt.figure(figsize=(11,7))
plt.grid(zorder=0)
plt.bar(keys, values, color=['#00A599', '#F35529'], zorder=3)
plt.xlabel('Total de Bancas')
plt.ylabel('Quant. de Áreas')
plt.title('Histograma')
plt.show()