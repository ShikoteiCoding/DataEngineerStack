import logging

from config import Session
from definition import load as load_definition



if __name__ == "__main__":
    
    session = Session(from_local=True)

    env_config = session.config

    logger = logging.basicConfig(level=env_config["LOG_LEVEL"])

    definition_path = "microservices/generator/definitions/dummy.yaml"
    definition_dict = load_definition(definition_path)
    