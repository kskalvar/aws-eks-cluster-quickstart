AWS Elastic Kubernetes Service (EKS) QuickStart  
===============================================

This solution shows how to create an AWS EKS Cluster and deploy a simple web application with an external Load Balancer. This readme updates an article "Getting Started with Amazon EKS" referenced below and provides a more basic step by step process.  Unfortunately this is a pretty manual effort right now.

Steps:  
  Create your Amazon EKS Service Role  
  Create your Amazon EKS Cluster VPC  
  Create your Amazon EKS Cluster  
  Launch and Configure Your Amazon EKS Worker Nodes  
  Configure Your AWS EC2 Instance  
  Configure kubectl on Your EC2 Instance  
  Enable Worker Nodes to Join Your Cluster  
  Deploy WebApp to Your Cluster  
  Remove Your AWS EKS Cluster  


To make this first cluster easy to deploy we'll use a docker image located in DockerHub at kskalvar/web.  This image is nothing more than a simple webapp that returns the current ip address of the container it's running in.  We'll create an external AWS Load Balancer and you should see a unique ip address as it is load balanced across containers.

The project also includes the Dockerfile for those interested in the configuration of the actual application or to build your own and deploy using ECR.


## Create your Amazon EKS Service Role

Use the AWS Console to configure the EKS IAM Role.  This is a step by step process.

### AWS IAM Dashboard
Select Roles  

Click on "Create role"  
Select "AWS Service"  
Choose the service that will use this role  
```
EKS
```  
Click on "Next: Permissions"  
Click on "Next: Review"  
Enter "Role Name"
```
eks-role
```
Click on "Create role"

## Create your Amazon EKS Cluster VPC

Use the AWS CloudFormation to configure the Cluster VPC.  This is a step by step process.

### AWS CloudFormation Console
Click on "Create Stack"  
Select "Specify an Amazon S3 template URL"  
```
https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2018-08-30/amazon-eks-vpc-sample.yaml
```
Click on "Next"  
```
Stack Name: eks-vpc
```
Click on "Next"  
Click on "Next"  
Click on "Create"

Wait for Status CREATE_COMPLETE before proceeding 


## Create your Amazon EKS Cluster

Use the AWS Console to configure the EKS Cluster.  This is a step by step process and should take approximately 10 minutes.

### AWS EKS Dashboard
Click on "Clusters"  

Click on "Create cluster"  
```
Cluster name: eks-cluster
Kubernetes version:  1.10
Role ARN: eks-role
VPC: eks-vpc-VPC
Subnets:  Should preselect all available
Security groups: eks-vpc-ControlPlaneSecurityGroup-*
```

Click on "Create"  

Wait for Status ACTIVE before proceeding

## Launch and Configure Your Amazon EKS Worker Nodes

Use AWS CloudFormation to configure the Worker Nodes.  This is a step by step process.

### AWS CloudFormation Console
Click on "Create Stack"  
Select "Specify an Amazon S3 template URL"  
```
https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2018-08-30/amazon-eks-nodegroup.yaml
```
Click on "Next"  
```
Stack Name: eks-nodegroup
ClusterNamme: eks-cluster
ClusterControlPlaneSecurityGroup: eks-vpc-ControlPlaneSecurityGroup-*
NodeGroupName: eks-nodegroup
NodeImageId: ami-0440e4f6b9713faf6
KeyName: <Your AWS KeyName>
VpcId: eks-vpc-VPC
Subnets: Subnet01, Subnet02, Subnet03
```
Click on "Next"  
Click on "Next"  
Select Check Box "I acknowledge that AWS CloudFormation might create IAM resources"  
Click on "Create"

Wait for Status CREATE_COMPLETE before proceeding  
You should be able to see the additional nodes visible in AWS EC2 Console  

Click on "Outputs" Tab Below
```
Copy NodeInstanceRole Value for use later
```

## Configure Your AWS EC2 Instance

Use AWS Console to configure the EC2 Instance for kubectl.  This is a step by step process.

### AWS EC2 Dashboard  

Click on "Launch Instance"  
Click on "Community AMIs"  
Search community AMIs
```
Amazon Linux AMI 2018.03.0 (HVM), SSD Volume Type - ami-0ff8a91507f77f867 
```  
Click on "Select"

