import boto3
import botocore.exceptions
import argparse
from simple_term_menu import TerminalMenu


if __name__ == "__main__":
    # Get parameters
    parser = argparse.ArgumentParser(description='''
                                      Return a list of AWS ECS clusters and  
                                      tasks for easy shell connection to container\n
                                      ''')
    parser.add_argument('--aws-profile',
                        help='Specify amazon profile to use. Uses default profile if not specified',
                        default=None,
                        dest='profile')
    args = parser.parse_args()



    print("Wibble")
