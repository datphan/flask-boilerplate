# -*- coding: utf-8 -*-

"""support for webargs"""

from webargs import Arg
from functools import wraps
from ..utils import extract_filters
from webargs.flaskparser import use_args


def _string_to_boolean(value):
    mappings = {
        'true': True,
        'false': False,
        '1': True,
        '0': False
    }

    return mappings.get(value.lower(), True)

# false or 0 => False; others => True
BoolArg = Arg(bool, use=_string_to_boolean)


def extract_args(search_args):
    """
    Decorator that extract args

    :param search_args: fields to extract.
    """
    
    def wrapper(func):
        @wraps(func)
        @use_args(search_args)
        def decorated(*args, **kwargs):

            if args and args[1]:
                # class method
                args[1]['filters'] = extract_filters(args[1])

                return func(args[0], *args[1:], **kwargs)
            else:
                # function
                args['filters'] = extract_filters(args)

                return func(args)


        return decorated

    return wrapper
