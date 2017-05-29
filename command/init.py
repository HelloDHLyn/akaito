import json
import os
import subprocess

import boto3

from command.common import Colors

TABLE_NAME = 'Akaito'
FUNCTION_JSON_DATA = {
    'runtime': 'python3.6',
    'handler': 'main.handle',
    'description': 'Check if the server is alive. (Added by Akaito)',
    'environment': {}
}


def check_credential():
    """
    Check if credential exists.
    :return: 
    """
    session = boto3.session.Session()
    if not session.get_credentials():
        exit('[FAILED] No credential available.')


def set_configs():
    chatbot_token = input('Chatbot Token: ')
    chat_id = input('Chatroom ID: ')

    FUNCTION_JSON_DATA['environment']['CHATBOT_URL'] = f"https://api.telegram.org/bot{chatbot_token}"
    FUNCTION_JSON_DATA['environment']['CHAT_ID'] = chat_id

    with open('./functions/alive_check/function.json', 'w') as f:
        json.dump(FUNCTION_JSON_DATA, f, indent=4)


def apex_init():
    try:
        # Initialize.
        subprocess.run(['apex', 'init'])
    except OSError as e:
        # If Apex doesn't exist.
        if e.errno == os.errno.ENOENT:
            exit('[FAILED] Akaito needs Apex. Please install Apex first.')
        else:
            raise


def apex_deploy():
    subprocess.run(['apex', 'deploy', 'akaito_alive_check'])


def command():
    check_credential()

    set_configs()

    # apex_init()
    # apex_deploy()

    print(f"""
    {Colors.BOLD}COMPLETED!{Colors.ENDC} Type \'akaito add\' to set your first akaito connection.
    """)
