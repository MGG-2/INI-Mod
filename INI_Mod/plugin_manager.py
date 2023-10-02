import os
import importlib.util
import logging

logging.basicConfig(level=logging.INFO)

class PluginManager:
    def __init__(self, plugin_folder):
        self.plugin_folder = plugin_folder
        self.plugins = {}
        self.active_plugins = set()

    def load_plugins(self):
        for filename in os.listdir(self.plugin_folder):
            if filename.endswith('.py'):
                try:
                    spec = importlib.util.spec_from_file_location(
                        filename[:-3], os.path.join(self.plugin_folder, filename))
                    plugin = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(plugin)
                    self.plugins[filename[:-3]] = plugin
                    logging.info(f"Plugin {filename[:-3]} loaded successfully.")
                except Exception as e:
                    logging.error(f"Error loading plugin {filename[:-3]}: {e}")

    def activate_plugin(self, plugin_name):
        if plugin_name in self.plugins and plugin_name not in self.active_plugins:
            self.active_plugins.add(plugin_name)
            logging.info(f"Plugin {plugin_name} activated.")

    def deactivate_plugin(self, plugin_name):
        if plugin_name in self.active_plugins:
            self.active_plugins.remove(plugin_name)
            logging.info(f"Plugin {plugin_name} deactivated.")
