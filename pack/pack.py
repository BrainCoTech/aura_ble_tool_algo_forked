import os
import pprint
import shutil
import datetime
import subprocess
import sys
import time

import py7zr
import PySide6
import platform
from PyInstaller.__main__ import run
platform_sys = platform.platform()

# 对于需要用户能看到的资源文件和文件夹, 当_PACK_TYPE为-F时, 需要将其复制到打包后的exe文件夹中
# 对于不需要用户看到的资源文件和文件夹, 当_PACK_TYPE为-F时, 需要将其复制到exe_temp_path中
# 对于submodule, 无论_PACK_TYPE为-F还是-D, 无论submodule相对于当前项目的路径是在哪里, 都需要将其复制到exe_temp_path中


_APP_ROOT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(_APP_ROOT_PATH)
from version import VERSION

_PACK_TYPE = "-D"  # -F: 生成单个EXE文件, -D: 生成文件夹
_USE_PROTOBUF = True  # 是否使用protobuf
_ADD_IMG_ICON = True  # 是否添加图标
_EXE_NAME = "Edu_Dongle_Sensor_Demo_Tool"  # 项目生成EXE可执行文件名
_ICON_PATH_STRUCTURE = ["material", "edu.ico"]  # 图标相对路径结构
_PROTO_PATH_STRUCTURE = ["proto", "generated", "python"]  # protobuf python文件夹相对路径结构 例: ["mobius1.5_protobuf", "generated", "python"]
_COPY_FILES_PATH = ['settings.yaml', 'custom.css']
_COPY_FOLDER_PATH = ['material']

# ---------------------------------------------- 以下代码不需要修改 ----------------------------------------------
if "Windows" in platform_sys:
    _ADD_DATA_SEPARATOR = ";"
    _FILE_PATH_SEPARATOR = "\\"
else:
    _ADD_DATA_SEPARATOR = ":"
    _FILE_PATH_SEPARATOR = "/"

_TIME = datetime.datetime.now().strftime("%Y%m%d")
_CUR_FOLDER_NAME = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
_SITE_PACKAGES_PATH = os.path.dirname(PySide6.__path__[0])
_, COMMIT_ID = subprocess.getstatusoutput('git rev-parse HEAD')
_PACK_EXE_NAME = f"{_EXE_NAME}_{COMMIT_ID[:4]}_{VERSION}_{_TIME}"

if _PACK_TYPE == "-D":
    _PACK_DIST_PATH = os.path.join(_APP_ROOT_PATH, _CUR_FOLDER_NAME, _PACK_EXE_NAME, _EXE_NAME)
else:
    _PACK_DIST_PATH = os.path.join(_APP_ROOT_PATH, _CUR_FOLDER_NAME, _PACK_EXE_NAME)

print('APP_ROOT_PATH:', _APP_ROOT_PATH)
print("CUR_FOLDER_NAME:", _CUR_FOLDER_NAME)
print("SITE_PACKAGES_PATH:", _SITE_PACKAGES_PATH)
print("PACK_DIST_PATH:", _PACK_DIST_PATH)
print('\n' * 3)


def copy_file():
    for path in _COPY_FILES_PATH:
        absolute_path = os.path.join(_APP_ROOT_PATH, path)
        shutil.copy(absolute_path, _PACK_DIST_PATH)


def copy_folder():
    for path in _COPY_FOLDER_PATH:
        absolute_path = os.path.join(_APP_ROOT_PATH, path)
        folder_name = os.path.split(absolute_path)[1]
        shutil.copytree(absolute_path,  os.path.join(_PACK_DIST_PATH, folder_name))


opts = [_PACK_TYPE,
        f'--paths={_APP_ROOT_PATH}',
        f'--paths={_SITE_PACKAGES_PATH}{_FILE_PATH_SEPARATOR}PySide6',
        f'--add-data={_SITE_PACKAGES_PATH}{_FILE_PATH_SEPARATOR}google{_ADD_DATA_SEPARATOR}google',
        f'--distpath={_PACK_EXE_NAME}',
        '--noupx', '--clean', '--name', _EXE_NAME,
        f'{_APP_ROOT_PATH}/main.py']

#
# if _PACK_TYPE == "-D":
#     for file_path in _COPY_FILES_PATH:
#         absolute_path = os.path.join(_APP_ROOT_PATH, file_path)
#         opts.append(f'--add-data={absolute_path}{_ADD_DATA_SEPARATOR}.')
#
#     for folder_path in _COPY_FOLDER_PATH:
#         absolute_path = os.path.join(_APP_ROOT_PATH, folder_path)
#         opts.append(f'--add-data={absolute_path}{_ADD_DATA_SEPARATOR}.')


if _ADD_IMG_ICON:
    img_path = os.path.join(_APP_ROOT_PATH, *_ICON_PATH_STRUCTURE)
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"icon path not exists: {img_path}")
    opts.insert(1, '-i')
    opts.insert(2, img_path)


if _USE_PROTOBUF:
    _proto_path = os.path.abspath(os.path.join(_APP_ROOT_PATH, *_PROTO_PATH_STRUCTURE))
    if not os.path.exists(_proto_path):
        raise FileNotFoundError(f"protobuf python path not exists: {_proto_path}")
    print("PROTO_PYTHON_PATH:", _proto_path)
    sys.path.append(_proto_path)

    opts.append(f'--add-data={_proto_path}{_ADD_DATA_SEPARATOR}{os.path.join(*_PROTO_PATH_STRUCTURE)}')


if __name__ == '__main__':
    pprint.pprint(opts)
    run(opts)

    copy_file()
    copy_folder()  # 为什么不直接在软件自动解压后的_Temp文件夹内查找文件, 也是为了性能吧, 如果是一些大文件, 可能解压时候会很耗时

    shutil.rmtree("build")
    os.remove(_EXE_NAME + ".spec")

    # 7z压缩
    start_time = time.time()
    with py7zr.SevenZipFile(f'{_PACK_EXE_NAME}.7z', 'w') as z:
        z.writeall(_PACK_DIST_PATH, _PACK_EXE_NAME)
    print(f"7z打包耗时: {round(time.time() - start_time, 2)} s")

