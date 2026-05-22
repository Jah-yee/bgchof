"""Serialize and deserialize a list of fasting values.

Uses .csv files in CFG_DATAFILE_PREFIX to read from and write into.
"""

# import generateCalendar
import csv
import sys
import os

if "BGCHOF_CFG_CFG_DATAFILE_PREFIX" not in os.environ:
    BGCHOF_CFG_CFG_DATAFILE_PREFIX = "./.bgchofcache/"
else:
    BGCHOF_CFG_CFG_DATAFILE_PREFIX = os.environ["BGCHOF_CFG_CFG_DATAFILE_PREFIX"]
CFG_DATAFILE_MODE = 0o777


def read_fasting_list(input_year):
    """Load contents of .csv cache file into a list.

    Args:
        input_year: int representing the year for which to load the cache file.

    Returns:
        fasting_list: a list of [int(0..365) dayNumber, int(0..6) statusValue].
    Raises:
        FileNotFoundError: if cache file doesn't exists. Moves on to create a new one.
    """
    fasting_list = []
    file_name = BGCHOF_CFG_CFG_DATAFILE_PREFIX + str(input_year) + ".csv"
    try:
        with open(file_name, mode="r") as fasting_list_file:
            file_reader = csv.reader(fasting_list_file, delimiter=",")
            next(file_reader, None)  # skip headers --> should we validate instead?
            for row in file_reader:
                fasting_list.append(row[1])
            return fasting_list
    except FileNotFoundError as e:
        msg = (
            "Can't find the data file for year "
            + str(input_year)
            + ". Creating new one...\n"
        )
        sys.stderr.write(msg)
        return None


def write_fasting_list(input_year, input_list):
    """Dump an year-worth of fasting statuses into a .csv cache file.

    Args:
        input_year: an int representing the year for which the status values.
        input_list: a list of [int(0..365) dayNumber, int(0..6) statusValue]
    Returns:
        True: if serialization was successful.
    Raises:
        Returns error messages if cache directory exists or can't be created, 
        if cache file can't be created.
    """
    # try to create the cache directory, write error to stdout if exists
    if not os.path.isdir(BGCHOF_CFG_CFG_DATAFILE_PREFIX):
        try:
            os.umask(0o022)
            os.makedirs(
                BGCHOF_CFG_CFG_DATAFILE_PREFIX, CFG_DATAFILE_MODE, exist_ok=True
            )
        except:
            sys.stderr.write("Can't create the cache directory.\n")
            exit(1)
    else:
        sys.stderr.write("Cache directory already exists.\n")
    file_name = BGCHOF_CFG_CFG_DATAFILE_PREFIX + str(input_year) + ".csv"
    try:
        with open(file_name, mode="w") as fasting_list_file:
            file_writer = csv.writer(fasting_list_file, delimiter=",")
            file_writer.writerow(["dayNumber", "Status"])
            for n in range(len(input_list)):
                file_writer.writerow([n + 1, input_list[n]])
        return True
    except:
        msg = "Can't create data file for year " + str(input_year) + ".\n"
        sys.stderr.write(msg)
        exit(1)


# To do - add CLI arguments to manage cache, i.e. delete all .csv files
