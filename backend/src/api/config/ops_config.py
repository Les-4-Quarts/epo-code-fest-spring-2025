from api.config.logging_config import load_config
import os


# Load configuration
config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
config = load_config(config_path)

ops_config = config.get('ops', {})
ops_consumer_key = ops_config.get('consumer_key')
ops_consumer_secret_key = ops_config.get('consumer_secret_key')
ops_api_url = ops_config.get('ops_api_url')
