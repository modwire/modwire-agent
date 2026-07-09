import importlib

for module_name in ("tag", "section", "record", "content"):
    importlib.import_module(f"{__name__}.{module_name}")
