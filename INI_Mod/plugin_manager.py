import importlib.util
import os
import logging

logging.basicConfig(level=logging.INFO)

class PluginManager:
    def __init__(self):
        self.plugins = []

    def load_plugins(self, directory):
        if not os.path.exists(directory):
            logging.error(f"The directory {directory} does not exist.")
            return

        try:
            for filename in os.listdir(directory):
                if filename.endswith(".py"):
                    file_path = os.path.join(directory, filename)
                    spec = importlib.util.spec_from_file_location("module.name", file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    if hasattr(module, 'execute'):  # Validate that the plugin has an execute method
                        self.plugins.append(module)
                        logging.info(f"Loaded plugin: {filename}")
                    else:
                        logging.warning(f"{filename} does not have an execute method and is not considered a valid plugin.")
            logging.info(f"Total plugins loaded: {len(self.plugins)}")
        except Exception as e:
            logging.error(f"Error loading plugins: {e}")

    def execute_plugins(self, *args, **kwargs):
        if not self.plugins:
            logging.warning("No plugins to execute.")
            return

        try:
            for plugin in self.plugins:
                plugin.execute(*args, **kwargs)
                logging.info(f"Executed plugin: {plugin.__name__}")
        except Exception as e:
            logging.error(f"Error executing plugins: {e}")
