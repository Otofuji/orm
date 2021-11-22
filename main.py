#   Este é o projeto individual da disciplina Computação em Nuvem da Graduação em Engenharia de Computação do Insper Instituto de Ensino e Pesquisa. Para referência, o enunciado está no repositório como refs/Projeto.pdf. Referências podem ser encontradas em refs/references.txt e a elas também se somam os demais arquivos constantes no mesmo diretório.
#   Detalhes, discussões e decisões de projetos estão documentados em código na forma de comentários como este. Cada linha de comentário equivale a um parágrafo de um texto convencional. Para fins de leitura deste material, é recomendável que esteja com a quebra de linha ativada para visualizar o conteúdo de cada parágrafo na íntegra. No VS Code, isso pode ser feito pelo atalho Alt + Z (Windows) ou Option + Z (macOS). Comentários que começam com uma tabulação, como este, o anterior e o próximo, indicam necessariamente a existência de texto explicativo sobre o que está acontecendo. Comentários sem essa tabulação são comentários normais de Python, contendo informações breves de sinalização, caso exista. 
#   O primeiro passo do projeto é a definição de uma plataforma. Para fins deste projeto, foi eleito o Boto3, que é o AWS SDK para Python. Sua documentação completa pode ser vista em https://boto3.amazonaws.com/v1/documentation/api/latest/index.html. A escolha da Amazon AWS enquanto provedor de nuvem pública é uma definição do enunciado do projeto.
#   Existem duas formas de acessar uma instância na AWS usando boto3: low-level client e resource. O primeiro é um acesso 1:1 das chamadas de API da AWS. O último é bastante útil para quando se tem classes e objetos, pois as chamadas são relativas a esses objetos. Como não usaremos uma aplicação com classes e objetos, é mais racional usar client. 
#   Para autorizar devidamente o acesso, foi criada uma nova política denominada AdminOhio que herda AdministratorAccess para permitir o lançamento de instâncias em us-east-2. Além disso, já estava anteriormente implantada a política AdminVirginia, também herdada de AdministratorAccess, que permite o lançamento de instâncias em us-east-1. Feitas as devidas explicações, vamos propriamente para a implantação dos primeiros passos em código para a criação e lançamento de instância, tendo por base a documentação do AWS SDK para Python, mais conhecido por Boto3. 

#PRÉ-REQUISITO: Ter instalado AWS CLI e então o comando $ pip install 'boto3[crt]'

import sys
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')


#   Agora, será criada um resource para poder lançar uma instância. Isso não é de forma alguma um desvio do que foi escrito alguns parágrafos atrás. Pesquisando sobre como lançar instâncias, vi que é necessário que se faça via resource. Porém, de acordo com a documentação do Boto3, é possível criar um client facilmente a partir de um resource posteriormente, usando conforme necessário. Este trecho foi baseado no tutorial de KGP Talkie.

ec2_resource = boto3.resource('ec2')
instances = ec2_resource.create_instances(
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
    SecurityGroups = ['default']

)