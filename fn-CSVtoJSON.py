import json
def converte_CSV_into_JSON(arquivoCSV, arquivoJSON):

    
    nrLinha = 0
    coluna_numero = {}
    colunasEsperadas = "Cod_Inscr","Cod_Prova","Num_Atleta","Nome_Completo","Sexo","Dt_Nasc","CPF","Tel_Contato","Celular","Equipe","Camiseta"
    #colunasEsperadas = "id_seq","Modalidade","Categoria","ID_Usuario","Nome_Completo","Sexo","Email","Data_Nascto","Num_Documento","Camiseta","Equipe"
    codInscrList = []
    numAtletaList = []

    file_json = open(arquivoJSON, 'w')
    file_json.write('{"inscricoes":[' + '\n')

    for linhaCSV in open(arquivoCSV):
        nrLinha += 1
        
        
        linhaCSV = linhaCSV.rstrip()  # remove all kinds of trailing whitespace '\n'        
        linhaCSV = linhaCSV.split(";")

        # Na primeira linha, checa se o cabecalho do CSV tem todas as colunas esperadas.
        if (nrLinha == 1):
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
            
            if (col == "Cod_Inscr"):
                if (linhaCSV[coluna_numero[col]] in codInscrList):
                    print("** ERRO ** CHAVE DUPLICADA! Linha: " + str(nrLinha) + " [Cod_Inscr]: " + linhaCSV[coluna_numero[col]])
                    break # sai deste for.
                codInscrList.append(linhaCSV[coluna_numero[col]].upper())
                

            if (col == "Num_Atleta"):
                if (linhaCSV[coluna_numero[col]] in numAtletaList):
                    print("** AVISO ** Usuarios[Num_Atleta] repetidos! Linha: " + str(nrLinha) + " [Num_Atleta]: " + linhaCSV[coluna_numero[col]])
                numAtletaList.append(linhaCSV[coluna_numero[col]].upper())
                    
            
            linhaJSON[col] = linhaCSV[coluna_numero[col]].upper()
            
        if (len(linhaJSON) == 0):
            continue # var para a proxima linha do for.

        if (nrLinha > 2):
            file_json.write(',')
        
        file_json.write(json.dumps(linhaJSON) + '\n')
        

        
    file_json.write(']}' + '\n')
    file_json.close()
    return

converte_CSV_into_JSON("C:/workspace/corrida-bencao-de-paz/test/Inscricoes_bencao_de_paz_2018.csv",
                       "C:/workspace/corrida-bencao-de-paz/test/Inscricoes_bencao_de_paz_2018.JSON")
