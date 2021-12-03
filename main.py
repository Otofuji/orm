#!/usr/bin/env python
# -*- coding: utf-8 -*-

#LINHAS LONGAS | USE QUEBRA DE LINHA PARA VISUALIZAR

def readme():
    #   Este é o projeto individual da disciplina Computação em Nuvem da Graduação em Engenharia de Computação do Insper Instituto de Ensino e Pesquisa. Para referência, o enunciado está no repositório como refs/Projeto.pdf. Referências podem ser encontradas em refs/references.txt e a elas também se somam os demais arquivos constantes no mesmo diretório.
    #   Detalhes, discussões e decisões de projetos estão documentados em código na forma de comentários como este. Cada linha de comentário equivale a um parágrafo de um texto convencional. Para fins de leitura deste material, é recomendável que esteja com a quebra de linha ativada para visualizar o conteúdo de cada parágrafo na íntegra. No VS Code, isso pode ser feito pelo atalho Alt + Z (Windows) ou Option + Z (macOS). Comentários que começam com uma tabulação, como este, o anterior e o próximo, indicam necessariamente a existência de texto explicativo sobre o que está acontecendo. Comentários sem essa tabulação são comentários normais de Python, contendo informações breves de sinalização, caso exista. Nesse caso, a seguinte notação será usada:
    #  
    # #BLOCO para indicar o início de um bloco, e 
    # #bloco para indicar o fim desse bloco.

    #   O primeiro passo do projeto é a definição de uma plataforma. Para fins deste projeto, foi eleito o Boto3, que é o AWS SDK para Python. Sua documentação completa pode ser vista em https://boto3.amazonaws.com/v1/documentation/api/latest/index.html. A escolha da Amazon AWS enquanto provedor de nuvem pública é uma definição do enunciado do projeto.
    #   Existem duas formas de acessar uma instância na AWS usando boto3: low-level client e resource. O primeiro é um acesso 1:1 das chamadas de API da AWS. O último é bastante útil para quando se tem classes e objetos, pois as chamadas são relativas a esses objetos. Como não usaremos uma aplicação com classes e objetos, é mais racional usar client. 
    #   Para autorizar devidamente o acesso, foi criada uma nova política denominada AdminOhio que herda AdministratorAccess para permitir o lançamento de instâncias em us-east-2. Além disso, já estava anteriormente implantada a política AdminVirginia, também herdada de AdministratorAccess, que permite o lançamento de instâncias em us-east-1. Feitas as devidas explicações, vamos propriamente para a implantação dos primeiros passos em código para a criação e lançamento de instância, tendo por base a documentação do AWS SDK para Python, mais conhecido por Boto3. 
    #   Inicialmente, havia lançado instância usando o Security Group manipulado diretamente no console da AWS, via navegador. Porém, para maior automatização e menor dependência de ter que ficar organizando as coisa por fora, vou regionurar o SG por aqui mesmo usando o Boto3. Por referência, usarei a regionuração de Security Group do KGP Talkie.
    #   Durante a explicação do KGP Talkie, ele visualiza os SGs e, ao constatar nenhum SG fora o padrão, mostra como criar um Security Group. Isso funciona na primeira vez, mas me leva a pensar: e se rodar novamente? Ele não pode criar algo que já existe. Portanto, é necessário verificar se o SG já existe e, caso contrário, então proceder para criá-lo. Por referência, github@franciol faz essa verificação de forma mais dramática, mas suficientemente funcional para o nosso caso. Ele apaga o SG existente e então cria-o novamente. É a mesma lógica que usamos ao fazer DROP TABLE IF EXISTS antes de um CREATE TABLE em um banco de dados relacional. 
    #   AVISO DISCIPLINAR: A um observador externo e conhecedor das diretrizes gerais de programação do Insper, pode suscitar dúvidas quanto à consulta feita ao trabalho elaborado por franciol. Todavia, cabe ressaltar que essa visualização foi feita dentro de premissas permitidas e legais, diante do objetivo de aprendizagem para este projeto, que envolve uma etapa de pesquisa tanto em documentação quanto em projetos similares. Não por interpretação minha, mas por explícita autorização tanto do professor da disciplina quanto do autor do projeto anterior e, além disso, com a explícita inclusão dos créditos a todas as referências consultadas. Note que a pasta de referências contém extensas documentações e linhas de referências em references.txt. Todo esse material foi usado para embasar este projeto e de forma nenhuma constitui plágio ou infração às diretrizes de integridade intelectual do Insper. Antes de proceder à visualização desse material, foi discutido com o professor em detalhes sobre essa autorização, definindo o que está dentro da proposta do projeto e é considerado aceitável ou recomendável. Portanto, declaro que tudo está dentro das regras como deveria estar e que não foi cometida nenhuma desonestidade intelectual no processo de elaboração deste projeto, submetido à avaliação para a disciplina Computação em Nuvem em 3 de dezembro de 2021. Caso você seja um aluno lendo isto para fazer o projeto de uma disciplina, converse com seu professor antes de prosseguir a leitura para ter certeza que está tudo bem estar lendo isso. Caso contrário, não prossiga com a leitura.
    #   Até 26/11/2021, estava tendando primeiro criar os SGs para depois verificar as instâncias. Porém, me deparei com um problema inesperado. Ao rodar o programa pela segunda vez, ele não conseguia apagar o SG existente. De acordo com https://stackoverflow.com/questions/61236712/unable-to-delete-security-group-an-error-occurred-dependencyviolation-when-ca, isso se deve à existência de uma instância que foi criada na última vez em que foi rodado. Para contornar isso, primeiro apagarei as instâncias existentes, usando uma adaptação prática do que consta na documentação do Boto3 https://boto3.amazonaws.com/v1/documentation/api/latest/guide/migrationec2.html. Porém, após isso, o problema persistiu. Em conversas com Henrique Mualem, ele sugeriu uma forma diferente de realizar o mesmo procedimento. Primeiro, pega-se as instâncias usando ec2.describe_instances() ao invés de ec2.instances.filter() como havia feito inicialmente, e então filtrar os dados desse dicionário. Além disso, não estava aguardando que a instância termine, pois era necessário aguardar e, por isso, estava dando erro. Passei então a usar esse método sugerido por ele a partir de 29/11/2021, que consiste, além do mencionado, no seguinte: descrever as instâncias e SGs existentes e então deletar as instâncias usando o SG que estamos querendo usar (assim, caso haja outra instância para alguma outra coisa, este código não atrapalha ela). Após fazer isso, aguardar cinco segundos e veificar se a instância foi encerrada, e caso não aguardar mais cinco segundos. Após confirmado o encerramento da instância, apaga-se o SG de interesse e então cria-se ele. Após, autorizar o Security Group e por fim criar a instância na forma como estava criando ele inicialmente seguindo o modo sugerido pelo KGP Talkie no seu vídeo tutorial.
    #   Será criada um resource para poder lançar uma instância. Isso não é de forma alguma um desvio do que foi escrito alguns parágrafos atrás. Pesquisando sobre como lançar instâncias, vi que é necessário que se faça via resource. Porém, de acordo com a documentação do Boto3, é possível criar um client facilmente a partir de um resource posteriormente, usando conforme necessário. Este trecho foi baseado no tutorial de KGP Talkie. 
    #   Até 29/11/2021 (239443089bbd8e8d72f14f3c5bf6ab8303fe90e9), as operações de apagar instâncias e security groups existentes e então criar security group e instância funcionam perfeitamente para Ohio, mas por um motivo que a lógica não é capaz de explicar, não funciona para a Virgínia do Norte, embora seja empregado exatamente o mesmo código da mesma forma. Isso não faz sentido algum. Conversando com colegas que passaram por essa parte, não fizeram nada de diferente, exceto pelo fato de terem usado funções ao invés de escrever o código hardcoded de forma sequencial como se fosse um programa Assembly como fiz até o commit 239443089bbd8e8d72f14f3c5bf6ab8303fe90e9. Optei por então refatorar o código, criando uma única função que dispara instâncias após verificar e apagar SG e instâncias anteriores, e chamando ela depois duas vezes, uma para cada região.
    #    Em 30/11/2021, porém, reparei que essa arquitetura não será adequada para as próximas etapas do projeto. Isso porque se a criação de instâncias se dá dentro de uma função, devido às variáveis locais será difícil acessar os clientes do boto3. Refletindo sobre o programa, decidi refatorar novamente, e agora separando as regiões por scripts hardcoded. Este script, o main, será responsável por orquestrar os deploys, sendo que o apagamento de instâncias existentes, apagamento de security groups existentes e lançamento de novas instâncias em cada região serão feitos em scripts separados. 
    #   Decidi por uma nova refatoração no mesmo dia logo em seguida, trazendo tudo para o mesmo script, mas separando por funções. Assim, o que tem que ser feito numa região é uma função, e o que tem que ser feito na outra região é outra função. Isso resolve o problema mencionado acima.
    #   O banco de dados é instalado em Ohio usando UserData, e a aplicação Django de Raul Ikeda (https://github.com/rauilikeda/tasks) é configurada na Virgínia, apontando para Ohio, feitas as devidas configurações.
    #   Para aguardar a configuração da máquina Django em Virgínia, após inicializar a instância, faço um loop infinito fazendo conexão SSH via biblioteca paramiko, conectando e desconectando incessantemente. Até que chega um momento em que isso dá erro, ou seja, não é possível conectar usando paramiko. Isso quer dizer que a instância está fazendo reboot e, portanto, concluiu a configuração. Basta aguardar o reboot para que a aplicação esteja no ar. 
    #PRÉ-REQUISITO: Ter instalado AWS CLI e então o comando $ pip install 'boto3[crt]'
    return None 

