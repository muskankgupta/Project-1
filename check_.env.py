from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent / ".env"

print("Current directory :", Path.cwd())
print("Script directory  :", Path(__file__).parent)
print("Env path          :", env_path)
print("Env exists?       :", env_path.exists())

loaded = load_dotenv(dotenv_path=env_path)

print("Loaded?           :", loaded)
print("HOST              :", os.getenv("DATABRICKS_SERVER_HOSTNAME"))
print("HTTP PATH         :", os.getenv("DATABRICKS_HTTP_PATH"))
print("TOKEN FOUND?      :", os.getenv("DATABRICKS_TOKEN") is not None)