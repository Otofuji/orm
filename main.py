#!/usr/bin/env python
# -*- coding: utf-8 -*-

#LINHAS LONGAS | USE QUEBRA DE LINHA PARA VISUALIZAR

#   Este é o projeto individual da disciplina Computação em Nuvem da Graduação em Engenharia de Computação do Insper Instituto de Ensino e Pesquisa. Para referência, o enunciado está no repositório como refs/Projeto.pdf. Referências podem ser encontradas em refs/references.txt e a elas também se somam os demais arquivos constantes no mesmo diretório.
#   Detalhes, discussões e decisões de projetos estão documentados em código na forma de comentários como este. Cada linha de comentário equivale a um parágrafo de um texto convencional. Para fins de leitura deste material, é recomendável que esteja com a quebra de linha ativada para visualizar o conteúdo de cada parágrafo na íntegra. No VS Code, isso pode ser feito pelo atalho Alt + Z (Windows) ou Option + Z (macOS). Comentários que começam com uma tabulação, como este, o anterior e o próximo, indicam necessariamente a existência de texto explicativo sobre o que está acontecendo. Comentários sem essa tabulação são comentários normais de Python, contendo informações breves de sinalização, caso exista. Nesse caso, a seguinte notação será usada: #BLOCO para indicar o início de um bloco, e #bloco para indicar o fim desse bloco.
#   O primeiro passo do projeto é a definição de uma plataforma. Para fins deste projeto, foi eleito o Boto3, que é o AWS SDK para Python. Sua documentação completa pode ser vista em https://boto3.amazonaws.com/v1/documentation/api/latest/index.html. A escolha da Amazon AWS enquanto provedor de nuvem pública é uma definição do enunciado do projeto.
#   Existem duas formas de acessar uma instância na AWS usando boto3: low-level client e resource. O primeiro é um acesso 1:1 das chamadas de API da AWS. O último é bastante útil para quando se tem classes e objetos, pois as chamadas são relativas a esses objetos. Como não usaremos uma aplicação com classes e objetos, é mais racional usar client. 
#   Para autorizar devidamente o acesso, foi criada uma nova política denominada AdminOhio que herda AdministratorAccess para permitir o lançamento de instâncias em us-east-2. Além disso, já estava anteriormente implantada a política AdminVirginia, também herdada de AdministratorAccess, que permite o lançamento de instâncias em us-east-1. Feitas as devidas explicações, vamos propriamente para a implantação dos primeiros passos em código para a criação e lançamento de instância, tendo por base a documentação do AWS SDK para Python, mais conhecido por Boto3. 

#PRÉ-REQUISITO: Ter instalado AWS CLI e então o comando $ pip install 'boto3[crt]'


#IMPORTS
import sys
import boto3
from botocore.exceptions import ClientError
import subprocess
#imports



#CLIENTE
ec2_us_east_1 = boto3.client('ec2', region_name = 'us-east-1')
ec2_us_east_2 = boto3.client('ec2', region_name = 'us-east-2')
#cliente


#   Inicialmente, havia lançado instância usando o Security Group manipulado diretamente no console da AWS, via navegador. Porém, para maior automatização e menor dependência de ter que ficar organizando as coisa por fora, vou configurar o SG por aqui mesmo usando o Boto3. Por referência, usarei a configuração de Security Group do KGP Talkie.
#   Durante a explicação do KGP Talkie, ele visualiza os SGs e, ao constatar nenhum SG fora o padrão, mostra como criar um Security Group. Isso funciona na primeira vez, mas me leva a pensar: e se rodar novamente? Ele não pode criar algo que já existe. Portanto, é necessário verificar se o SG já existe e, caso contrário, então proceder para criá-lo. Por referência, github@franciol faz essa verificação de forma mais dramática, mas suficientemente funcional para o nosso caso. Ele apaga o SG existente e então cria-o novamente. É a mesma lógica que usamos ao fazer DROP TABLE IF EXISTS antes de um CREATE TABLE em um banco de dados relacional. 
#   AVISO DISCIPLINAR: A um observador externo e conhecedor das diretrizes gerais de programação do Insper, pode suscitar dúvidas quanto à consulta feita ao trabalho elaborado por franciol. Todavia, cabe ressaltar que essa visualização foi feita dentro de premissas permitidas e legais, diante do objetivo de aprendizagem para este projeto, que envolve uma etapa de pesquisa tanto em documentação quanto em projetos similares. Não por interpretação minha, mas por explícita autorização tanto do professor da disciplina quanto do autor do projeto anterior e, além disso, com a explícita inclusão dos créditos a todas as referências consultadas. Note que a pasta de referências contém extensas documentações e linhas de referências em references.txt. Todo esse material foi usado para embasar este projeto e de forma nenhuma constitui plágio ou infração às diretrizes de integridade intelectual do Insper. Antes de proceder à visualização desse material, foi discutido com o professor em detalhes sobre essa autorização, definindo o que está dentro da proposta do projeto e é considerado aceitável ou recomendável. Portanto, declaro que tudo está dentro das regras como deveria estar e que não foi cometida nenhuma desonestidade intelectual no processo de elaboração deste projeto, submetido à avaliação para a disciplina Computação em Nuvem em 3 de dezembro de 2021. Caso você seja um aluno lendo isto para fazer o projeto de uma disciplina, converse com seu professor antes de prosseguir a leitura para ter certeza que está tudo bem estar lendo isso. Caso contrário, não prossiga com a leitura.

#APAGA SECURITY GROUP EXISTENTE
existing_SG = ec2_us_east_2.describe_vpcs()
vpc_id = existing_SG.get('Vpcs', [{}])[0].get('VpcId', '') 
try:
    resp = ec2_us_east_2.describe_security_groups()
    for i in resp['SecurityGroups']:
        if(i['GroupName'] == 'SG-US-EAST-2'):
            security_group_id = i['GroupId']
            resp = ec2_us_east_2.delete_security_group(GroupId=security_group_id)
except ClientError as e:
    print(e)
#apaga security group existente

#CRIA NOVO SECURITY GROUP
try:
    resp = ec2_us_east_2.create_security_group(GroupName='SG-US-EAST-2',
                                         Description='SG-US-EAST-2',
                                         VpcId=vpc_id)
    security_group_id = resp['GroupId']
    print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

    data = ec2_us_east_2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 5000,
             'ToPort': 5000,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
except ClientError as e:
    print(e)
#cria novo security group

#   Agora, será criada um resource para poder lançar uma instância. Isso não é de forma alguma um desvio do que foi escrito alguns parágrafos atrás. Pesquisando sobre como lançar instâncias, vi que é necessário que se faça via resource. Porém, de acordo com a documentação do Boto3, é possível criar um client facilmente a partir de um resource posteriormente, usando conforme necessário. Este trecho foi baseado no tutorial de KGP Talkie. 

#CRIA NOVA INSTÂNCIA
ec2_resource_us_east_2 = boto3.resource('ec2', region_name = 'us-east-2')
instances = ec2_resource_us_east_2.create_instances(
    ImageId = 'ami-020db2c14939a8efb', #Ubuntu Server 18.04 LTS (HVM), SSD Volume Type 64 bits x86
    MinCount = 1,
    MaxCount = 1,
    InstanceType = 't2.micro',
    KeyName = 'KeyName',
    BlockDeviceMappings = [
        {
            'DeviceName' : "/dev/xvda",
            'Ebs' :{
                'DeleteOnTermination': False,
                'VolumeSize': 20
            }
        }
    ],
    SecurityGroups = ['SG-US-EAST-2']

)
#cria nova instância