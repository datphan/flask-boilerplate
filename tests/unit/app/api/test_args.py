# -*- coding: utf-8 -*-

"""tests for app.api.args"""

from app.api.args import BoolArg
from mock import patch

from tests.unit import UnitTestCase


class ArgsTestCase(UnitTestCase):

    def test_bool_arg(self):

        tests = {
            'true': True,
            'True': True,
            'tRuE': True,
            'false': False,
            'False': False,
            'fAlSe': False,
            '0': False,
            '1': True,
            '-1': True,  # follow python bool
            'something': True
        }

        for val, expected in tests.iteritems():
            self.assertEqual(BoolArg.validated('active', val), expected,
                             '{} should be {}'.format(val, expected))

    @patch('app.api.args.use_args')
    def test_extract_args(self, mock_use_args):

        from app.api.args import extract_args
        from webargs import Arg

        search_args = {
            'filters': Arg(str),
            'email': Arg(str),
        }

        def use_args(args):
            return args

        mock_use_args.return_value = use_args

        class Test:
            @extract_args(search_args)
            def test(self, args):
                return args

        test = Test()


        # missing value
        result = test.test({
            'email': '',
            'filters': 'abc,eq;def,lt,2.3,4'
        })

        

        expected_result = {
            'email': '',
            'filters': [
                {'key': 'def', 'op': 'lt', 'value': 2.3}
            ]
        }


        self.assertEqual(result, expected_result)


        # correct format
        result = test.test({
            'name': '',
            'filters': 'abc,eq,1;def,lt,2,3,4,5,6,7;<key>,<op>,<value>'
        })

        expected_result = {
            'name': '',
            'filters': [
                {'key': 'abc', 'op': 'eq', 'value': 1},
                {'key': 'def', 'op': 'lt', 'value': 2},
                {'key': '<key>', 'op': '<op>', 'value': '<value>'}
            ]
        }

        self.assertEqual(result, expected_result)


        # contain quote
        result = test.test({
            'name': '',
            'filters': "abc,eq,1;def,lt,\"3\";<key>,<op>,'<value>'"
        })

        expected_result = {
            'name': '',
            'filters': [
                {'key': 'abc', 'op': 'eq', 'value': 1},
                {'key': 'def', 'op': 'lt', 'value': '"3"'},
                {'key': '<key>', 'op': '<op>', 'value': "'<value>'"}
            ]
        }

        self.assertEqual(result, expected_result)

