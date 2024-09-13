import importlib
import os
import pkgutil
import sys

# 加载 PROTO_PATH 下的 python 模块
_MODULES = {}
_CLASSES = {}
_CLASSES_TYPE = {}
_PACK_NAME_MAP = {}


def _reload_all(proto_path):
    global _MODULES
    global _CLASSES
    global _CLASSES_TYPE
    _MODULES = {}
    _CLASSES = {}
    _CLASSES_TYPE = {}

    # 由于某些协议文件是多文件夹结构, 但是没有为每一个文件夹提升为模块(添加__.init__.py)， 导致 pkgutil.walk_packages
    # 解决方式
    # 1. 生成协议的python文件夹如果涉及到多文件, 必须加上__init__.py

    for importer, modname, ispkg in pkgutil.walk_packages(path=[proto_path], onerror=ImportError):
        if not ispkg:
            pack = os.path.split(importer.path)[-1]
            mod = importlib.import_module(modname)
            _MODULES.setdefault(pack, [])
            _MODULES[pack].append(mod)
        else:
            importlib.import_module(modname)

    for pack in _MODULES:
        for mod in _MODULES[pack]:
            mod_scope = [name for name in dir(mod) if not name.startswith('__')]
            for obj in mod_scope:
                mod_attr = getattr(mod, obj)
                if isinstance(mod_attr, type) and not mod_attr.__subclasses__():
                    pack_name = pack[0].upper() + pack[1:]
                    _CLASSES.setdefault(pack_name, [])
                    if mod_attr.__name__ not in _CLASSES[pack_name]:
                        _CLASSES[pack_name].append(mod_attr.__name__)
                        _CLASSES_TYPE[mod_attr.__name__] = mod_attr


def register_proto_class(proto_path):
    if not _MODULES:
        if os.path.exists(proto_path):
            _reload_all(proto_path)


def get_proto_class(name):
    if name in _CLASSES_TYPE:
        return _CLASSES_TYPE[name]
    raise NameError("{} is not a proto class".format(name))


def list_proto_class():
    return _CLASSES.copy()
