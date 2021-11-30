#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Este script é uma dependência de main.py. Para documentação, veja o main.py.


#IMPORTS
import boto3
from botocore.exceptions import ClientError
import time
#imports

 
#VARIÁVEIS GLOBAIS
finishing = False
#variáveis globais


#CLIENTE E RECURSO
ec2_us_east_2 = boto3.client('ec2', region_name = 'us-east-2')
ec2_resource_us_east_2 = boto3.resource('ec2', region_name = 'us-east-2')
#cliente e recurso




#APAGA INSTÂNCIAS DE OHIO
finishing = False
instances = ec2_us_east_2.describe_instances()
instances_amount = len(instances['Reservations'])
print("Instâncias existentes em Ohio")
print("    ", instances_amount)
existing_SG = ec2_us_east_2.describe_security_groups()['SecurityGroups']
SG_amount = len(existing_SG)
for i in range(instances_amount):
    print("Instâncias em Ohio")
    try:
        print("    Tentando apagar instâncias em Ohio")
        instances_SG = instances['Reservations'][i]['Instances'][0]['NetworkInterfaces'][0]['Groups'][0]['GroupName']
        if instances_SG == 'SG-US-EAST-2':
            instance_id = instances['Reservations'][i]['Instances'][0]['InstanceId']
            ec2_us_east_2.terminate_instances(InstanceIds = [instance_id])
            finishing = True
            print("        Apagando uma instância em Ohio")
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
                print("            Aguarde o término da instância em Ohio")
        except:
            pass
    time.sleep(5)
print("        Terminou instâncias em Ohio")

#apaga instâncias de Ohio


#APAGA SECURITY GROUP EXISTENTE DE OHIO
print("Apagando SG-US-EAST-2")
existing_SG = ec2_us_east_2.describe_vpcs()
vpc_id = existing_SG.get('Vpcs', [{}])[0].get('VpcId', '')
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

    data = ec2_us_east_2.authorize_security_group_ingress(
        GroupId=us_east_2_security_group_id,
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
    print("Criou SG em Ohio")
except ClientError as e:
    print(e)
#cria novo security group em Ohio

#CRIA NOVA INSTÂNCIA EM OHIO
print("Criando nova instância em Ohio")
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
                'DeleteOnTermination': True,
                'VolumeSize': 20
            }
        }
    ],
    SecurityGroups = ['SG-US-EAST-2']

)
print("Criou nova instância em Ohio")
#cria nova instância em Ohio

