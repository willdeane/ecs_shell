# ecs_shell
Menu-driven script for running shell on AWS ECS containers using the AWS 
[ECS Exec for debugging](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-exec.html) tooling. 
Scripts enumerates ECS clusters, services, tasks and containers and then presents an easy-to-use menu to select the 
cluster --> service --> container to open an interactive shell on. 

## Usage
```shell
python ecs_shell --profile [aws profile]
```
If not profile is specified it uses the default configured aws profile. 
## Requirements
Runs on linux or mac. It can only be used on Windows within a linux WSL environment as `simple-term-menu` 
is not supported on Windows.

As well as the python dependencies, the following must be installed and configured:
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-environment.html)
* [Session Manager plugin for AWS CLI](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)

The `enable-execute-command` flag must be set on ECS Services/Tasks. 