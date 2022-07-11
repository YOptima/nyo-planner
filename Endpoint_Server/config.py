import os
import yaml
from pathlib import Path

# Importing Configuration Settings
config_path = Path.cwd() / "config.yaml"
CONFIGURATION: dict = {}
with open(config_path) as stream:
    CONFIGURATION = yaml.safe_load(stream)

# Setting Environment variables
CONFIGURATION["environment"] = "dev"
if "environment" in os.environ: CONFIGURATION["environment"] = os.environ.get("environment")

# Importing Logging configurations
logging_config_path = Path.cwd() / "Logging" / "config.yaml"
LOGGING_CONFIGURATION: dict = {}
with open(logging_config_path) as stream:
    LOGGING_CONFIGURATION = yaml.safe_load(stream)