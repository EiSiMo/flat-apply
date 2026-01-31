from providers._provider import Provider

import pkgutil
import importlib


# This code runs the moment anyone imports the 'providers' package
__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    full_module_name = f"{__name__}.{module_name}"
    importlib.import_module(full_module_name)
    __all__.append(module_name)


PROVIDERS = dict()
for provider_class in Provider.__subclasses__():
    provider_instance = provider_class()
    PROVIDERS[provider_instance.domain] = provider_instance
