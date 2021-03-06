import os
import time
from build_interface.settings import BASE_DIR
import subprocess


def update_last_kinit_env_var():

    """
    This function performs kinit as and when required.
    The function expects .aws directory in the project base directory.
    The .aws directory should have a keytab file by name redhat.keytab.
    :return: None
    """

    keytab_file = BASE_DIR + "/.keytab/redhat.keytab"
    print(keytab_file)
    kinit_request = subprocess.Popen(["kinit", "-kt", keytab_file, "adtrived@REDHAT.COM"],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = kinit_request.communicate()
    os.environ["LAST_KINIT_TIME"] = str(int(time.time()))


def handle_kinit():

    """
    This function tests whether kinit is required. The current policy is to do kinit after
    every hour.
    :return: None
    """

    if "LAST_KINIT_TIME" not in os.environ:
        update_last_kinit_env_var()

    last_update = os.environ["LAST_KINIT_TIME"]
    time_now = int(time.time())

    if time_now - int(last_update) >= 3600:
        update_last_kinit_env_var()
