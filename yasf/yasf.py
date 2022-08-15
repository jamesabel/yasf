from enum import Enum
import decimal
from decimal import Decimal
import json
from typing import Tuple, Union, Any
import csv
from tempfile import TemporaryDirectory
from pathlib import Path
from logging import getLogger

from yasf.__version__ import __application_name__

structured_sentinel = "<<>>"  # use illegal JSON
_half_size = int(round(len(structured_sentinel) / 2))
escaped_structured_sentinel = structured_sentinel[:_half_size] + "/" + structured_sentinel[_half_size:]  # put some special character in the middle of the sentinel


log = getLogger(__application_name__)


def convert_serializable_special_cases(o):
    """
    Convert an object to a type that is fairly generally serializable (e.g. json serializable).
    This only handles the cases that need converting.  The json module handles all the rest.
    For JSON, with json.dump or json.dumps with argument default=convert_serializable.
    Example:
    json.dumps(my_animal, indent=4, default=convert_serializable)
    :param o: object to be converted to a type that is serializable
    :return: a serializable representation
    """

    if isinstance(o, Enum):
        serializable_representation = o.name
    elif isinstance(o, Decimal):
        try:
            is_int = o % 1 == 0  # doesn't work for numbers greater than decimal.MAX_EMAX
        except decimal.InvalidOperation:
            is_int = False  # numbers larger than decimal.MAX_EMAX will get a decimal.DivisionImpossible, so we'll just have to represent those as a float

        if is_int:
            # if representable with an integer, use an integer
            serializable_representation = int(o)
        else:
            # not representable with an integer so use a float
            serializable_representation = float(o)
    elif isinstance(o, bytes) or isinstance(o, bytearray):
        serializable_representation = str(o)
    elif hasattr(o, "value"):
        serializable_representation = str(o.value)
    else:
        serializable_representation = str(o)
        # raise NotImplementedError(f"can not serialize {o} since type={type(o)}")
    return serializable_representation


def _args_to_csv_string(*args):
    """
    Convert args to a comma-separated string
    :param args: args
    :return: comman separated string
    """
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir, "temp.txt")
        with file_path.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(*args)
        with file_path.open() as f:
            s = f.read().strip()
    return s


def _get_escape_structured_sentinel(value: Any) -> Any:
    """
    return a string that has any appearance of the sentinel escaped out
    :param value -
    :return: string with any sentinels escaped out
    """
    if isinstance(value, str):
        if structured_sentinel in value:
            log.info(f'sentinel "{structured_sentinel}" found in {str(value)}. While it may not cause an issue, it is recommended to not use the sentinel in structured data.')
        value = value.replace(structured_sentinel, escaped_structured_sentinel)
    return value


def sf(*_args, **_kwargs) -> str:
    """
    Structured formatter helper function. When called with any number of positional or keyword arguments, creates a structured string representing those arguments.
    This is a short function name (sf) since it usually goes inside a logging call.
    Example code:
    question = "life"
    answer = 42
    :param _args: args
    :param _kwargs: kwargs
    """

    # make sure the sentinel isn't in the arguments
    args = []
    for s in _args:
        args.append(_get_escape_structured_sentinel(s))
    kwargs = {}
    for k, v in _kwargs.items():
        kwargs[_get_escape_structured_sentinel(k)] = _get_escape_structured_sentinel(v)

    output_list = []
    if len(args) > 0:
        args_string = _args_to_csv_string(args)
        output_list.append(args_string)
    if len(kwargs) > 0:
        # use json.dumps to handle special strings (e.g. embedded quotes)
        output_list.extend([structured_sentinel, json.dumps(kwargs, default=convert_serializable_special_cases), structured_sentinel])
    return " ".join(output_list)


def sf_separate(s: str) -> Tuple[Union[str, None], Union[str, None]]:
    """
    Separates a structured string into the args (as CSV string) and kwargs parts (as JSON, without sentinels).
    :param s: structured format string
    :return: a tuple of args (as list) and kwargs (as dict)
    """
    split_string = s.split(structured_sentinel)
    args_string = None
    kwargs_string = None
    if len(split_string) > 0:
        args_string = split_string[0].strip()
    if len(split_string) > 1:
        kwargs_string = split_string[1].strip()
    return args_string, kwargs_string
