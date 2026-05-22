"""A python module to calculate a fasting diet.

Logic
the user asks for a particular date/week/month/year
- check if there is a file, matching the requested year
- if not, generate the full list for the year and write it down
- load the file and get the value for the requested period
- load the (localized) text strings matching the value(s)
- bassed on the request, form the output

"""
import sys
from datetime import date
import warnings

# set sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fasting_io import read_fasting_list, write_fasting_list
from fasting_status import fasting_value_to_message

# from calculateEasterSunday import calcEaster
from generateCalendar import fastingYearList, date_number

# from src.calculateEasterSunday import calcEaster


def get_fasting_message_for_date(input_date: date):
    """Calculate the fasting status and forms a text message for a particular date.

    Args:
        inputDate: a date for which to calculate the status

    Returns:
        An text string, describing the fasting do's and don'ts

    """
    # check if we have the list structure pre-populated
    my_fasting_list = read_fasting_list(input_date.year)
    if my_fasting_list is None:  # we found no file, we need to generate a list
        my_fasting_list = fastingYearList(input_date.year)
        # make sure we serialize the calendar, so it can be re-used in the future
        write_fasting_list(input_date.year, my_fasting_list)
        #my_fasting_list = read_fasting_list(
        #    input_date.year
        #)  # think how to avoid calling this twice
    # get the date number in the year
#    date_number = date_number(input_date)
    return fasting_value_to_message(int(my_fasting_list[date_number(input_date) - 1]))


def get_status_for_date(input_date: date):
    """Calculate the fasting status for a particular date.

    Args:
        inputDate: a date for which to calculate the status

    Returns:
        An integer (0..6) representing the fasting status

    """
    # check if we have the list structure pre-populated
    my_fasting_list = read_fasting_list(input_date.year)
    if my_fasting_list is None:  # we found no file, we need to generate a list
        my_fasting_list = fastingYearList(input_date.year)
        # make sure we serialize the calendar, so it can be re-used in the future
        write_fasting_list(input_date.year, my_fasting_list)
        #my_fasting_list = read_fasting_list(
        #    input_date.year
        #)  # think how to avoid calling this twice
    # get the date number in the year
    return int(my_fasting_list[date_number(input_date) - 1])

def getStatusForDate(input_date: date):
    """
    Keep for compatibility
    """
    warnings.warn("getStatusForDate is being deprecated, pls use get_status_for_date().")
    return get_status_for_date(input_date)

def getFastingMessageForDate(input_date: date):
    """
    Keep for compatibility
    """
    warnings.warn("getFastingMessageForDate is being deprecated,\
                pls use get_fasting_message_for_date().")
    return get_fasting_message_for_date(input_date)



def main(argv):
    """Evaluate the CLI arguments and calculate the fasting status.

    Args:
        one argument: a date in YYYY-MM-DD format for which to calculate the status
        zero arguments/no input: defaults to the current date
        more than 1 argument: returns an error message
        anything else: raises a value error

    Returns:
        An integer (0..6) representing the fasting status

    """
    # check for number of arguments - should be one (year) plus one (name of program itself)
    if (len(argv) > 2) or (len(argv) < 1):
        sys.stderr.write("USAGE:$python /path/to/bgchof.py <date for which to get the orthodox fasting status>\n")
        return None
    elif len(argv) == 1:
        #print("NoThe argument should be an day in the format yyyy-mm-dd)
        # return None
        d_input_date = date.today()
    else:
        s_input_date = argv[1]
        # check for valid type
        try:
            d_input_date = date.fromisoformat(s_input_date)
        except ValueError:
            sys.stderr.write("The argument should be an day in the format yyyy-mm-dd")
            return None

    # get the status
    return get_fasting_message_for_date(d_input_date)

if __name__ == "__main__":
    sys.exit(main(sys.argv))


# debug

# myDate = date.today()
# myDate = date(2024, 11, 11)
# status = getFastingStatusForDate(myDate)
# print(status)
