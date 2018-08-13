import json
import boto3
from boto3.dynamodb.conditions import Key, Attr



def getInscricao(event, context):
    
    try:
        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('corrida-inscricoes')
        
        body = {}
        
        response = ""
        
        # GET request
        if ("queryStringParameters" in event):
        
        
            response = table.scan(
                    ProjectionExpression="Numero_de_inscricao",
                    FilterExpression=Attr("Kit_Entregue").eq("False")
                )
            
            print(response)
            
            # ScannedCount — the number of items that matched the key condition expression, before a filter expression (if present) was applied..
            body["TotalKits"] = response["ScannedCount"]
            
            # Count — the number of items that remain, after a filter expression (if present) was applied.
            body["KitsNaoEntregues"] = response["Count"]
            
            
        
            # Attributes I want to see.
            columns_to_return = "Numero_de_inscricao,Kit_Entregue,Nome_Completo,CAMISETA,CAMISETA_KIDS"

            Numero_de_inscricao = ""
            Nome_Completo = ""
            Documento = ""
            Pesquisa_texto = ""
            Kit_Entregue = "False"            
                
            for key, value in event["queryStringParameters"].items():
                if (key == "Numero_de_inscricao"):
                    Numero_de_inscricao = value
                if (key == "Nome_Completo"):
                    Nome_Completo = value.upper()
                if (key == "Documento"):
                    Documento = value
                if (key == "Pesquisa_texto"):
                    Pesquisa_texto = value.upper()
                if (key == "somenteNaoEntregues"):
                    if (value == "True"):
                        Kit_Entregue = "False"
                    else:
                        Kit_Entregue = "True"
                    
             # Pesquisa por [Numero_de_inscricao]
            if (Numero_de_inscricao != ""):
                response = table.scan(
                    ProjectionExpression=columns_to_return,
                    FilterExpression=Attr("Numero_de_inscricao").eq(Numero_de_inscricao)
                )
                    
            # Pesquisa por [Nome_Completo]
            if (Nome_Completo != ""):
                response = table.scan(
                    ProjectionExpression=columns_to_return,
                    FilterExpression=
                    Attr("Kit_Entregue").eq(Kit_Entregue) &
                    Attr('Nome_Completo').begins_with(Nome_Completo)
                )
                    
            # Pesquisa por [Documento]
            elif (Documento != ""):
                response = table.scan(
                    ProjectionExpression=columns_to_return,
                    FilterExpression=
                    Attr("Kit_Entregue").eq(Kit_Entregue) &
                    Attr("Documento").contains(Documento)

                )

            # Pesquisa por qualquer campo
            else:
                response = table.scan(
                    ProjectionExpression=columns_to_return,
                    FilterExpression=
                    Attr("Kit_Entregue").eq(Kit_Entregue) & (
                        Attr("Numero_de_inscricao").contains(Pesquisa_texto) |
                        Attr("Nome_Completo").contains(Pesquisa_texto) |
                        Attr("Documento").contains(Pesquisa_texto)
                    )
                )
                

            # Count — the number of items that remain, after a filter expression (if present) was applied.
            body["TotalSelecionado"] = response["Count"]
        

        print(response)
        
        keyNames = ("Numero_de_inscricao","Grupo_Categoria","Categoria","Nome_Completo","Data_de_nascimento","E_mail","Tipo_de_Documento","Documento","Sexo","CAMISETA","CAMISETA_KIDS","Kit_Entregue","Nome_Entregue","Data_Entregue")
        
        body["message"] = ""
        
        # Se tiver apenas 1 item na resposta
        if ('Item' in response):
            body["Item"] = {}
            item = response["Item"]
            for key in keyNames:
                if (key in item):
                    body["Item"][key] = item[key].title()
                    if (key == "CAMISETA" or key == "CAMISETA_KIDS"):
                        body["Item"][key] = body["Item"][key].upper()
            
            
        
        # Se tiverem vários itens na resposta
        elif ('Items' in response):
            body["Items"] = []
            ix = 0
            itemsList = sorted(response["Items"], key=lambda k: k["Nome_Completo"])

            for item in itemsList:
                body["Items"].append({})
                for key in keyNames:
                    if (key in item):
                        body["Items"][ix][key] = item[key].title()
                        if (key == "CAMISETA" or key == "CAMISETA_KIDS"):
                            body["Items"][ix][key] = body["Items"][ix][key].upper()
                ix += 1
        else:
            body["message"] = "Id não encontrado!"
            

        body["input"] = event
        

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

   
    
