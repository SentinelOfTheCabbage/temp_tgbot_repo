#pylint: disable=C0111
import os
import sys

if __name__ != '__main__':
    GETCWD = os.getcwd()
    sys.path.append(GETCWD + '/branches/')
    os.chdir('./branches/')

def get_branches():
    current_directory = os.listdir()
    branches = [folder for folder in current_directory if os.path.isdir(folder)]
    branches.sort()
    branches_container = {}
    for elem in branches:
        exec(f'import {elem}')
        new_branch = {}
        exec(f'new_branch[\'triggers\'] = {elem}.get_triggers()')
        exec(f'new_branch[\'restarts\'] = {elem}.get_restarts()')
        exec(f'new_branch[\'steps\']    = {elem}.get_steps()')
        exec(f'new_branch[\'start\']    = {elem}.get_on_start')
        branches_container[elem] = new_branch

    return branches_container
