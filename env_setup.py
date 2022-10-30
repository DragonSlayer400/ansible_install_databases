import os
import sys
from datetime import datetime

"""
Run command generate windows variables from properties file: python3 ./env_setup.py export_bat
Run command generate linux variables from properties file: python3 ./env_setup.py export_shell
Run commad output variables from properties file: python3 ./env_setup.py output_env
"""

def logger(level, message):
    text = "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] [" + level+ "] " + message
    if level == 'INFO':
        print("\033[32m{}\033[0m".format(text))
    if level == 'ERROR':    
        print("\033[31m{}\033[0m".format(text))
    if level == 'WARN':
        print("\033[33m{}\033[0m".format(text))

def read_properties(filepatch, sep='=', comment_char='#'):
    props = []
    logger('INFO', 'Читаем файл ' + filepatch)
    with open(filepatch, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"')
                props.append([key, value])
    logger('INFO', 'Файл ' + filepatch + ' прочитан')
    return props

def set_env(props):
    for item in props:
        os.environ[item[0]] = item[1]

def output_env(props):
    for item in props:
        logger('INFO', item[0] + "=" + item[1])

def write_variables_to_file(file_path_output, variables_export):
    logger('INFO', 'Запись переменных окружения в файл ' + file_path_output + ' начата')
    with open(file_path_output, 'w') as fp:
        for item in variables_export:
            fp.write("%s\n" % item)
    logger('INFO', 'Запись переменных окружения в файл ' + file_path_output + ' завершена')

def generate_export_variables_to_shell(props, file_path_output='./export_sh.sh'):
    export_variable_shell=[]
    logger('INFO', 'Генерируем переменные окружения для linux')
    for item in props:
        export_variable_shell.append("export " + item[0] + "=" + item[1])
    write_variables_to_file(file_path_output, export_variable_shell)
    logger('INFO', 'Генерация переменных окружения для linux завершена')

def generate_export_variables_to_bat(props, file_path_output='./export_bat.bat'):
    export_variable_bat=[]
    logger('INFO', 'Генерируем переменные окружения для windows')
    for item in props:
        export_variable_bat.append("SET " + item[0] + "=" + item[1])
    write_variables_to_file(file_path_output, export_variable_bat)
    logger('INFO', 'Генерация переменных окружения для windows завершена')

args = sys.argv[1:]

if len(args) == 0:
    logger('ERROR', 'Не указан входной аргумент, указывающий значение action')
    sys.exit(1)

action = args[0]

file_input_path = './env.properties'
file_path_output = ''

if len(args) > 1:
    file_input_path = args[1]

if not os.path.isfile(file_input_path):
    logger('ERROR', 'Не найден указанный properties файл ' + file_input_path)
    sys.exit(1)

if action == 'export_bat' or action == 'export_shell':
    if len(args) == 3:
        file_path_output = args[2]

if action == 'set_env':
    set_env(read_properties(file_input_path))
elif action == 'export_bat':
    generate_export_variables_to_bat(read_properties(file_input_path), file_path_output if file_path_output != '' else './export_bat.bat')
elif action == 'export_shell':
    generate_export_variables_to_shell(read_properties(file_input_path), file_path_output if file_path_output != '' else './export_bat.sh')
elif action == 'output_env':
    output_env(read_properties(file_input_path))
else:
    logger('WARN', 'Action не опознан')