import json
import boto3



def insertInscricao(event, context):
    
    # event is a dictionary object.
    
    try:
        
        # Checa se há algum conteúdo no body, e converte o conteúdo em um json.
        # Isso é necessário porque o body, mesmo contendo um json, vem dentro de aspas e com ENTERS e TABs.
        bodyRequest = event["body"]
        if (bodyRequest != ""):
            bodyRequest = json.loads(bodyRequest)
        else:
            bodyRequest = {}
    
        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('corrida-inscricoes')
        
        registroInscricao = {}
        
        nomeColunas = ("Cod_Inscr","Cod_Prova","Num_Atleta","Nome_Completo","Sexo","Dt_Nasc","CPF","Tel_Contato","Celular","Equipe","Camiseta","Kit_Entregue","Nome_Entregue","Data_Entregue")
        
        
        # Prepara o objeto [registroInscricao], colocando nele o nome de todas as colunas que o objeto terá. O objeto [registroInscricao], que é o registro que é enviado ao banco.
        for nomeColuna in nomeColunas:
            registroInscricao[nomeColuna] = " "
            
        
        if ("inscricoes" in bodyRequest):        
            # The batch writer is  able to handle a very large amount of writes to the table.
            with table.batch_writer() as batch:
                for registro in bodyRequest["inscricoes"]:
                    
                    registroInscricao["Kit_Entregue"] = "False"
                    registroInscricao["Nome_Completo"] = " "
                    registroInscricao["Data_Entregue"] = " "
                    for key, value in registro.items():
                        if (key in registroInscricao and str(value) != ""):
                            registroInscricao[key] = str(value)
                    #print(registroInscricao)
                    batch.put_item(Item=registroInscricao.copy())
                

        body = {
            "message": str(registroInscricao),
            #"message": "Os registros foram criados com sucesso!",
            "input": event
        }
    
    


    
        response = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin" : "*", # Required for CORS support to work
                "Access-Control-Allow-Credentials" : True # Required for cookies, authorization headers with HTTPS
            },
            "body": json.dumps(body)
        }
    except Exception as err:
        response = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin" : "*", # Required for CORS support to work
                "Access-Control-Allow-Credentials" : True # Required for cookies, authorization headers with HTTPS
            },
            "body": json.dumps({"Erro": {"Descricao": str(err)}})
        }
            

    return response

   