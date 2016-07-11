import os
import sys

_dir = sys.argv[1]
_list = os.popen('ls {}'.format(_dir)).read()
_list = _list.split('\n')
for item in range(0, len(_list) - 1):
    print(_list[item])
    _name = _list[item].split('.')[0]
    os.popen('mv {0}{1} {0}{2}.mp4'.format(
        _dir,
        _list[item],
        _name
    ))
