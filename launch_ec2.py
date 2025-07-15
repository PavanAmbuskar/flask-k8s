import boto3

# Create EC2 resource in us-east-1
ec2 = boto3.resource('ec2', region_name='us-east-1')

# User data script for Ubuntu 22.04
user_data_script = """#!/bin/bash
# Wait for apt lock
while fuser /var/lib/dpkg/lock-frontend >/dev/null 2>&1; do
   sleep 5
done
# Update and install Docker + Git
apt-get update -y
apt-get install -y docker.io git
# Start and enable Docker
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu
# Clone Flask project
cd /home/ubuntu
git clone https://github.com/PavanAmbuskar/flask.git
cd flask
# Build and run the Docker container
docker build -t flask-app-3 .
docker run -d -p 5000:5000 --name my-flask-container flask-app-3
"""

# Launch EC2 instance
instances = ec2.create_instances(
    ImageId='ami-020cba7c55df1f615',  # Ubuntu 22.04 LTS
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='my-server',  # Make sure this key pair exists in us-east-1
 SecurityGroupIds=['sg-04e73bbda715725b5'],  # Ensure port 22 & 5000 open
    UserData=user_data_script,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'flask-docker-instance'}]
        }
    ]
)

# Wait for the instance to be running
instances[0].wait_until_running()

# Reload instance to fetch public IP
instances[0].reload()

print(f"Launched EC2 Instance ID: {instances[0].id}")
print(f"Public IP: {instances[0].public_ip_address}")
