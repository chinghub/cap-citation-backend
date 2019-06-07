from unittest import TestCase

from controllers import case_controller

class CaseControllerTest(TestCase):

    def test_case_controller(self):
        with self.assertRaises(Exception):
            case_controller.get_case(
                {
                    'payload': {
                        'capId': "abc123"
                    }
                }
            )
