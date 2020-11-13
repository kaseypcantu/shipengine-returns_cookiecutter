import os
import datetime
import importlib
import sys
import subprocess
from contextlib import contextmanager

from cookiecutter.utils import rmtree
from click.testing import CliRunner
import shlex
import pytest_cookies


@contextmanager
def inside_directory(dirpath):
    """
    Execute code from inside the given directory.
    
    :param dirpath: String: Path of the directory the command is being run in. 
    :return: void
    """
    previous_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(previous_path)


@contextmanager
def bake_in_temporary_directory(cookies, *args, **kwargs):
    """
    Delete the temporary directory that is created when executing tests.
    
    :param cookies: pytest_cookies.Cookies: Cookie to be baked and its temporary files to be removed.
    :param args: 
    :param kwargs: 
    :return: 
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def run_inside_directory(command, dirpath):
    with inside_directory(dirpath):
        return subprocess.check_call(shlex.split(command))


def check_output_inside_directory(command, dirpath):
    """Run a command inside a given directory, returning the command output for review,"""
    with inside_directory(dirpath):
        return subprocess.check_output(shlex.split(command))


def project_insight(result):
    """
    Get top-level directory, project_slug, and project directory from baked cookies.
    :param result:
    :return: Project path, project slug, and project directory.
    """
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, project_slug)
    return project_path, project_slug, project_dir


def test_bake_with_defaults(cookies):
    with bake_in_temporary_directory(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        assert_toplevel_files = [f.basename for f in result.preojct.listdir()]
        assert "requirements.txt" in assert_toplevel_files
        assert ".env" in assert_toplevel_files
        assert "run.py" in assert_toplevel_files


def test_in_pytest(cookies):
    with bake_in_temporary_directory(
            cookies,
            extra_context={"use_pytest": "y"}
    ) as result:
        assert result.project.isdir()
        test_file_path = result.project.join(
                "tests/test_in_pytest.py"
        )
        lines = test_file_path.readlines()
        assert "import pytest" in "".join(lines)
        # Test the new pytest target
        run_inside_directory('python setup.py pytest', str(result.project)) == 0
        # Test the test alias (which invokes pytest)
        run_inside_directory('python setup.py test', str(result.project)) == 0\