def getAtletasPorGrupoNome(event, context):
    
    try:
        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('corrida-inscricoes')
        
        body = {}
        
        response = ""
        
        # GET request
        if ("queryStringParameters" in event):
        
        
            response = table.scan(
                    ProjectionExpression="Numero_de_inscricao",
                    FilterExpression=Attr("Kit_Entregue").eq("False")
                )
            
            print(response)
            
            # ScannedCount — the number of items that matched the key condition expression, before a filter expression (if present) was applied..
            body["TotalKits"] = response["ScannedCount"]
            
            # Count — the number of items that remain, after a filter expression (if present) was applied.
            body["KitsNaoEntregues"] = response["Count"]
            
            
        
            # Attributes I want to see.
            columns_to_return = "Numero_de_inscricao,Kit_Entregue,Nome_Completo,CAMISETA,CAMISETA_KIDS"
            
            # Pesquisa por [Nome_Completo]
            if ("idGrupo" in event["queryStringParameters"] and event["queryStringParameters"]["idGrupo"] != ""):
                idGrupo = event["queryStringParameters"]["idGrupo"]
                if idGrupo == "ad":
                    
                    response = table.scan(
                        ProjectionExpression=columns_to_return,
                        FilterExpression=
                        Attr("Kit_Entregue").eq("False") &
                        (
                            Attr('Nome_Completo').begins_with("A") |
                            Attr("Nome_Completo").begins_with("B") |
                            Attr("Nome_Completo").begins_with("C") |
                            Attr("Nome_Completo").begins_with("D")
                        )
                    )
                elif idGrupo == "eh":
                    response = table.scan(
                        ProjectionExpression=columns_to_return,
                        FilterExpression=
                        Attr("Kit_Entregue").eq("False") &
                        (
                            Attr('Nome_Completo').begins_with("E") |
                            Attr("Nome_Completo").begins_with("F") |
                            Attr("Nome_Completo").begins_with("G") |
                            Attr("Nome_Completo").begins_with("H")
                        )
                    )
                elif idGrupo == "il":
                    response = table.scan(
                        ProjectionExpression=columns_to_return,
                        FilterExpression=
                        Attr("Kit_Entregue").eq("False") &
                        (
                            Attr('Nome_Completo').begins_with("I") |
                            Attr("Nome_Completo").begins_with("J") |
                            Attr("Nome_Completo").begins_with("K") |
                            Attr("Nome_Completo").begins_with("L")
                        )
                    )
                elif idGrupo == "mp":
                    response = table.scan(
                        ProjectionExpression=columns_to_return,
                        FilterExpression=
                        Attr("Kit_Entregue").eq("False") &
                        (
                            Attr('Nome_Completo').begins_with("M") |
                            Attr("Nome_Completo").begins_with("N") |
                            Attr("Nome_Completo").begins_with("O") |
                            Attr("Nome_Completo").begins_with("P")
                        )
                    )
                elif idGrupo == "qt":
                    response = table.scan(
                        ProjectionExpression=columns_to_return,
                        FilterExpression=
                        Attr("Kit_Entregue").eq("False") &
                        (
                            Attr('Nome_Completo').begins_with("Q") |
                            Attr("Nome_Completo").begins_with("R") |
                            Attr("Nome_Completo").begins_with("S") |
                            Attr("Nome_Completo").begins_with("T")
                        )
                    )
                elif idGrupo == "uz":
                    response = table.scan(
                        ProjectionExpression=columns_to_return,
                        FilterExpression=
                        Attr("Kit_Entregue").eq("False") &
                        (
                            Attr('Nome_Completo').begins_with("U") |
                            Attr("Nome_Completo").begins_with("V") |
                            Attr("Nome_Completo").begins_with("W") |
                            Attr("Nome_Completo").begins_with("X") |
                            Attr("Nome_Completo").begins_with("Y") |
                            Attr("Nome_Completo").begins_with("Z")
                        )
                    )
                    


            # Count — the number of items that remain, after a filter expression (if present) was applied.
            body["TotalSelecionado"] = response["Count"]
        

        print(response)
        
        keyNames = ("Numero_de_inscricao","Grupo_Categoria","Categoria","Nome_Completo","Data_de_nascimento","E_mail","Tipo_de_Documento","Documento","Sexo","CAMISETA","CAMISETA_KIDS","Kit_Entregue","Nome_Entregue","Data_Entregue")
        
        body["message"] = ""
        
        # Se tiver apenas 1 item na resposta
        if ('Item' in response):
            body["Item"] = {}
            item = response["Item"]
            for key in keyNames:
                if (key in item):
                    body["Item"][key] = item[key].title()
                    if (key == "CAMISETA" or key == "CAMISETA_KIDS"):
                        body["Item"][key] = body["Item"][key].upper()
            
            
        
        # Se tiverem vários itens na resposta
        elif ('Items' in response):
            body["Items"] = []
            ix = 0
            itemsList = sorted(response["Items"], key=lambda k: k["Nome_Completo"])
            for item in itemsList:
                body["Items"].append({})
                for key in keyNames:
                    if (key in item):
                        body["Items"][ix][key] = item[key].title()
                        if (key == "CAMISETA" or key == "CAMISETA_KIDS"):
                            body["Items"][ix][key] = body["Items"][ix][key].upper()
                ix += 1
        else:
            body["message"] = "Id não encontrado!"
            

        body["input"] = event
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





