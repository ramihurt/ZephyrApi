import configparser
import hashlib
import json
import sys
import time
import jwt
import requests
from urllib.parse import urlencode
from pydantic import ValidationError
from dto import Cycle
from TestCaseStatus import Status



config = configparser.ConfigParser()
config.read('../environment.ini')
# ACCOUNT ID
ACCOUNT_ID = config["zephyr.api"]["account_id"]

# ACCESS KEY from navigation >> Tests >> API Keys
ACCESS_KEY = config["global"]["access_key"]

# ACCESS KEY from navigation >> Tests >> API Keys
SECRET_KEY = config["global"]["secret_key"]

# JWT EXPIRE how long token been to be active? 3600 == 1 hour
JWT_EXPIRE = 3600

# BASE URL for Zephyr for Jira Cloud
BASE_URL = 'https://prod-api.zephyr4jiracloud.com/connect'


def is_valid_json(json_string: str):
    try:
        json.loads(json_string)
        return True
    except json.JSONDecodeError:
        return False

def get_list_of_folders(version_id: int, cycle_id: str, project_id: int,
                        expand: str = "executionSummaries,folderSummaries"):
    # RELATIVE PATH for token generation and make request to api
    relative_path = f'/public/rest/api/1.0/folders'
    # CANONICAL PATH (Http Method & Relative Path & Query String)
    canonical_path = f'GET&' + relative_path + f'&cycleId={cycle_id}&projectId={project_id}&versionId={version_id}'

    zephyr_jwt = generate_jwt(canonical_path=canonical_path)

    headers = {
        'Authorization': 'JWT ' + zephyr_jwt,
        'Content-Type': 'text/plain',
        'zapiAccessKey': config["global"]["access_key"]
    }

    payload = {"versionId": version_id, "projectId": project_id, "cycleId": cycle_id}

    response = requests.get(config["zephyr.api"]["prod_base_url"] + relative_path, headers=headers, params=payload)
    return response.text

def get_cycle(version_id: int, cycle_id: str, project_id: int, expand: str = "executionSummaries,folderSummaries"):
    """
    Returns all information pertaining to a given cycle.
    :param version_id:
    :param expand:
    :param cycle_id:
    :param project_id:
    :return:
    """
    # RELATIVE PATH for token generation and make request to api
    relative_path = f'/public/rest/api/1.0/cycle/{cycle_id}'
    # CANONICAL PATH (Http Method & Relative Path & Query String)
    canonical_path = f'GET&' + relative_path + f'&cycleId={cycle_id}&projectId={project_id}&versionId={version_id}'
    zephyr_jwt = generate_jwt(canonical_path=canonical_path)

    headers = {
        'Authorization': 'JWT ' + zephyr_jwt,
        'Content-Type': 'text/plain',
        'zapiAccessKey': config["global"]["access_key"]
    }

    payload = {"versionId": version_id, "projectId": project_id, "cycleId": cycle_id}

    response = requests.get(config["zephyr.api"]["prod_base_url"] + relative_path, headers=headers, params=payload)
    return response.text

def get_list_of_cycles(version_id: int, project_id: int, expand: str = "executionSummaries"):
    relative_path = f'/public/rest/api/1.0/cycles/search'
    query_params = {"versionId": version_id, "expand": expand, "projectId": project_id}
    canonical_query = urlencode(sorted(query_params.items()))
    canonical_request = f"GET&{relative_path}&{canonical_query}"
    zephyr_jwt = generate_jwt(canonical_path=canonical_request)

    headers = {
        'Authorization': 'JWT ' + zephyr_jwt,
        'Content-Type': 'text/plain',
        'zapiAccessKey': config["global"]["access_key"]
    }
    response = requests.get(config["zephyr.api"]["prod_base_url"] + relative_path, headers=headers, params=query_params)
    return response.text

def get_list_of_executions(issue_id:int, offset:int, size:int, project_id:int):
    """
    Currently not working. Getting an error that the qsh value is not correct even though we are using the same
    method of JWT generation as the other API endpoints.
    :param issue_id:
    :param offset:
    :param size:
    :param project_id:
    :return:
    """
    # RELATIVE PATH for token generation and make request to api
    relative_path = f'/public/rest/api/1.0/executions'
    # CANONICAL PATH (Http Method & Relative Path & Query String)
    canonical_path = f'GET&' + relative_path + f'&issueId={issue_id}&projectId={project_id}'
    zephyr_jwt = generate_jwt(canonical_path=canonical_path)

    headers = {
        'Authorization': 'JWT ' + zephyr_jwt,
        'Content-Type': 'text/plain',
        'zapiAccessKey': config["global"]["access_key"]
    }

    payload = {"projectId": project_id, "issueId": issue_id}

    response = requests.get(url=config["zephyr.api"]["prod_base_url"] + relative_path, headers=headers, params=payload)
    return response.text

