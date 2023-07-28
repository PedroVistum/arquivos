import matplotlib.pyplot as plt
import sys
import csv
import random
import time
import pandas as pd

path_tsv = sys.argv[1]

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
        for row in rd:
            soma = 0
            for i in range(0, len(row)-1):
                # print(row[i])
                d[list(d.keys())[i]] += int(row[i+1])

        
except FileNotFoundError:
    print(f"Arquivo {path_tsv} não encontrado.")
    sys.exit(1)

valores = list(d.values())

# Converter a lista de valores para inteiros
valores_int = [int(i) for i in valores]

bins = list(range(0, max(valores_int) + 500, 500))  # Cria uma lista de bins de 0 até o máximo de seus dados, de 1000 em 1000
labels = [f'{i}-{i+499}' for i in bins[:-1]]  # Cria rótulos para cada bin

# Usar pd.cut para dividir seus dados em bins e contar a frequência de cada bin
valores_series = pd.Series(valores_int)  # Transforma a lista em uma Series do pandas
valores_bins = pd.cut(valores_series, bins=bins, labels=labels, include_lowest=True)
freq_counts = valores_bins.value_counts().sort_index()

data = freq_counts.to_dict()
a = {list(d.keys())[0]: list(d.values())[0]}
data = a | data
data = {k: v for k, v in data.items() if v != 0}

keys = list(data.keys())
values = list(data.values())

plt.figure(figsize=(11,7))
plt.bar(keys, values, color=['#00A599', '#F35529'])
plt.xlabel('Total de Bancas')
plt.ylabel('Quant. de Áreas')
plt.title('Histograma')
plt.show()