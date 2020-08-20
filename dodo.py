import os


os.environ['PYTHONPATH'] = '.'


def task_test():
    """Run all tests"""
    return {'actions': ['pytest'],
            'verbosity': 2}


def task_lint():
    """Check linting"""
    return {'actions': ['flake8 ruly test']}
