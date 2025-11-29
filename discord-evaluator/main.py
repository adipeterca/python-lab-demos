from shared import API_TOKEN
from bot import client, scores
from utils import create_score_path, create_folder_structure
import signal


def custom_on_close(signal, frame):
    
    print("[INFO] Discord bot closed")
    if len(scores) == 0:
        print("[WARNING] Scoreboard is empty")
        exit()

    score_path = create_score_path()
    print(f"[INFO] Saving scores to {score_path} ...")
    try:
        with open(score_path, "w") as fout:
            for k, v in scores.items():
                fout.write(f"{k} : {v} points\n")
    except Exception as e:
        print("[ERROR] Could not save scores, printing them instead ...")
        print(scores)
        print(f"The following exception was raised: {e}")
    
    # To ensure the bot closes properly
    client.loop.create_task(client.close())
    exit(0)

# Reliable way to ensure cleanup once the bot finishes execution
# By default, `ctrl+c` is handled inside `client.run()` and cannot be
# caught outside of it.
signal.signal(signal.SIGINT, custom_on_close)

try:
    create_folder_structure()
except Exception as e:
    print(f"[ERROR] Could not create the project structure: {e}")
else:
    print("[INFO] Project structure status: OK")
    print("[INFO] Before you run, make sure docker / Docker Desktop is running.")
    input("[INFO] Press enter to continue ...")
    client.run(API_TOKEN)