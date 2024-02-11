import argparse
import boto3
import subprocess
import sys
from simple_term_menu import TerminalMenu
from aws_functions import (
    get_aws_session,
    get_ecs_clusters,
    get_ecs_tasks,
    get_ecs_containers,
    get_ecs_services,
)


def execute_aws_ecs_exec_command(
    ecs_cluster: str, task: str, container_name: str, profile_name: str
):
    region = ecs_cluster.split(":")[3]
    ecs_execute_command = (
        f"aws ecs execute-command "
        f"--interactive --region {region} "
        f"--cluster {ecs_cluster} "
        f"--task {task} "
        f"--container {container_name} "
        f"--command '/bin/sh' "
        f"--profile {profile_name}"
    )
    print(ecs_execute_command)
    try:
        subprocess.run(ecs_execute_command, shell=True)
    except subprocess.SubprocessError as err:
        print(err)
    main()


def cluster_menu(ecs_client: boto3, ecs_clusters: dict):
    if ecs_clusters:
        options = list(ecs_clusters.keys())
        options.append("Exit")
        terminal_menu = TerminalMenu(options, title="Select ECS Cluster")
        menu_entry_index = terminal_menu.show()
        if options[menu_entry_index] == "Exit":
            sys.exit(0)
        selected_cluster_name = options[menu_entry_index]
        selected_cluster_arn = ecs_clusters[selected_cluster_name]
        services = get_ecs_services(ecs_client, selected_cluster_arn)
        services_menu(ecs_client, selected_cluster_arn, services)
    else:
        print("No clusters found!")


def services_menu(ecs_client: boto3, ecs_cluster: str, ecs_services: dict):
    print(ecs_services)
    if ecs_services:
        options = list(ecs_services.keys())
        options.append("Exit")
        terminal_menu = TerminalMenu(options, title="Select ECS Service")
        menu_entry_index = terminal_menu.show()
        if options[menu_entry_index] == "Exit":
            sys.exit(0)
        selected_service_name = options[menu_entry_index]
        selected_service_arn = ecs_services[selected_service_name]
        tasks = get_ecs_tasks(ecs_client, ecs_cluster, selected_service_arn)
        container_menu(ecs_client, ecs_cluster, tasks)
    else:
        print("No Services found!")


def container_menu(ecs_client: boto3, ecs_cluster: str, ecs_tasks: list):
    service_containers = {}
    for task in ecs_tasks:
        task_containers = get_ecs_containers(ecs_client, ecs_cluster, task)
        for k, v in task_containers.items():
            service_containers[k] = v
    if service_containers:
        options = list(service_containers.keys())
        options.append("Exit")
        terminal_menu = TerminalMenu(options, title="Select Container")
        menu_entry_index = terminal_menu.show()
        if options[menu_entry_index] == "Exit":
            sys.exit(0)
        selected_container_name = options[menu_entry_index]
        selected_container_task = service_containers[selected_container_name]
        execute_aws_ecs_exec_command(
            ecs_cluster, selected_container_task, selected_container_name, args.profile
        )
    else:
        print("No Services found!")


def main():
    # Setup AWS Session
    client = get_aws_session(args.profile)

    # Get cluster details
    clusters = get_ecs_clusters(client)

    # Call Cluster top level menu
    cluster_menu(client, clusters)


if __name__ == "__main__":
    # Get parameters
    parser = argparse.ArgumentParser(
        description="""
                                      Return a list of AWS ECS clusters, services and  
                                      tasks for easy shell connection to containers using
                                      ecs execute-command.\n
                                      """
    )
    parser.add_argument(
        "--profile",
        help="Specify aws profile to use. Uses default profile if not specified",
        default="default",
        dest="profile",
    )

    args = parser.parse_args()

    main()
