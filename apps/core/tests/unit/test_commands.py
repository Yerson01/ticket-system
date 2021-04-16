from io import StringIO

from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test.testcases import TestCase


class TestWaitForDbCommand(TestCase):

    def test_wait_for_db_command_ready(self):
        """Test that wait for db command is called"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as get_item:
            output = StringIO()
            get_item.return_value = True
            call_command('wait_for_db', stdout=output)
            assert get_item.call_count == 1

    @patch('time.sleep')
    def test_wait_for_db_command(self, ts):
        """Test wait for db command works as expected"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as get_item:
            output = StringIO()
            get_item.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db', stdout=output)
            assert get_item.call_count == 6
