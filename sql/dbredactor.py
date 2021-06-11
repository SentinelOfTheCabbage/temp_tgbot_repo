#pylint: disable=W0614,W0401,C0111,W0703
from db_teller import *

DATABASE = DbTeller()

if __name__ == '__main__':
    while True:
        COMMAND = input('WRITE CMD:\n')
        try:
            DATABASE.execute(COMMAND)
        except Exception as exc:
            print('SOMETHING WRONG\n', exc)
            continue
