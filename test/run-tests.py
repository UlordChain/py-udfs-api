#!/usr/bin/python
from __future__ import print_function

import contextlib
import pathlib
import os
import random
import shutil
import subprocess
import sys
import time


if not hasattr(contextlib, "suppress"):
	"""
	Polyfill for ``contextlib.suppress``
	"""
	@contextlib.contextmanager
	def _contextlib_suppress(*exceptions):
		try:
			yield
		except exceptions:
			pass
	contextlib.suppress = _contextlib_suppress


######################
# Test configuration #
######################

# Environment name as used by `tox`
ENVNAME = "py{}{}".format(sys.version_info.major, sys.version_info.minor)

# Determine project base directory and testing path
BASE_PATH = pathlib.Path(__file__).parent.parent
TEST_PATH = BASE_PATH / "build" / "test-{}".format(ENVNAME)
udfs_PATH = TEST_PATH / "udfs-path"

HOST = "127.0.0.1"
PORT = random.randrange(40000, 65535)


###########################
# Set up test environment #
###########################

# Add project directory to PYTHONPATH
sys.path.insert(0, str(BASE_PATH))

# Switch working directory to project directory
os.chdir(str(BASE_PATH))

# Export environment variables required for testing
os.environ["udfs_PATH"] = str(udfs_PATH)
os.environ["PY_udfsAPI_DEFAULT_HOST"] = str(HOST)
os.environ["PY_udfsAPI_DEFAULT_PORT"] = str(PORT)

# Make sure the udfs data directory exists and is empty
with contextlib.suppress(OSError):  #PY2: Replace with `FileNotFoundError`
	shutil.rmtree(str(udfs_PATH))

with contextlib.suppress(OSError):  #PY2: Replace with `FileExistsError`
	os.makedirs(str(udfs_PATH))

# Initialize the udfs data directory
subprocess.call(["udfs", "init"])
subprocess.call(["udfs", "config", "Addresses.Gateway", ""])
subprocess.call(["udfs", "config", "Addresses.API",     "/ip4/{}/tcp/{}".format(HOST, PORT)])


################
# Start daemon #
################

# Spawn udfs daemon in data directory
DAEMON = subprocess.Popen(["udfs", "daemon", "--enable-pubsub-experiment"])
os.environ["PY_udfsAPI_TEST_DAEMON_PID"] = str(DAEMON.pid)

# Collect the exit code of `DAEMON` when `SIGCHLD` is received
# (otherwise the shutdown test fails to recognize that the daemon process is dead)
if os.name == "posix":
	import signal
	signal.signal(signal.SIGCHLD, lambda *a: DAEMON.poll())

# Wait for daemon to start up
import udfsapi
while True:
	try:
		udfsapi.connect(HOST, PORT)
	except udfsapi.exceptions.ConnectionError:
		time.sleep(0.05)
	else:
		break


##################
# Run test suite #
##################

PYTEST_CODE = 1
try:
	# Run tests in CI-mode (will stop the daemon at the end through the API)
	os.environ["CI"] = "true"
	
	# Make sure all required py.test plugins are loaded
	os.environ["PYTEST_PLUGINS"] = ",".join(["pytest_cov", "pytest_ordering"])
	
	# Launch py.test in-process
	import pytest
	PYTEST_CODE = pytest.main([
		"--verbose",
		"--cov=udfsapi",
		"--cov-report=term",
		"--cov-report=html:{}".format(str(TEST_PATH / "cov_html")),
		"--cov-report=xml:{}".format(str(TEST_PATH / "cov.xml"))
	] + sys.argv[1:])
finally:
	# Make sure daemon was terminated during the tests
	if DAEMON.poll() is None:  # "if DAEMON is running"
		DAEMON.kill()
		
		print("udfs daemon was still running after test!", file=sys.stderr)

sys.exit(PYTEST_CODE)
