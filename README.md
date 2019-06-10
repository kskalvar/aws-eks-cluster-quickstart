AWS Elastic Kubernetes Service (EKS) QuickStart  
===============================================

This solution shows how to create an AWS EKS Cluster and deploy a simple web application with an external Load Balancer. This readme updates an article "Getting Started with Amazon EKS" referenced below and provides a more basic step by step process.  Unfortunately this is a pretty manual effort right now.

Note:  This how-to assumes you are creating the eks cluster in us-east-1 and you have access to the AWS Root Account

Steps:  

  Configure Your AWS EC2 Instance  
  Create AWS EKS Cluster using AWS CloudFormation  
  Configure kubectl on Your EC2 Instance   
  Deploy WebApp to Your Cluster  
  Configure the Kubernetes Dashboard (optional)
  Remove Your AWS EKS Cluster  


To make this first microservice easy to deploy we'll use a docker image located in DockerHub at kskalvar/web.  This image is nothing more than a simple webapp that returns the current ip address of the container it's running in.  We'll create an external AWS Load Balancer and you should see a unique ip address as it is load balanced across containers.

The project also includes the Dockerfile for those interested in the configuration of the actual application or to build your own and deploy using ECR.


## Configure Your AWS EC2 Instance
Use AWS Console to configure the EC2 Instance for kubectl.  This is a step by step process.

### AWS EC2 Dashboard  
Click on "Launch Instance"  
Click on "Quick Start"  
```
Amazon Linux 2 AMI (HVM), SSD Volume Type - ami-0c6b1d09930fac512 
```  
Click on "Select"

Choose Instance Type
```
t2.micro
```
Click on "Next: Configure Instance Details"  
Expand Advanced Details
```
User data
Select "As text"
Cut and Paste contents of file from "aws-eks-cluster-quickstart/cloud-init/cloud-init" in github 
```  
Click on "Next: Add Storage"  
Click on "Next" Add Tags"  
Click on "Add Tag"
```
Key: Name
Value: kubectl-console
```
Click on "Next: Configure Security Group"  

Click on "Review and Launch"    
Click on "Launch"  
```
Note:  Be sure select an "Choose an existing key pair" or "Create a new key pair"
```

## Create AWS EKS Cluster using AWS CloudFormation 
Use the AWS Console to configure the EKS Cluster.  This is a step by step process.

### AWS CloudFormation Dashboard
Click on "Create Stack"  
Select "Specify an Amazon S3 template URL"  
```
https://998551034662-aws-eks-cluster.s3.amazonaws.com/eks-cluster-demo.json  
```
Click on "Next"  

Specify Details
```
Stack name: eks-cluster-demo
KeyName: <Your AWS KeyName>
```
Click on "Next"  
Click on "Next"  
```
Select "I acknowledge that AWS CloudFormation might create IAM resources with custom names"  
Select "I acknowledge that AWS CloudFormation might require the following capability: CAPABILITY_AUTO_EXPAND"  
```
Click on "Create"  

Wait for Status CREATE_COMPLETE before proceeding  

## Configure kubectl on Your EC2 Instance
You will need to ssh into the AWS EC2 Instance you created above.  This is a step by step process.  

### Connect to EC2 Instance
Using ssh from your local machine, connect to your AWS EC2 Instance
```
ssh -i <AWS EC2 Private Key> ec2-user@<AWS EC2 Instance IP Address>
```

### Check to insure cloud-init has completed
See contents of "/tmp/install-eks-support" it should say "installation complete".

### Configure AWS CLI
aws configure
```
AWS Access Key ID []: <Your Access Key ID>
AWS Secret Access Key []: <Your Secret Access Key>
Default region name []: us-east-1
```
Test aws cli
```
aws s3 ls
```

### Configure kubectl
Configure kubectl to access the cluster
```
NOTE:  There is a script in /home/ec2-user called "configure-kube-control".  
       You may run this script to automate the creation and population of environment 
       variables in .kube/aws-auth-cm.yaml and .kube/control-kubeconfig.  It
       uses the naming convention I specified in this HOW-TO.  So if you didn't
       use the naming convention it won't work.  If you do use the script then all
       you need to do is run the "Test Cluster" and "Test Cluster Nodes" steps.
       
./configure-kube-control
```

### Test Cluster
Using kubectl test the cluster status
```
source ~/.bashrc # To insure you picked up the environment variables
kubectl get svc 
```
### Test Cluster Nodes
Use kubectl to test status of cluster nodes
```
source ~/.bashrc # To insure you picked up the environment variables
kubectl get nodes
```
Wait till you see all nodes appear in "STATUS Ready"


## Deploy WebApp to Your Cluster
You will need to ssh into the AWS EC2 Instance you created above. This is a step by step process.

### Deploy Web App
Use kubectl to create a single pod
```
kubectl apply -f ~/aws-eks-cluster-quickstart/scripts/web-deployment-service.yaml
```

### Show Pods Running
Use kubectl to display pods
```
kubectl get pods --output wide
```
Wait till you see all pods appear in "STATUS Running"

### Get AWS External Load Balancer Address
Capture EXTERNAL-IP for use below
```
kubectl get service web --output wide
```

### Test from browser
Using your client-side browser enter the following URL
```
http://<EXTERNAL-IP>
```

### Delete Deployment, Service
Use kubectl to delete application
```
kubectl delete -f ~/aws-eks-cluster-quickstart/scripts/web-deployment-service.yaml
```

## Configure the Kubernetes Dashboard (optional)
You will need to configure the dashboard from the AWS EC2 Instance you created as well as use ssh to create a tunnel on port 8001 from your local machine.  This is a step by step process.

### configure-kube-dashboard
Configure Kubernetes Dashboard 
```
NOTE:  There is a script in /home/ec2-user called "configure-kube-dashboard".  
       You may run this script to automate the installation of the dashboard components into the cluster,
       configure the service role, and start the kubectl proxy.
       
./configure-kube-dashboard
```

### Connect to EC2 Instance redirecting port 8001 Locally
Using ssh from your local machine, open a tunnel to your AWS EC2 Instance
```
ssh -i <AWS EC2 Private Key> ec2-user@<AWS EC2 Instance IP Address> -L 8001:localhost:8001
```

### Test from Local Browser
Using your local client-side browser enter the following URL. The configure-kube-dashboard script
also generated a "Security Token" required to login to the dashboard.
```
http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/
```

## Remove Your AWS EKS Cluster
Before proceeding be sure you delete deployment,service web as instructed above.  Failure to do so will cause cloudformation
script to fail.

### AWS CloudFormation
Delete "eks-cluster-demo" Stack  

### AWS EC2
Delete "kubectl-console" Instance  

## References
Getting Started with Amazon EKS  
https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html  

Amazon EKS-Optimized AMI  
https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html
