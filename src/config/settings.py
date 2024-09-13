from ruamel.yaml import YAML
yaml = YAML()


SETTINGS_FILE_PATH = "settings.yaml"


with open(SETTINGS_FILE_PATH, 'r', encoding='utf-8') as f:
    config = yaml.load(f)

if not isinstance(config, dict):
    raise Exception("file is corrupted：{}".format(SETTINGS_FILE_PATH))

ALL_CONFIG = config
BASIC = config['BASIC']
PROTO_CONFIG = config['PROTO_CONFIG']
TOOL_CONFIG = config['TOOL_CONFIG']
BLE_CONFIG = config['BLE_CONFIG']


