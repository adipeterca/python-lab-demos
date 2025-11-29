import os
import docker
import json
from shared import LAB_NAME

def create_submission_path(author: str):
    '''
    Searches for a suitable local filepath for a submission.
    '''

    counter = 1
    while os.path.exists(f"{LAB_NAME}/submissions/{author}_{counter}.py"):
        counter += 1
    return f"{LAB_NAME}/submissions/{author}_{counter}.py"

def create_score_path():

    counter = 1
    while os.path.exists(f"{LAB_NAME}/scores_{counter}.txt"):
        counter += 1
    return f"{LAB_NAME}/scores_{counter}.txt"

def create_folder_structure():
    
    setup_complete = True

    lab_folder_path = f"./{LAB_NAME}"
    submissions_path = f"{lab_folder_path}/submissions"
    tester_path = f"{lab_folder_path}/tester.py"
    
    if not (os.path.exists(lab_folder_path) and os.path.isdir(lab_folder_path)):
        os.mkdir(lab_folder_path)
        print(f"[WARNING] Folder path {lab_folder_path} did not exist, but I created it for you")
        setup_complete = False
    
    if not (os.path.exists(submissions_path) and os.path.isdir(submissions_path)):
        os.mkdir(submissions_path)
        print(f"[WARNING] Folder path {submissions_path} did not exist, but I created it for you")
        setup_complete = False

    if not (os.path.exists(tester_path) and os.path.isfile(tester_path)):
        with open(tester_path, "w") as fout:
            with open("tester_template.py", "r") as fin:
                content = fin.read()
                fout.write(content)
        
        print(f"[WARNING] Tester path {tester_path} did not exist, but I created it for you")
        setup_complete = False

    if not setup_complete:
        print("[ERROR] The setup wasn't complete, but now it is. Rerun the bot please!")
        exit(1)
        

def run_submission(path: str) -> dict:
    '''
    Given the path to a submission, run it in docker and return a JSON object:\n
    {
        "test_logs": ["Output from the submission script itself. useful for end-user debugging"], 
        "errors": ["Fatal problems from the script itself and also from the container"], 
        "score": "an integer value representing the total points for this problem. Maximum value is 10, minimum is 0."
    }
    '''

    client = docker.from_env()
    
    # Limit CPU usage
    cpus = 0.1
    cpu_period = 100_000  # default in Docker
    cpu_quota = int(cpus * cpu_period)

    container = client.containers.create(
        image="python:3.11-slim",
        command=["python", "/tester.py"],
        volumes={
            os.path.abspath(path) : { "bind" : "/usercode.py", "mode" : "ro" },
            os.path.abspath(f"{LAB_NAME}/tester.py") : { "bind" : "/tester.py", "mode" : "ro"}
        },
        cpu_period=cpu_period,
        cpu_quota=cpu_quota,
        network_disabled=True,
        detach=True
    )


    try:
        result_dict = None

        container.start()

        try:
            container.wait(timeout=5)
        except Exception as e:
            print(f"[DEBUG] Just got exception {e} from container timeout")
            return {"errors" : [], "test_logs" : [":stopwatch: Script timeout"], "score" : 0}

        # Ignore the first part of the logs as they are 
        # the output from the script send by the student.
        logs = container.logs().decode()
        print(f"[DEBUG] logs collected from container: {logs}")
        logs = logs.split("JSON-DELIMITER")[1]
        result_dict = json.loads(logs)

        print(f"[DEBUG] result_dict: {result_dict}")

        container.remove(force=True)

        return result_dict
    
    except Exception as e:

        # Cover the case in which `container.remove()` fails
        if result_dict is not None:
            result_dict["errors"].append(e)
            result_dict["test_logs"].append(f":exclamation: Server error. Please contact the teacher. Score before this: {result_dict['score']}")
            result_dict["score"] = 0
            return result_dict
        else:
            return {"errors" : [e], "test_logs" : [":exclamation: Server error. Please contact the teacher"], "score" : 0}

    
