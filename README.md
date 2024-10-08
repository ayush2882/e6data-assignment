# e6data-assignment

1. Running the Flask app locally
	
It returns the Pod’s IP as the 127.0.0.1 as we are running it locally on localhost.

2. Created a Dockerfile for the Flask-app, Built the image and ran it as a container.
	
Now’s while hitting the IP - 127.0.0.1/5000/ip → We get the Container’s IP as the Pod_IP address - 172.17.0.2

Finding the Container’s IP - docker inspect d553cc2053d73de3d5161f14b0ca8cf07e09b409164937c1a5f5a85aae1fc68b | grep "IPAddress"

            "SecondaryIPAddresses": null,
            "IPAddress": "172.17.0.2",
                    "IPAddress": "172.17.0.2",
We can also get the response with a curl command from terminal - 
`curl http://localhost:5000/ip
{"pod_ip":"172.17.0.2"}`

Deploying the App to Kubernetes:

Components Created: 
A) Deployment for Flask app - `kubectl create -f flask-deployment.yaml`
B) Load Balancer service to expose the app externally - `kubectl create -f flask-service.yaml`
C) Setup HPA for High availability - `kubectl autoscale deployment flask-deployment --cpu-percent=50 --min=3 --max=10`. We can also scale the replicas of the deployment to Scale the number of pods serving the application.
C) Ingress Controller and Ingress Resource - Setup the nginx ingress controller via official Helm chart for Nginx Ingress deployment. Then deployed ingress resource - kubectl apply -f flask-ingress.yaml
D) Nginx Deployment, Service, Config Map - `kubectl create -f nginx-config.yaml`, `kubectl create -f nginx-deployment.yaml`, `kubectl create -f nginx-service.yaml`

3. Testing the flask service - 

Get the service external IP - `kubectl get svc flask-service`

`curl a4579d893385d4ceab258a374190c423-1319051632.ap-south-1.elb.amazonaws.com/ip
{"pod_ip":"172.31.26.104"}`

4. Testing via Ingress Controller and Resource - 

Get the external IP for Load balancer created as part of Ingress controller setup - `kubectl get svc | grep ingress `

`curl adc1147eb6777484ca12c5897667026f-846301740.ap-south-1.elb.amazonaws.com/ip
{"pod_ip":"172.31.19.129"}`

5. Testing the app via nginx reverse proxy - 

Get the external IP  - `kubectl get svc nginx-service`

`curl http://ad78f279033e746a480ff92529def6ff-1653859855.ap-south-1.elb.amazonaws.com/ip
{"pod_ip":"172.31.21.76"}`

6. I ran jenkins in a docker container. Installed Kubernetes CLI plugin, Docker, Dockerpipeline, Git, etc plugins to enable Jenkins to interact with different components.
Stored the kubeconfig file as a Jenkins credenetials. Also, added a token for Jenkins to access Github.
Then created a pipeline which is checking out the code from the repo. Then it will build the image and push it to dockerhub. Then in the next stage the flask application will be deployed on EKS cluster with the manifest files from the Git Repo.
