import sys
import unittest


class BaseTestCase(unittest.TestCase):
    """Baseclass for all the tests that Flask uses.  Use these methods
    for testing instead of the camelcased ones in the baseclass for
    consistency.
    """

    def setup(self):
        pass

    def teardown(self):
        pass

    def setUp(self):
        self.setup()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.teardown()

    def assert_equal(self, x, y):
        return self.assertEqual(x, y)

    def assert_raises(self, exc_type, callable=None, *args, **kwargs):
        catcher = _ExceptionCatcher(self, exc_type)
        if callable is None:
            return catcher
        with catcher:
            callable(*args, **kwargs)

    def assert_true(self, x, msg=None):
        self.assertTrue(x, msg)

    def assert_false(self, x, msg=None):
        self.assertFalse(x, msg)

    def assert_in(self, x, y):
        self.assertIn(x, y)

    def assert_not_in(self, x, y):
        self.assertNotIn(x, y)

    if sys.version_info[:2] == (2, 6):
        def assertIn(self, x, y):
            assert x in y, "%r unexpectedly not in %r" % (x, y)

        def assertNotIn(self, x, y):
            assert x not in y, "%r unexpectedly in %r" % (x, y)


class _ExceptionCatcher(object):

    def __init__(self, test_case, exc_type):
        self.test_case = test_case
        self.exc_type = exc_type

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        exception_name = self.exc_type.__name__
        if exc_type is None:
            self.test_case.fail('Expected exception of type %r' %
                                exception_name)
        elif not issubclass(exc_type, self.exc_type):
            reraise(exc_type, exc_value, tb)
        return True
