import os
import sys
from abc import ABCMeta

import aaa_compose


class Command(ABCMeta):
    COMPOSE_DIR = os.path.dirname(aaa_compose.__file__)

    @classmethod
    def build_parser(mcs, parser):
        pass

    @classmethod
    def execute(mcs, args):
        arg = [[k, v] for k, v in args.__dict__.items() if v]
        if not arg:
            sys.exit(f'Command {mcs.NAME} requires at least one command')
        arg = arg[0]
        return arg[0], arg[1]