def getDetalheAtleta(event, context):
    
    try:
        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('corrida-inscricoes')
        
        body = {}
        response = ""
        
        # GET request
        if ("queryStringParameters" in event):
        
            response = table.scan(ProjectionExpression="Numero_de_inscricao",FilterExpression=Attr("Kit_Entregue").eq("False"))
            
            # ScannedCount — the number of items that matched the key condition expression, before a filter expression (if present) was applied..
            body["TotalKits"] = response["ScannedCount"]
            
            # Count — the number of items that remain, after a filter expression (if present) was applied.
            body["KitsNaoEntregues"] = response["Count"]
            
            # Pesquisa por [Numero_de_inscricao]
            if ("Numero_de_inscricao" in event["queryStringParameters"]):
                
                Numero_de_inscricao = event["queryStringParameters"]["Numero_de_inscricao"]
                
                response = table.scan(FilterExpression=Attr("Numero_de_inscricao").eq(Numero_de_inscricao))

            # Count — the number of items that remain, after a filter expression (if present) was applied.
            body["TotalSelecionado"] = response["Count"]        

        print(response)
        
        body["message"] = ""
        
        # Se tiver apenas 1 item na resposta
        if ('Item' in response):
            body["Item"] = {}
            item = response["Item"]
            for key, value in item.items():
                body["Item"][key] = value.title()
                if (key == "CAMISETA" or key == "CAMISETA_KIDS"):
                    body["Item"][key] = body["Item"][key].upper()
            
            
        
        # Se tiverem vários itens na resposta
        elif ('Items' in response):
            body["Items"] = []
            ix = 0
            itemsList = sorted(response["Items"], key=lambda k: k["Nome_Completo"])
            for item in itemsList:
                body["Items"].append({})
                for key,value in item.items():
                    body["Items"][ix][key] = item[key].title()
                    if (key == "CAMISETA" or key == "CAMISETA_KIDS"):
                        body["Items"][ix][key] = body["Items"][ix][key].upper()
                ix += 1
        else:
            body["message"] = "Id não encontrado!"            

        body["input"] = event

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


def getDownloadAllRecords(event, context):
    
    try:
        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('corrida-inscricoes')
        
        body = {}
                
        response = table.scan(FilterExpression=Attr("Numero_de_inscricao").exists())
        print(response)        
        
        body["message"] = ""
        
        body["Items"] = []
        ix = 0
        itemsList = sorted(response["Items"], key=lambda k: k["Nome_Completo"])
        for item in itemsList:
            body["Items"].append({})
            for key,value in item.items():
                body["Items"][ix][key] = item[key].title().strip()
                if (key == "CAMISETA" or key == "CAMISETA_KIDS"):
                    body["Items"][ix][key] = body["Items"][ix][key].upper()
            ix += 1

        body["input"] = event
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
