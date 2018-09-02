# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 17:43:07 2018

@author: vanessa
"""
import pandas as pd

dados = pd.read_excel('autores.xlsx')

#FUNCTION THAT ADJUST ET AL
def verificarEtAl(autor):
    if('et' in autor):
        if('al' in autor):
            aux = autor.split('et')[0].rstrip().lstrip()
            if(';' in aux or ',' in aux or '.' in aux):
                return aux[:-1] + ' et al.'
            else:
                return aux + ' et al.'
    else:
        return autor
dados['autor'] = dados['autor'].apply(lambda x: verificarEtAl(x.lower()))

#FUNCTION TO ADJUST LAST NAME
def arrumarSobrenome(autor):
    if(len(autor.split(',')) == 1):
        nome = autor.split(' ')[0:-1]
        sobrenome = autor.split(' ')[-1].upper().rstrip().lstrip()
        return sobrenome + ', ' + ' '.join(nome).lstrip()
    else:
        return autor.split(',')[0].upper().rstrip().lstrip() + ', ' + autor.split(',')[1].rstrip().lstrip()

#FUNCTION TO ADJUST IN THE FORM: LAST NAME, NAME
def arrumarLinha(linha):
    autores = linha.split(';')
    if(len(autores) == 1): #se tem somente 1 autor
        if('et' in linha and 'al' in linha):
            aux = linha.split('et')[0].lstrip().rstrip()
            return arrumarSobrenome(aux) + ' et al.'
        else:
            return arrumarSobrenome(linha)
    elif(len(autores) == 2):
        return arrumarSobrenome(autores[0]) + '; ' + arrumarSobrenome(autores[1])
    elif(len(autores) == 3):
        return arrumarSobrenome(autores[0]) + '; ' + arrumarSobrenome(autores[1]) + '; ' + arrumarSobrenome(autores[2])
dados['autor'] = dados['autor'].apply(lambda x: arrumarLinha(x))

#FUNCTION TO ADJUST UPPER AND LOWER LETTERS IN THE NAME
def arrumaLetra(autor):
    tam = len(autor.split(' '))
    nome = autor.split(' ')
    for i in range(1,tam):
        if(nome[i].lower() == 'de' or nome[i].lower() =='da' or nome[i].lower() == 'da;' or nome[i].lower() == 'dos' or nome[i] == 'et' or nome[i] == 'al.'):
            continue
        else:
            #nome[i] = nome[i][0].upper() + '.'
            nome[i] = nome[i][0].upper() + nome[i][1:]
    return ' '.join(nome) 
dados['autor'] = dados['autor'].apply(lambda x: arrumaLetra(x))

#SAVE IN A EXCEL FILE CALLED OUTPUT
dados.to_excel('output.xlsx', index=False)