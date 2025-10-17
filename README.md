# Batfish DashBoard

 First, I want to say thank you to the Batfish team from making such a great tool!
 
 This dashboard wraps a few features from the tool [Batfish](www.batfish.org) in a "pretty" GUI.

## Quick Start

### Prerequisites
- Download and run [batfish](https://pybatfish.readthedocs.io/en/latest/getting_started.html):
    ```bash
    docker pull batfish/allinone
    docker run --name batfish -v batfish-data:/data -p 8888:8888 -p 9997:9997 -p 9996:9996 batfish/allinone
    ```

### Deployment Options

This modernized dashboard can be deployed in multiple ways to connect to your existing Docker network:

#### Option 1: Docker Compose (Recommended)
```bash
# Simple deployment with automatic network connection
docker-compose up --build -d

# Or use the deployment script
./deploy.sh compose    # Linux/Mac
deploy.bat compose     # Windows
```

#### Option 2: Direct Docker Commands
```bash
# Connect to existing network 'myNetwork'
docker build -t batfish_dashboard .
docker run -d --name batfish_dashboard --network myNetwork -p 8050:8050 batfish_dashboard

# Or use the deployment script
./deploy.sh docker    # Linux/Mac
deploy.bat docker     # Windows
```

#### Option 3: Standalone (Original Method)
```bash
# Basic deployment without specific network
docker build -t batfish_dashboard . && docker run -p 8050:8050 batfish_dashboard
```

### Access the Dashboard
- **Local access**: http://localhost:8050
- **Remote access**: http://[your-server-ip]:8050

### Management Commands
```bash
# Check deployment status
./deploy.sh status

# Clean up deployment
./deploy.sh cleanup

# View logs
docker-compose logs -f batfish-dashboard  # If using compose
docker logs -f batfish_dashboard          # If using direct docker
```

### Network Configuration
The dashboard automatically connects to the `myNetwork` Docker network. If this network doesn't exist, the deployment scripts will create it automatically.

Enjoy your modernized Batfish Dashboard! 🎉

## Features

### Graphs

##### Layer 3 Graph

<img src="/assets/img/Layer_3_Graph.PNG" width="1000" />


##### OSPF Graph

<img src="/assets/img/Ospf_graph.PNG" width="1000" />

##### BGP Graph

<img src="/assets/img/BGP_graph.PNG" width="1000" />

### Ask a Question

<img src="/assets/img/Ask_a_question.PNG" width="1000" />

### Trace Route

<img src="/assets/img/trace_routev2.PNG" width="1000" />

### Refactor ACLs

<img src="/assets/img/ACL_refractored.PNG" width="1000" />

## Roadmap

* Chaos Monkey
* Ask a Question advanced search
* ACL Tester
