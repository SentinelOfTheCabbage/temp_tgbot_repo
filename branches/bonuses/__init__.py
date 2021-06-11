import os
import json
from copy import deepcopy
import pickle
import sys

MODULE_NAME = __name__

if __name__ != '__main__':
    getcwd = os.getcwd()
    sys.path.append(getcwd + f'/{MODULE_NAME}/')
    os.chdir(f'./{MODULE_NAME}/')
    PHASES_PKL_FILE = f'{MODULE_NAME}/phases.pickle'

from phase_pattern import Phase

#-----constants-----
NEW_PHASE_PHRASE = '# SETPHASE '
PHRASE_LEN_CONST = len(NEW_PHASE_PHRASE)
PHASES_FILE_NAME = 'phases.json'
PHASES_PKL_FILE = f'{MODULE_NAME}/phases.pickle'
IMPORTS = set(['re', 'Phase', 'types', 'datetime',
               'timedelta', 'MKAD', 'Point', 'Polygon', 'send_adm_message', 'deepcopy'])

phase_files = os.listdir('steps')
# phase_files.remove('phase_pattern.py')
# # phase_files.remove('__init__.py')
# # phase_files.remove('__pycache__')
# phase_files.remove('php.py')
# phase_files.remove(PHASES_FILE_NAME)

with open(PHASES_FILE_NAME, 'r') as phase_files_json:
    phases = json.loads(phase_files_json.read())

phases_backup = deepcopy(phases)
for filename in phase_files:
    with open('steps/' + filename, 'r', errors='ignore') as file:
        first_line = file.readline()

    if NEW_PHASE_PHRASE in first_line:
        print(f'NEW STEP FOUND AT "{filename}"')
        phase_number = int(first_line[PHRASE_LEN_CONST:])

        with open(filename, 'r') as file:
            whole_file = file.readlines()
            whole_file = whole_file[1:]
        with open(filename, 'w') as file:
            for line in whole_file:
                file.write(line)

        if len(phases) == phase_number:
            phases.append(filename)
        elif len(phases) > phase_number:
            phases = phases[:phase_number] + [filename] + phases[phase_number:]
        elif len(phases) == phase_number - 1:
            phases.append(filename)
        else:
            print(f'----ERROR ON {filename}---')
            with open(PHASES_FILE_NAME, 'w') as file:
                json.dump(phases_backup, file)
            break
        with open(PHASES_FILE_NAME, 'w') as file:
            json.dump(phases, file)


def find_all_steps():
    prev_dir = None
    import_cmd = None
    new_dir = None
    new_step = set()
    steps = []
    with open(PHASES_FILE_NAME, 'r') as source:
        phases = json.loads(source.read())

    for phase in phases:
        prev_dir = set(dir())
        phase = phase.replace('.py', '')
        import_cmd = f'from {MODULE_NAME}.steps.{phase} import *'
        exec(import_cmd)
        new_dir = set(dir())
        new_step = new_dir - prev_dir - IMPORTS - set(dir(Phase))
        steps.append(set(new_step))

    for pos, elem in enumerate(steps):
        steps[pos] = steps[pos].pop()
    steps = '[' + ', '.join(steps) + ']'
    with open('phases.pickle', 'wb') as file:
        exec(f'print("{MODULE_NAME}{steps}")')
        exec(f'pickle.dump({steps},file)')


def get_steps():
    getcwd = os.getcwd()
    os.chdir(f'./{MODULE_NAME}')
    with open('phases.pickle', 'rb') as source:
        x = pickle.load(source)
    os.chdir(getcwd)
    return x


def get_triggers():
    triggers = []
    triggers.append('/start bonuses')
    triggers.append('bonuses')
    return triggers


def get_restarts():
    restarts = []
    restarts.append('bonuses')
    restarts.append('/start bonuses')
    return restarts


def get_on_start(message):
    kwargs = {'start_phase':0}
    if '/start' in message.content:
        referal_id = message.get_referal()
        if referal_id is not None:
            kwargs['referal_id'] = referal_id
    return kwargs


if __name__ != '__main__':
    find_all_steps()
    os.chdir(getcwd)

if __name__ == '__main__':
    # find_all_steps()
    PHASES_PKL_FILE = 'phases.pickle'
    get_steps()
