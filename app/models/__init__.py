import os
import importlib


models_dir = os.path.dirname(__file__)

for root, dirs, files in os.walk(models_dir):
    for filename in files:
        if filename.endswith(".py") and filename != "__init__.py":
            rel_path = os.path.relpath(os.path.join(root, filename), models_dir)
            module_path = rel_path.replace(os.sep, ".").rsplit(".py", 1)[0]
            full_module = f"app.models.{module_path}"

            importlib.import_module(full_module)
