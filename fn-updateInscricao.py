import json
import boto3



def updateInscricao(event, context):
    
    # event is a dictionary object.
    
    try:
        
        print(event)
        
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
        
                
        nomeColunas = ("Cod_Inscr","Kit_Entregue","Nome_Entregue")        
        
        
        if ("inscricoes" in bodyRequest):        
            
            for registro in bodyRequest["inscricoes"]:
                response = table.update_item(Key={"Cod_Inscr":registro["Cod_Inscr"]},
                                             UpdateExpression="SET Kit_Entregue = :Kit_Entregue, Nome_Entregue = :Nome_Entregue, Data_Entregue = :Data_Entregue",
                                             ExpressionAttributeValues={":Kit_Entregue": registro["Kit_Entregue"], 
                                                                        ":Nome_Entregue": registro["Nome_Entregue"],
                                                                        ":Data_Entregue": registro["Data_Entregue"]},
                                             ReturnValues= "UPDATED_NEW")

                
                

        body = {
            "message": str(response),
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

   