Choose Instance Type
```
t2.micro
```
Click on "Next: Configure Instance Details"  
Click on "Advanced Details
```
User data
Select "As file"
Click on "Choose File" and Select "cloud-init" from project cloud-deployment directory 
```  
Click on "Next: Add Storage"  
Click on "Next" Add Tags"  
Click on "Add Tag"
```
Key: Name
Value: kubectl-console
```
Click on "Next: Configure Security Group"  
Configure Security Group  
Select "Select an existing security group"  
Select "default"  
Click on "Review and Launch"    
Click on "Launch"

## Configure kubectl on Your EC2 Instance

You will need to ssh into the AWS EC2 Instance you created above.  This is a step by step process.

### Check to insure cloud-init has completed

See contents of "/tmp/install-eks-support" it should say "installation complete".


### Configure AWS CLI

aws configure
```
AWS Access Key ID []: <Your Access Key ID>
AWS Secret Access Key []: <Your Secret Access Key>
Default region name []: us-east-1
```

```
NOTE:  There is a script in /home/ec2-user called "configure-kube-control".  You may run this script to automate the  
       creation and population of environment variables in .kube/aws-auth-cm.yaml and .kube/control-kubeconfig.  It
       uses the naming convention I specified in this HOW-TO.  So if you didn't use the naming convention it won't work.
       If you do use the script then all you need to do is run "Test Cluster" and "Test Cluster Nodes" steps.
```

### control-kubeconfig
Gather cluster name, endpoint, and certificate for use below
```
aws eks list-clusters                                                               
aws eks describe-cluster --name eks-cluster --query cluster.endpoint                
aws eks describe-cluster --name eks-cluster  --query cluster.certificateAuthority.data  
```

Copy the control-kubeconfig template from the github project
```
mkdir -p ~/.kube  
cp ~/aws-eks-cluster-quickstart/kube-config/control-kubeconfig.txt ~/.kube/control-kubeconfig 
```

### Edit control-kubeconfig and replace with values above
```
<myendpoint>
<mydata>
<mycluster>
```

### Test Cluster
Using kubectl test the cluster status
```
source ~/.bashrc # To insure you picked up the environment variables
kubectl get svc 
```

## Enable Worker Nodes to Join Your Cluster
You will need to ssh into the AWS EC2 Instance you created above. This is a step by step process.

###  aws-auth-cm.yaml
Copy the aws-auth-cm.yaml template from the github project
```
cp ~/aws-eks-cluster-quickstart/kube-config/aws-auth-cm.yaml.txt ~/.kube/aws-auth-cm.yaml
```

### Edit aws-auth-cm.yaml
Replace <myarn> with NodeInstanceRole from output of CloudFormation script "eks-nodegroup"
```
<myarn>
```

### Test Cluster Nodes
Use kubectl to test status of cluster nodes
```
kubectl apply -f ~/.kube/aws-auth-cm.yaml
kubectl get nodes
```
Wait till you see all nodes appear in "STATUS Ready"


## Deploy WebApp to Your Cluster

You will need to ssh into the AWS EC2 Instance you created above. This is a step by step process.

### Create Pod
Use kubectl to create a single pod
```
kubectl run web --image=kskalvar/web --port=5000
```

### Scale Pod
Use kubectl to scale pod
```
kubectl scale deployment web --replicas=3
```

### Show Pods Running
Use kubectl to display pods
```
kubectl get pods --output wide
```
Wait till you see all pods appear in "STATUS Running"

### Create Load Balancer
Use kubectl to create AWS EC2 LoadBalancer
```
kubectl expose deployment web --port=80 --target-port=5000 --type="LoadBalancer"
```

### Get AWS External Load Balancer Address
Capture EXTERNAL-IP for use below
```
kubectl get service web --output wide
```
Wait till you see "EXTERNAL-IP ```*.<your account>.<region>.elb.amazon.com```" 

### Test from browser
Using your client-side browser enter the following URL
```
http://<EXTERNAL-IP>
```

### Delete Deployment, Service
Use kubectl to delete application
```
kubectl delete deployment,service web
```

## Remove Your AWS EKS Cluster

### AWS CloudFormation
Delete "eks-nodegroup" Stack  
Wait for "eks-nodegroup" to be deleted before proceeding

### AWS EKS
Delete "eks-cluster"  
Wait for cluster to be deleted before proceeding.  Really slow!  

### AWS CloudFormation
Delete "eks-vpc"  
Wait for vpc to be deleted before proceeding

### AWS EC2
Delete "kubectl-console" Instance  
Wait for instance to be deleted before proceeding

### AWS IAM Roles
Delete the following Roles:

```
eks-role  
```
## References
Getting Started with Amazon EKS  
https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html  

Amazon EKS-Optimized AMI  
https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html
