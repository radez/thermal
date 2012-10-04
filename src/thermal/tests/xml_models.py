"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from thermal.models import Stack

class XmlModelTests(TestCase):
    def test_get_all_stacks(self):
        """
        Test that we can get stacks
        """
        stacks = Stack.objects.all()
        for s in stacks:
            self.assertTrue(s.StackName.startswith('wordpress'))
        self.assertEqual(stacks.count(), 3)