def update_execution(executionId: str, issue_id:int, project_id:int, cycle_id:str, status: int, comment:str, userKey:str):
    # RELATIVE PATH for token generation and make request to api
    relative_path = f'/public/rest/api/1.0/execution/{executionId}'
    # CANONICAL PATH (Http Method & Relative Path & Query String)
    canonical_path = f'PUT&' + relative_path
    zephyr_jwt = generate_jwt(canonical_path=canonical_path)
    json_body = {
        "status": {"id": status},
        "id": executionId,
        "projectId": project_id,
        "issueId": issue_id,
        "cycleId": cycle_id,
        "versionId": -1,
        "comment": comment,
        "defects": "",
        "assigneeType": "currentUser/assignee",
        "assignee": userKey
    }

    headers = {
        'Authorization': 'JWT ' + zephyr_jwt,
        'Content-Type': 'text/plain',
        'zapiAccessKey': config["global"]["access_key"]
    }

    response = requests.put(url=config["zephyr.api"]["prod_base_url"] + relative_path, headers=headers, json=json_body)
    return response.status_code

def get_zql_field_values():
    # RELATIVE PATH for token generation and make request to api
    relative_path = f'/public/rest/api/1.0/zql/fields/values'
    query_params = {}
    canonical_query = urlencode(sorted(query_params.items()))
    # CANONICAL PATH (Http Method & Relative Path & Query String)
    canonical_path = f'GET&{relative_path}&{canonical_query}'

    zephyr_jwt = generate_jwt(canonical_path=canonical_path)

    headers = {
        'Authorization': 'JWT ' + zephyr_jwt,
        'Content-Type': 'application/json',
        'zapiAccessKey': config["global"]["access_key"]
    }

    response = requests.get(config["zephyr.api"]["prod_base_url"] + relative_path, headers=headers)
    return response.text

def get_execution_navigation_result(project: str, cycle_name: str):
    relative_path = f'/public/rest/api/1.0/zql/search'
    query_params = {"isAdvanced": 0}
    canonical_query = urlencode(sorted(query_params.items()))
    canonical_path = f'POST&{relative_path}&{canonical_query}'
    zephyr_jwt = generate_jwt(canonical_path=canonical_path)

    headers = {
        'Authorization': 'JWT ' + zephyr_jwt,
        'Content-Type': 'application/json',
        'zapiAccessKey': config["global"]["access_key"]
    }

    json_body = {"zqlQuery":"project = '" + project + "' AND cycleName = '"+cycle_name+"'"}
    response = requests.post(config["zephyr.api"]["prod_base_url"] + relative_path, headers=headers, json=json_body, params=query_params)
    response_data = response.json()
    # print(response_data)

    if hasattr(response_data, 'errorType'):
        print("Encountered an error getting cycle data")
        print(response_data["clientMessage"])
        sys.exit(1)

    try:
        search_results = Cycle.Cycle(searchObjectList=response_data["searchObjectList"],summaryList=response_data["summaryList"],
                                     totalCount=response_data["totalCount"], currentOffset=response_data["currentOffset"],
                                     maxAllowed=response_data["maxAllowed"], maxAllowedforSelect=response_data["maxAllowedforSelect"],
                                     sortBy=response_data["sortBy"], sortOrder=response_data["sortOrder"], executionStatus=response_data["executionStatus"],
                                     stepExecutionStatus=response_data["stepExecutionStatus"])
    except ValidationError as exc:
        print("ERROR: " + repr(exc.errors()[0]['type']))
        print(exc)
        sys.exit()

    return search_results
    # data_dict = dacite.from_dict(data_class=SearchObjectList, data=response.json(), config=Config(strict=False, check_types=True))
    # return data_dict

def generate_jwt(canonical_path: str):
    """
    Generates the JWT token for authenticating with the Zephyr API. Account ID, access key, and JWT expiration are
        automatically filled from the environment variables.
    :param canonical_path: Needs to be formatted as <METHOD> + relative_path + query params.
        Ex. Relative path is /public/rest/api/1.0/cycle/{cycle_id} which is then used in the final canonical path as
        "'GET&' + relative_path + f'&cycleId={cycle_id}&projectId={project_id}&versionId={version_id}"
    :return: JWT token string
    :raises ValueError: jwt_expire value from environment.ini could not be converted from string to int
    """
    try:
        payload_token = {
            'sub': config["zephyr.api"]["account_id"],
            'qsh': hashlib.sha256(canonical_path.encode('utf-8')).hexdigest(),
            'iss': config["global"]["access_key"],
            'exp': int(time.time()) + int(config["zephyr.api"]["jwt_expire"]),
            'iat': int(time.time())
        }
    except ValueError:
        print("Could not convert JWT expiration time from a string to int. Check environment variables.")
        sys.exit()

    return jwt.encode(payload_token, config["global"]["secret_key"], algorithm='HS256')

print("Get project information for TSN")
cycle = get_execution_navigation_result(project='test-sample-name', cycle_name='test-cycle-name')
matching_cases = [tc for tc in cycle.searchObjectList or [] if tc.issueKey == "TSN-1"]
test_case = matching_cases[0]
test_case_execution = test_case.execution
print (test_case_execution.id)
execution_status = Status.PASS.value
print(update_execution(executionId=test_case_execution.id,issue_id=test_case_execution.issueId,
                       project_id=test_case_execution.projectId,cycle_id=test_case_execution.cycleId,
                       status=execution_status,comment="test",userKey=config["zephyr.api"]["account_id"]))
