#   Este é o projeto individual da disciplina Computação em Nuvem da Graduação em Engenharia de Computação do Insper Instituto de Ensino e Pesquisa. Para referência, o enunciado está no repositório como Projeto.pdf.
#   Detalhes, discussões e decisões de projetos estão documentados em código na forma de comentários como este. Cada linha de comentário equivale a um parágrafo de um texto convencional. Para fins de leitura deste material, é recomendável que esteja com a quebra de linha ativada para visualizar o conteúdo de cada parágrafo na íntegra. No VS Code, isso pode ser feito pelo atalho Alt + Z (Windows) ou Option + Z (macOS). Comentários que começam com uma tabulação, como este, o anterior e o próximo, indicam necessariamente a existência de texto explicativo sobre o que está acontecendo. Comentários sem essa tabulação são comentários normais de Python, contendo informações breves de sinalização, caso exista. 
#   O primeiro passo do projeto é a definição de uma plataforma. Para fins deste projeto, foi eleito o Boto3, que é o AWS SDK para Python. Sua documentação completa pode ser vista em https://boto3.amazonaws.com/v1/documentation/api/latest/index.html. A escolha da Amazon AWS enquanto provedor de nuvem pública é uma definição do enunciado do projeto.
#   Existem duas formas de acessar uma instância na AWS usando boto3: low-level client e resource. O primeiro é um acesso 1:1 das chamadas de API da AWS. O último é bastante útil para quando se tem classes e objetos, pois as chamadas são relativas a esses objetos. Como não usaremos uma aplicação com classes e objetos, é mais racional usar client. 
#   Para autorizar devidamente o acesso, foi criada uma nova política denominada AdminOhio que herda AdministratorAccess para permitir o lançamento de instâncias em us-east-2. Além disso, já estava anteriormente implantada a política AdminVirginia, também herdada de AdministratorAccess, que permite o lançamento de instâncias em us-east-1. Feitas as devidas explicações, vamos propriamente para a implantação dos primeiros passos em código para a criação e lançamento de instância, tendo por base a documentação do AWS SDK para Python, mais conhecido por Boto3. 

#PRÉ-REQUISITO: Ter instalado AWS CLI e então o comando $ pip install 'boto3[crt]'

import sys
import boto3
from botocore.exceptions import ClientError

instance_id = sys.argv[2]
action = sys.argv[1].upper()

ec2 = boto3.client('ec2')


if action == 'ON':
    # Do a dryrun first to verify permissions
    try:
        ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)
else:
    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)..