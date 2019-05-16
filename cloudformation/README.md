AWS Elastic Kubernetes Service (EKS) QuickStart  
===============================================

This solution shows how to create an AWS EKS Cluster using AWS CloudFormation.
Note:  This how-to assumes you are creating the eks cluster in us-east-1

Steps:  
  Create AWS EKS Cluster using AWS CloudFormation  

## Create AWS EKS Cluster using AWS CloudFormation 
Use the AWS Console to configure the EKS IAM Role.  This is a step by step process.

### AWS CloudFormation Dashboard
Click on "Create Stack"  
Select "Specify an Amazon S3 template URL"  
```
https://s3.amazonaws.com/998551034662-aws-eks-cluster/eks-cluster-demo.json  
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
