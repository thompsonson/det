"""
File contains the PromptManager class and code to ensure it is a singleton.
It does this to reduce the load on the system by only loading the prompts once.
"""

import json
import logging
import os


class Singleton(type):
    """
    Singleton is a metaclass that ensures the instantiation of its instances to be singletons.
    It is used to control the creation of classes. If an instance of a class with Singleton as
    metaclass already exists, the existing instance is returned. If not, a new one is created.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# pylint: disable=too-few-public-methods
class PromptManager(metaclass=Singleton):
    """
    The PromptManager is responsible for managing all prompts in the application.
    It follows the Singleton pattern to ensure that there's only one instance of it
    throughout the application.
    """

    # Determine the directory of the current file (prompt_manager.py)
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to your resource
    PROMPTS_FILENAME = os.path.join(
        current_directory, "..", "resources", "prompts.json"
    )

    def __init__(self, prompts_file_path=None):
        self.logger = logging.getLogger(__name__)
        if prompts_file_path:
            self.PROMPTS_FILENAME = prompts_file_path
        self.logger.info("Loading prompts from %s", self.PROMPTS_FILENAME)

        if not os.path.exists(self.PROMPTS_FILENAME):
            self.logger.error("File %s does not exist", self.PROMPTS_FILENAME)
            raise FileNotFoundError(f"File {self.PROMPTS_FILENAME} does not exist")

        try:
            with open(self.PROMPTS_FILENAME, "r", encoding="utf-8") as file_to_read:
                self.prompts = json.load(file_to_read)
        except Exception as exception:
            self.logger.error("Failed to load prompts: %s", exception)
            raise

    def get_prompts(self, class_name):
        """
        Get the prompts for a specific class.

        Parameters
        ----------
        class_name : str
            The name of the class to get prompts for.

        Returns
        -------
        dict
            The prompts for the class.
        """
        prompts = self.prompts.get(class_name, {})
        if not prompts:
            self.logger.warning("No prompts found for class %s", class_name)
        return prompts