#IMPORTS
import boto3
from botocore.exceptions import ClientError
import time
import paramiko
#imports

def deploy_us_east_2():
    
    finishing = False

    #CLIENTE E RECURSO
    ec2_us_east_2 = boto3.client('ec2', region_name = 'us-east-2')
    ec2_resource_us_east_2 = boto3.resource('ec2', region_name = 'us-east-2')
    #cliente e recurso

    #APAGA INSTÂNCIAS DE OHIO
    finishing = False
    instances = ec2_us_east_2.describe_instances()
    instances_amount = len(instances['Reservations'])
    existing_SG = ec2_us_east_2.describe_security_groups()['SecurityGroups']
    SG_amount = len(existing_SG)
    for i in range(instances_amount):
        
        try:
            instances_SG = instances['Reservations'][i]['Instances'][0]['NetworkInterfaces'][0]['Groups'][0]['GroupName']
            if instances_SG == 'SG-US-EAST-2':
                instance_id = instances['Reservations'][i]['Instances'][0]['InstanceId']
                ec2_us_east_2.terminate_instances(InstanceIds = [instance_id])
                finishing = True
                print("Apagando uma instância em Ohio")
        except:
            pass
        
    while finishing:
        time.sleep(5)
        finishing = False
        instances = ec2_us_east_2.describe_instances()
        for i in range(instances_amount):
            try:
                instances_SG = instances['Reservations'][i]['Instances'][0]['NetworkInterfaces'][0]['Groups'][0]['GroupName']
                if instances_SG == 'SG-US-EAST-2':
                    finishing = True
                    print("    Aguarde o término da instância em Ohio")
            except:
                pass
        time.sleep(5)
    print("        Terminou instâncias em Ohio")

    #apaga instâncias de Ohio


    #APAGA SECURITY GROUP EXISTENTE DE OHIO
    print("Apagando SG-US-EAST-2")
    existing_SG = ec2_us_east_2.describe_vpcs()
    vpc_id = existing_SG.get('Vpcs', [{}])[0].get('VpcId', '')
    vpc = existing_SG.get('Vpcs', [{}])[0]
    print("    VpcId Ohio")
    print("        ", vpc_id)

    for i in range (SG_amount):
        try:    
            print("    Verificando apagar o Security Group")
            print("        ", ec2_us_east_2.describe_security_groups()["SecurityGroups"][i]["GroupName"])
            if (ec2_us_east_2.describe_security_groups()["SecurityGroups"][i]["GroupName"] == "SG-US-EAST-2"):
                ec2_us_east_2.delete_security_group(GroupName = "SG-US-EAST-2")
                print("            Apagou SG de Ohio")
                break
        except:
            print("        Não foi possível apagar o Security Group")

    #apaga security group existente de Ohio


    #CRIA NOVO SECURITY GROUP EM OHIO
    print("Criando novo SG em Ohio")

    try:
        
        resp = ec2_us_east_2.create_security_group(GroupName='SG-US-EAST-2',
                                            Description='SG-US-EAST-2',
                                            VpcId=vpc_id)
        us_east_2_security_group_id = resp['GroupId']
        print(us_east_2_security_group_id)
        print('Security Group Created %s in vpc %s.' % (us_east_2_security_group_id, vpc_id))

        data_in = ec2_us_east_2.authorize_security_group_ingress(
            GroupId=us_east_2_security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 8080,
                'ToPort': 8080,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 5432,
                'ToPort': 5432,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        data_out = ec2_us_east_2.authorize_security_group_egress(
            GroupId=us_east_2_security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 8080,
                'ToPort': 8080,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 5432,
                'ToPort': 5432,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print("Criou SG em Ohio")
    except ClientError as e:
        print(e)
    #cria novo security group em Ohio

    #CRIA NOVA INSTÂNCIA EM OHIO
    print("Criando nova instância em Ohio")

    user_data = str("""#cloud-config
    runcmd:
    - cd /home/ubuntu;
    - sudo apt update;
    - sudo apt upgrade -y;
    - sudo apt autoremove -y;
    - sudo apt install postgresql postgresql-contrib -y;
    - sudo su - postgres;
    - sudo -u postgres psql -c "CREATE USER cloud WITH PASSWORD 'cloud';";
    - sudo -u postgres psql -c "CREATE DATABASE tasks;";
    - sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE tasks TO cloud;";
    - sudo echo "listen_addresses = '*'" >> /etc/postgresql/10/main/postgresql.conf;
    - sudo echo "host all all 0.0.0.0/0 trust" >> /etc/postgresql/10/main/pg_hba.conf;
    - sudo ufw allow 5432/tcp -y
    - sudo systemctl restart postgresql
    - sudo reboot;
    """)

    print(user_data)

    instances = ec2_resource_us_east_2.create_instances(
        ImageId = 'ami-020db2c14939a8efb', #Ubuntu Server 18.04 LTS (HVM), SSD Volume Type 64 bits x86
        UserData = user_data,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = 't2.micro',
        KeyName = 'KeyName_us_east_2',
        BlockDeviceMappings = [
            {
                'DeviceName' : "/dev/xvda",
                'Ebs' :{
                    'DeleteOnTermination': True,
                    'VolumeSize': 20
                }
            }
        ],
        SecurityGroups = ['SG-US-EAST-2']

    )
    print("Criou nova instância em Ohio")
    #cria nova instância em Ohio


    #CONFIGURA A NOVA INSTÂNCIA 
    instance = instances[0]
    print("Aguardando a instância estar rodando")
    instance.wait_until_running()
    instance.load()
    print(instance.public_dns_name)
    public_dns_name: str = "ubuntu@" + instance.public_dns_name
    print(public_dns_name)
    postgresIP = str(instance.public_ip_address)
    user_data = user_data.replace("postgresIP", postgresIP)
    time.sleep(30)
    
    k = paramiko.RSAKey.from_private_key_file("/Users/otofuji/.ssh/KeyName_us_east_2.pem")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print ("connecting")

    c.connect( hostname = instance.public_dns_name, port = 22,  username = "ubuntu", password=None, pkey = k, key_filename = None, timeout=None,  allow_agent=True, look_for_keys=True, compress=False, sock=None, gss_auth=False, gss_kex=False, gss_deleg_creds=True, gss_host=None, banner_timeout=None, auth_timeout=None, gss_trust_dns=True, passphrase=None, disabled_algorithms=None )
    print ("connected")
    print("CONFIGURANDO")
    commands = [""]
    for command in commands:
        
        stdin , stdout, stderr = c.exec_command(command)
        print("")
        print(stdout.read())
        print("")
        print(stderr.read())
        
    c.close()
    print("    Comandos de configuração enviados para a instância")
    print("")
    print("")
    print("")

    return instance.public_ip_address

def deploy_us_east_1(us_east_2_ip):
    
    finishing = False

    #CLIENTE E RECURSO
    ec2_us_east_1 = boto3.client('ec2', region_name = 'us-east-1')
    ec2_resource_us_east_1 = boto3.resource('ec2', region_name = 'us-east-1')
    elastic_load_balancer = boto3.client('elbv2', region_name='us-east-1')
    #cliente e recurso

    #APAGA INSTÂNCIAS DE VIRGÍNIA DO NORTE
    finishing = False
    instances = ec2_us_east_1.describe_instances()
    instances_amount = len(instances['Reservations'])
    existing_SG = ec2_us_east_1.describe_security_groups()['SecurityGroups']
    SG_amount = len(existing_SG)
    for i in range(instances_amount):
        
        try:
            instances_SG = instances['Reservations'][i]['Instances'][0]['NetworkInterfaces'][0]['Groups'][0]['GroupName']
            if instances_SG == 'SG-US-EAST-1':
                instance_id = instances['Reservations'][i]['Instances'][0]['InstanceId']
                ec2_us_east_1.terminate_instances(InstanceIds = [instance_id])
                finishing = True
                print("Apagando uma instância em Virgínia do Norte")
        except:
            pass
        
    while finishing:
        time.sleep(5)
        finishing = False
        instances = ec2_us_east_1.describe_instances()
        for i in range(instances_amount):
            try:
                instances_SG = instances['Reservations'][i]['Instances'][0]['NetworkInterfaces'][0]['Groups'][0]['GroupName']
                if instances_SG == 'SG-US-EAST-1':
                    finishing = True
                    print("    Aguarde o término da instância em Virgínia do Norte")
            except:
                pass
        time.sleep(5)
    print("        Terminou instâncias em Virgínia do Norte")

    #apaga instâncias de Virgínia do Norte

    #APAGA LOAD BALANCER VIRGÍNIA DO NORTE
    try:
        existing_lb = elastic_load_balancer.describe_load_balancers()
        lb_arn: str = str(existing_lb['LoadBalancers'][0]['LoadBalancerArn'])
        print("lb_arn")
        print("    ", lb_arn)
        free_of_lb = elastic_load_balancer.delete_load_balancer(LoadBalancerArn=lb_arn)
        print(free_of_lb)
        print("    LOAD BALANCER APAGADO")
        time.sleep(30)
    except Exception as e:
        print("")
        print("")
        print(e)
        print("")
        print("")
    #apaga load balancer Virgínia do Norte


    #APAGA SECURITY GROUP EXISTENTE DE VIRGÍNIA DO NORTE
    print("Apagando SG-US-EAST-1")
    existing_SG = ec2_us_east_1.describe_vpcs()
    vpc_id = existing_SG.get('Vpcs', [{}])[0].get('VpcId', '')
    print("    VpcId Virgínia do Norte")
    print("        ", vpc_id)

    for i in range (SG_amount):
        try:    
            print("    Verificando apagar o Security Group")
            print("        ", ec2_us_east_1.describe_security_groups()["SecurityGroups"][i]["GroupName"])
            if (ec2_us_east_1.describe_security_groups()["SecurityGroups"][i]["GroupName"] == "SG-US-EAST-1"):
                ec2_us_east_1.delete_security_group(GroupName = "SG-US-EAST-1")
                print("            Apagou SG de Virgínia do Norte")
                break
        except:
            print("        Não foi possível apagar o Security Group")

    #apaga security group existente de Virgínia do Norte


    #CRIA NOVO SECURITY GROUP EM VIRGÍNIA DO NORTE
    print("Criando novo SG em Virgínia do Norte")

    try:
        
        resp = ec2_us_east_1.create_security_group(GroupName='SG-US-EAST-1',
                                            Description='SG-US-EAST-1',
                                            VpcId=vpc_id)
        us_east_1_security_group_id = resp['GroupId']
        print(us_east_1_security_group_id)
        print('Security Group Created %s in vpc %s.' % (us_east_1_security_group_id, vpc_id))

        data_in = ec2_us_east_1.authorize_security_group_ingress(
            GroupId=us_east_1_security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 8080,
                'ToPort': 8080,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 5432,
                'ToPort': 5432,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        data_out = ec2_us_east_1.authorize_security_group_egress(
            GroupId=us_east_1_security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 8080,
                'ToPort': 8080,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 5432,
                'ToPort': 5432,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print("Criou SG em Virgínia do Norte")
    except ClientError as e:
        print(e)
    #cria novo security group em Virgínia do Norte

    #CRIA NOVA INSTÂNCIA EM VIRGÍNIA DO NORTE
    print("Criando nova instância em Virgínia do Norte")

    user_data = str("""#cloud-config
    runcmd:
    - cd /home/ubuntu;
    - sudo apt update;
    - sudo apt upgrade -y;
    - sudo apt autoremove -y;
    - sudo apt install python3-pip -y;
    - pip3 install flask requests django psutil mock pytest flake8 tox;
    - git clone https://github.com/raulikeda/tasks;
    - cd tasks;
    - sed -i "s/node1/postgresIP/g" ./portfolio/settings.py;
    - ./install.sh;
    - sudo ufw allow 8080/tcp -y;
    - sudo reboot;
    """)
    user_data = user_data.replace("postgresIP", str(us_east_2_ip))
    print(user_data)

    instances = ec2_resource_us_east_1.create_instances(
        ImageId = 'ami-0279c3b3186e54acd', #Ubuntu Server 18.04 LTS (HVM), SSD Volume Type 64 bits x86
        UserData = user_data,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = 't2.micro',
        KeyName = 'KeyName_us_east_1',
        BlockDeviceMappings = [
            {
                'DeviceName' : "/dev/xvda",
                'Ebs' :{
                    'DeleteOnTermination': True,
                    'VolumeSize': 20
                }
            }
        ],
        SecurityGroups = ['SG-US-EAST-1']

    )
    print("Criou nova instância em Virgínia do Norte")
    #cria nova instância em Virgínia do Norte


    #CONFIGURA A NOVA INSTÂNCIA 
    instance = instances[0]
    print("Aguardando a instância estar rodando")
    instance.wait_until_running()
    instance.load()
    print(instance.public_dns_name)
    public_dns_name: str = "ubuntu@" + instance.public_dns_name
    print(public_dns_name)
    print("PostgreSQL IP")
    print("    ", us_east_2_ip)
    user_data = user_data.replace("postgresIP", str(us_east_2_ip))
    time.sleep(30)
    
    k = paramiko.RSAKey.from_private_key_file("/Users/otofuji/.ssh/KeyName_us_east_1.pem")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print ("connecting")

    c.connect( hostname = instance.public_dns_name, port = 22,  username = "ubuntu", password=None, pkey = k, key_filename = None, timeout=None,  allow_agent=True, look_for_keys=True, compress=False, sock=None, gss_auth=False, gss_kex=False, gss_deleg_creds=True, gss_host=None, banner_timeout=None, auth_timeout=None, gss_trust_dns=True, passphrase=None, disabled_algorithms=None )
    print ("connected")
    time.sleep(10)
    print("CONFIGURANDO")
    c.close()

    setting = True
    while setting:
        try:

            c.connect( hostname = instance.public_dns_name, port = 22,  username = "ubuntu", password=None, pkey = k, key_filename = None, timeout=None,  allow_agent=True, look_for_keys=True, compress=False, sock=None, gss_auth=False, gss_kex=False, gss_deleg_creds=True, gss_host=None, banner_timeout=None, auth_timeout=None, gss_trust_dns=True, passphrase=None, disabled_algorithms=None )
                
            c.close()
        except:
            setting = False
            pass

    print("    Instância configurada ")
    print("        REBOOT - aguarde instância estar no ar novamente")
    print("")
    print("")
    print("")

    time.sleep(21)
    rebooting = True
    while setting:
        try:

            c.connect( hostname = instance.public_dns_name, port = 22,  username = "ubuntu", password=None, pkey = k, key_filename = None, timeout=None,  allow_agent=True, look_for_keys=True, compress=False, sock=None, gss_auth=False, gss_kex=False, gss_deleg_creds=True, gss_host=None, banner_timeout=None, auth_timeout=None, gss_trust_dns=True, passphrase=None, disabled_algorithms=None )
                
            c.close()

            rebooting = False
        except:
            pass
    
    print("            Instância no ar novamente após reinício do sistema - plenamente configurado")
    print("Criando AMI")
    try:
        ami_image = ec2_us_east_1.create_image(
            Name = 'ami-otofuji',
            InstanceId = instance.id,
            NoReboot = False,
            TagSpecifications=[{
                "ResourceType": "image",
                "Tags": [{
                    "Key": "Name",
                    "Value": "DMI"
                }]
            }]
        )

        ec2_us_east_1.get_waiter('image_available').wait(ImageIds=[ami_image['ImageId']])
        ami_new_name = 'ami-otofuji'
        print("    AMI criada")
    except:
        ami_new_name: str = 'ami-otofuji-redundance-' + instance.id
        ami_image = ec2_us_east_1.create_image(
            Name = ami_new_name,
            InstanceId = instance.id,
            NoReboot = False,
            TagSpecifications=[{
                "ResourceType": "image",
                "Tags": [{
                    "Key": "Name",
                    "Value": "DMI"
                }]
            }]
        )

        ec2_us_east_1.get_waiter('image_available').wait(ImageIds=[ami_image['ImageId']])
        print("    AMI criada (redundance mode)")

    return ami_image['ImageId'], instance.id, ami_new_name, us_east_1_security_group_id

def elbv2(ami_id, instance_id, ami_new_name, us_east_1_security_group_id):

    elastic_load_balancer = boto3.client('elbv2', region_name='us-east-1')
    print("Security Group ID: ", us_east_1_security_group_id)
    print("    CRIANDO LOAD BALANCER")

    response = elastic_load_balancer.create_load_balancer(
        Name='otofuji-lb',
        Subnets=[
            'subnet-0f97ba686e75dfb10', 
            'subnet-00baef21b74680367',
            'subnet-01539151d6adb6873',
            'subnet-0408943dc85ec5fdf',
            'subnet-0d396ca117c2dcf56',
            'subnet-09d783f3b388bd35a'
        ],
        
        
        SecurityGroups=[
            us_east_1_security_group_id,
        ],
        #Scheme='internet-facing'|'internal',
        Tags=[
            {
                'Key': 'Name',
                'Value': 'ProjetoCloud'
            },
        ],
        Type='application',
        IpAddressType='ipv4',
        #CustomerOwnedIpv4Pool='string'
    )
    
    print("")
    print("")
    print("RESPONSE LOAD BALANCER")
    print("    ", response)
    print("")
    print("")

    create_tg_response = elastic_load_balancer.create_target_group(Name='target',
                                                        Protocol='TCP',
                                                        Port=8080)

    
    """ autoscaling = boto3.client('autoscaling')
    response = autoscaling.create_launch_configuration(
        LaunchConfigurationName = 'project_lc',
        ImageId = ami_id,
        SecurityGroups = [
            us_east_1_security_group_id
        ],
        InstanceId = instance_id,
        InstanceType = 't2.micro',
        InstanceMonitoring = {
            'Enabled': True
        },
    )

        ##Create auto scaling groups

    response = autoscaling.create_auto_scaling_group(
    AutoScalingGroupName='project_lc',
    LaunchConfigurationName='project_lc',
    MinSize=2,
    MaxSize=6,
    LoadBalancerNames=[
        'projectelb',
    ],
    HealthCheckType='ELB',
    HealthCheckGracePeriod=300,
    VPCZoneIdentifier='subnet-83dd6ade,subnet-28e79963'
    )
    ##Autoscaling Policies
    response = autoscaling.put_scaling_policy(
    AutoScalingGroupName='project_asg',
    PolicyName='HighCPUUtilization',
    AdjustmentType='PercentChangeInCapacity',
    ScalingAdjustment=65,
    Cooldown=60,
    )
    response = client_as.put_scaling_policy(
    AutoScalingGroupName='project_asg',
    PolicyName='LowCPUUtilization',
    AdjustmentType='PercentChangeInCapacity',
    ScalingAdjustment=20,
    Cooldown=60,
    )

        #########CLOUDWATCH METRICS#############
    client_cw = boto3.client('cloudwatch')
    scaledown = client_cw.put_metric_alarm(
        AlarmName='scaledown',
        AlarmDescription='High CPU Utilization',
        ActionsEnabled=True,
        MetricName='CPUUtilization',
        Namespace='ELB',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'i-0bb3fcb4396da630b'
            },
        ],
        Period=60,
        Unit='Seconds',
        EvaluationPeriods=1,
        Threshold=65.0,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
    )


    scaleup = client_cw.put_metric_alarm(
        AlarmName='scaleup',
        AlarmDescription='Low CPU Utilization',
        ActionsEnabled=True,
        MetricName='CPUUtilization',
        Namespace='ELB',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'i-0bb3fcb4396da630b'
            }
        ],
        Period=60,
        Unit='Seconds',
        EvaluationPeriods=2,
        Threshold=20.0,
        ComparisonOperator='LessThanThreshold'   
    )	
	
    response = autoscaling.attach_load_balancers(
        AutoScalingGroupName='project_asg',
        LoadBalancerNames=[
            'projectelb',
        ],
    )
 """


    return None




us_east_2_ip = deploy_us_east_2()

ami_id, instance_id, ami_new_name, us_east_1_security_group_id = deploy_us_east_1(us_east_2_ip)

elbv2(ami_id, instance_id, ami_new_name, us_east_1_security_group_id)
