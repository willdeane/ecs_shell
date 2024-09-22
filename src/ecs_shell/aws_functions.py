import boto3
import botocore.exceptions


def get_aws_session(profile: str) -> boto3.session:
    """
    Setup boto3 session for ECS, using specified profile
    """
    try:
        session = boto3.Session(profile_name=profile)
        ecs_client = session.client("ecs")

    except botocore.exceptions.ClientError as err:
        print(
            f"Error when processing request for profile {profile}: {err.response['Error']['Message']}"
        )
        raise SystemExit(1)
    except botocore.exceptions.ProfileNotFound:
        print(f"Profile {profile} not found")
        raise SystemExit(1)
    return ecs_client


def get_ecs_clusters(ecs_client: boto3) -> dict:
    """
    Get ECS cluster names and arns - returns dict of name : arn
    """
    try:
        response = ecs_client.list_clusters()
        ecs_clusters = {}
        cluster_arns = response["clusterArns"]
        for arn in cluster_arns:
            name = arn.split("/")[1]
            ecs_clusters[name] = arn
        return ecs_clusters
    except botocore.exceptions.ClientError as err:
        print(
            f"Error when requesting  cluster details: {err.response['Error']['Message']}"
        )
        raise SystemExit(1)


def get_ecs_services(ecs_client: boto3, cluster_arn: str) -> dict:
    """
    Get ECS cluster services and arns - returns dict {'cluster arn' : { 'service name' : arn} }
    """
    try:
        response = ecs_client.list_services(cluster=cluster_arn, maxResults=100)
        cluster_services = {}
        service_arns = response["serviceArns"]
        for arn in service_arns:
            name = arn.split("/")[-1]
            cluster_services[name] = arn
        return cluster_services
    except botocore.exceptions.ClientError as err:
        print(
            f"Error when requesting  cluster details: {err.response['Error']['Message']}"
        )
        raise SystemExit(1)


def get_ecs_tasks(ecs_client: boto3, cluster_arn: str, service_arn: str) -> list:
    """
    Get ECS tasks for the specified cluster and service  - returns list of task arns
    """
    try:
        response = ecs_client.list_tasks(
            cluster=cluster_arn, maxResults=100, serviceName=service_arn
        )
        task_arns = response["taskArns"]
        return task_arns
    except botocore.exceptions.ClientError as err:
        print(
            f"Error when requesting  cluster details: {err.response['Error']['Message']}"
        )
        raise SystemExit(1)


def get_ecs_containers(ecs_client: boto3, cluster_arn: str, task_arn: str) -> dict:
    """
    Get ECS running containers for the specified ecs task  - returns dict {container_name : task_arn}
    """
    containers = {}
    try:
        task = [task_arn]
        response = ecs_client.describe_tasks(cluster=cluster_arn, tasks=task)
        for container in response["tasks"][0]["containers"]:
            if container["lastStatus"] == "RUNNING":
                containers[container["name"]] = task_arn

        return containers
    except botocore.exceptions.ClientError as err:
        print(
            f"Error when requesting  cluster details: {err.response['Error']['Message']}"
        )
        raise SystemExit(1)
