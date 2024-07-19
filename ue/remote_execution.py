import sys

PythonScriptPlugin = r'D:\UE5\UE_5.4\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python'

if not PythonScriptPlugin in sys.path:
    sys.path.append(PythonScriptPlugin)

import remote_execution as remote

def execute_command(python_file_path):
    remote_exec = remote.RemoteExecution()
    remote_exec.start()
    remote_exec.open_command_connection(remote_exec.remote_nodes)
    remote_exec.run_command(python_file_path)
    remote_exec.stop()
    return None
    

python_file_path = r"D:\git\TECH_ART_ONLINE\Python\maya\generate_fbx.py"
execute_command(python_file_path)