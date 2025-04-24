# Import necessary modules
import os  # For interacting with the operating system (e.g., file paths)
from configobj import ConfigObj  # For reading structured configuration files

# Determine the absolute path of the current script's directory
BASE = os.path.dirname(os.path.abspath(__file__))

# Load the configuration file 'config.cfg' located in the same directory
CONFIG = ConfigObj(os.path.join(BASE, 'config.cfg'))

# Extract specific configuration sections for easy access
API_CONFIG = CONFIG['api']        # API-related configuration (e.g., host, port)
JWT_CONFIG = CONFIG['jwt']        # JWT settings (e.g., secret key, expiration)
LOG_CONFIG = CONFIG['log']        # Logging configuration (e.g., level, file path)
MONGO_CONFIG = CONFIG['mongo']    # MongoDB connection configuration (e.g., URI, database name)
OLLAMA_CONFIG = CONFIG['ollama']
