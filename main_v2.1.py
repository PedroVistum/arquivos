#!/usr/bin/env python3

import csv
import time
import sys


path_tsv = sys.argv[1]

if path_tsv.split('.')[1] != 'tsv':
    print("O input não é .tsv")
    sys.exit(1)

output_name = sys.argv[2]

if output_name.split('.')[1] != 'tsv':
    print("O output não é .tsv")
    sys.exit(1)
    
start = time.time()

# Check if file exists
try:
    with open(path_tsv) as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        keyList = next(rd)
        d = {}
        for i in keyList:
            d[i] = 0
        arrFinal = []
        for row in rd:
            if rd.line_num == 1:
                continue
            dictionary_of_ACindexEValor = {'nome': row[0]}
            for i in range(1, len(row)):
                try:
                    row[i] = int(row[i])
                except ValueError:
                    print(f"Valor não inteiro {row[i]} não pode ser convertido em numero. Pulando o valor.")
                    continue
            counter = 0
            zeroes = 0
            for i in row:
                if counter == 0:
                    pass
                # if type(row[counter]) != int:
                #     continue
                elif i >= 1:
                    dictionary_of_ACindexEValor[keyList[counter]] = i
                elif i == 0:
                    zeroes += 1
                
                counter += 1
                
            if zeroes != (len(row)-1):
                arrFinal.append(dictionary_of_ACindexEValor)
            elif zeroes == (len(row)-1):
                arrFinal.append({'nome': f'{row[0]}', 'nada': 1})
except FileNotFoundError:
    print(f"Arquivo {path_tsv} não encontrado.")
    sys.exit(1)

arrFinalFinal = []
for membro in arrFinal:
    nome = membro['nome']
    max_keys = []
    max_values = []
    membrofinal = {'nome': nome, }
    for key, value in membro.items():
        if isinstance(value, int):
            if not max_values or value > max_values[0]:
                max_values = [value]
                max_keys = [key]
            elif value == max_values[0] and len(max_values) < 3:
                max_values.append(value)
                max_keys.append(key)
        else:
            try:
                int_value = int(value)
                if not max_values or int_value > max_values[0]:
                    max_values = [int_value]
                    max_keys = [key]
                elif int_value == max_values[0] and len(max_values) < 3:
                    max_values.append(int_value)
                    max_keys.append(key)
            except ValueError:
                pass

    if max_keys:
        if max_keys[0] == 'nada':
            membrofinal['AC1'] = ''
            membrofinal['AC2'] = ''
            membrofinal['AC3'] = ''
        else:
            for i in range(len(max_keys)):
                membrofinal[f'AC{i+1}'] = f'{max_keys[i]}, {max_values[i]}'
                if len(membrofinal) == 2 or len(membrofinal) == 3:
                    membrofinal['AC2'] = ''
                    membrofinal['AC3'] = ''

    if len(membrofinal) == 1:
        membrofinal['AC1'] = ''
        membrofinal['AC1'] = ''
        membrofinal['AC1'] = ''

    arrFinalFinal.append(membrofinal)



try:
    field_names = arrFinalFinal[0].keys()
    with open(output_name, "w", newline="") as tsv_file:
        writer = csv.DictWriter(tsv_file, delimiter="\t", fieldnames=field_names)
        writer.writeheader()
        writer.writerows(arrFinalFinal)
    print(f"O codigo rodou em {round(time.time() - start, 2)} segundos")
except PermissionError:
    print(f"Permissão negada para criar o arquivo {output_name}.")
    sys.exit(1)
