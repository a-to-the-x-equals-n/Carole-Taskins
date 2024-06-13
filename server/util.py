from dotenv import load_dotenv
from pathlib import Path
import os


def load_vars(*args):
    """
    Loads specified environment variables from a .env file located in the current script's directory.
    
    Args:
        *args: A list of environment variable names as strings.
    
    Returns:
        list: Values of the environment variables in the same order as requested.
    
    Raises:
        EnvFileError: If there's an issue reading the .env file.
    """
    try:
        # Determine the current directory of the script and locate the .env file
        current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
        envars = current_dir / ".env"

        # Load the environment variables from the .env file
        load_dotenv(envars)
        print(envars)

    # If any exception occurs during the process, raise an EnvFileError
    except Exception as e:
        print(f'Error opening .env file: {str(e)}')
    
    # Return a list of values for the given environment variable names
    return [os.getenv(arg) for arg in args]