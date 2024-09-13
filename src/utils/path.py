import os
import sys


proto_path = ""
if getattr(sys, 'frozen', False):  # 打包
    tool_helper_path = os.path.dirname(sys.executable)  # 生成的可执行exe的路径
elif __file__:  # 非打包
    tool_helper_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
APP_ROOT_PATH = tool_helper_path

print('APP_ROOT_PATH:', os.path.abspath(APP_ROOT_PATH))
