import json
def converte_CSV_into_JSON(arquivoCSV, arquivoJSON):

    
    nrLinha = 0
    coluna_numero = {}
    colunasEsperadas = "Numero_de_inscricao","Grupo_Categoria","Categoria","Nome_Completo","Data_de_nascimento","E_mail","Tipo_de_Documento","Documento","Sexo","CAMISETA","CAMISETA_KIDS"
    #colunasEsperadas = "Cod_Inscr","Cod_Prova","Num_Atleta","Nome_Completo","Sexo","Dt_Nasc","CPF","Tel_Contato","Celular","Equipe","Camiseta"
    #colunasEsperadas = "id_seq","Modalidade","Categoria","ID_Usuario","Nome_Completo","Sexo","Email","Data_Nascto","Num_Documento","Camiseta","Equipe"
    codInscrList = []
    numAtletaList = []

    file_json = open(arquivoJSON, 'w')
    file_json.write('{"inscricoes":[' + '\n')

    for linhaCSV in open(arquivoCSV):
        nrLinha += 1
        
        
        linhaCSV = linhaCSV.rstrip()  # remove all kinds of trailing whitespace '\n'        
        if (nrLinha == 1):
            linhaCSV = linhaCSV.replace(" ","_").replace("-","_") # Na linha 1 (cabecalho) troca espaços e hifens por underline.

        linhaCSV = linhaCSV.split(";")

        # Na primeira linha, checa se o cabecalho do CSV tem todas as colunas esperadas.
        if (nrLinha == 1):
            linhaCSV = linhaCSV
            # Checa as colunas esperadas
            for col in colunasEsperadas:
                if (not col in linhaCSV):
                    print("Falta coluna [" + col + "] no arquivo!")
                    return
                # Guarda a posicao de cada coluna
                coluna_numero[col] = linhaCSV.index(col)
            continue # var para a proxima linha do for.

            
        linhaJSON = {}
        # Pega as colunas esperadas, e imprime-as.
        for col in colunasEsperadas:
            
            if (col == "Numero_de_inscricao"):
                if (linhaCSV[coluna_numero[col]] in codInscrList):
                    print("** ERRO ** CHAVE DUPLICADA! Linha: " + str(nrLinha) + " [Numero_de_inscricao]: " + linhaCSV[coluna_numero[col]])
                    break # sai deste for.
                codInscrList.append(linhaCSV[coluna_numero[col]].upper())
            
            linhaJSON[col] = linhaCSV[coluna_numero[col]].upper()
            
        if (len(linhaJSON) == 0):
            continue # var para a proxima linha desse "for loop".

        if (nrLinha > 2):
            file_json.write(',')
        
        file_json.write(json.dumps(linhaJSON) + '\n')
        

        
    file_json.write(']}' + '\n')
    file_json.close()
    return

converte_CSV_into_JSON("C:/workspace/corrida-bencao-de-paz/test/ListagemGeral_6238_07082018191948.csv",
                       "C:/workspace/corrida-bencao-de-paz/test/ListagemGeral_6238_07082018191948.JSON")
