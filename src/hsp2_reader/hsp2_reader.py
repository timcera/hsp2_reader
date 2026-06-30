"""Collection of functions for reading different time series from HSP2 results in a HDF5 file."""

import os.path as _os_path
import sys as _sys
import warnings as _warnings

import pandas as pd

from hsp2_reader.toolbox_utils.src.toolbox_utils import tsutils
from hsp2_reader.toolbox_utils.src.toolbox_utils.readers.hdf5 import hdf5 as _hdf5

_warnings.filterwarnings("ignore")


def about():
    """Display version number and system information."""
    return tsutils.about("hsp2_reader")


@tsutils.doc(tsutils.docstrings)
def hdf5(hdf5path, interval, *labels, **kwds):
    r"""
    Prints out data to the screen from a HDF5 file.

    Parameters
    ----------
    hdf5path : str
        The HSP2 formatted HDF5 binary output file.  This file must have been
        created from a completed model run.
    interval : str
        One of 'yearly', 'monthly', 'daily', or 'bivl'.  The 'bivl' option
        is a sub-daily interval defined in the UCI file.  Typically 'bivl'
        is used for hourly output, but can be set to any value that evenly
        divides into a day and needs to match the BIVL setting in the model
        run.
    labels : str
        The remaining arguments uniquely identify a time-series in the
        binary file.  The format is
        'OPERATIONTYPE,ID,VARIABLEGROUP,VARIABLE'.

        For example: 'PERLND,101,PWATER,UZS IMPLND,101,IWATER,RETS'

        Leaving a section without an entry will wild card that
        specification.  To get all the PWATER variables for PERLND 101 the
        label would use::

            PERLND,101,PWATER,

        To get TAET for all PERLNDs::

            PERLND,,,TAET

        Note that there are spaces ONLY between label specifications not
        within the labels themselves.

        +-----------------------+-------------------------------+
        | OPERATIONTYPE         | VARIABLEGROUP                 |
        +=======================+===============================+
        | PERLND                | ATEMP, SNOW, PWATER, SEDMNT,  |
        |                       | PSTEMP, PWTGAS, PQUAL,        |
        |                       | MSTLAY, PEST, NITR, PHOS,     |
        |                       | TRACER                        |
        +-----------------------+-------------------------------+
        | IMPLND                | ATEMP, SNOW, IWATER, SOLIDS,  |
        |                       | IWTGAS, IQUAL                 |
        +-----------------------+-------------------------------+
        | RCHRES                | HYDR, CONS, HTRCH, SEDTRN,    |
        |                       | GQUAL, OXRX, NUTRX, PLANK,    |
        |                       | PHCARB, INFLOW, OFLOW, ROFLOW |
        +-----------------------+-------------------------------+
        | BMPRAC                | Not used Have to leave        |
        |                       | VARIABLEGROUP as a wild card. |
        |                       | For example,                  |
        |                       | 'BMPRAC,875,,RMVOL'           |
        +-----------------------+-------------------------------+

        The Time Series Catalog in the HSPF Manual lists all of the
        variables in each of these VARIABLEGROUPs.  For BMPRAC, all of the
        variables in all Groups in the Catalog are available in the unnamed
        (blank) Group.

        ID is the operation type identification number specified in the UCI
        file.

        Here, the user can specify:

        - a single ID number to match (1-999)
        - no entry, matching all ID's in the HDF5 file
        - a range, specified as any combination of integers and
          groups of integers marked as "start:end", with multiple
          allowed sub-ranges separated by the "+" sign.

        +------------------+-------------------------+
        | Example Label ID | Expands to:             |
        +==================+=========================+
        | 1:10             | 1,2,3,4,5,6,7,8,9,10    |
        +------------------+-------------------------+
        | 11:14+19:22      | 11,12,13,14,19,20,21,22 |
        +------------------+-------------------------+
        | 3:5+7            | 3,4,5,7                 |
        +------------------+-------------------------+

    ${start_date}
    ${end_date}
    sort_columns:
        [optional, default is False]

        If set to False will maintain the columns order of the labels.  If
        set to True will sort all columns by their columns names.
    """
    try:
        start_date = kwds.pop("start_date")
    except KeyError:
        start_date = None
    try:
        end_date = kwds.pop("end_date")
    except KeyError:
        end_date = None
    try:
        sort_columns = kwds.pop("sort_columns")
    except KeyError:
        sort_columns = False
    if kwds:
        raise ValueError(
            tsutils.error_wrapper(
                f"""
                The only allowed keywords are start_date and end_date.  You
                have given {kwds}.
                """
            )
        )

    labels = tsutils.make_list(labels)

    result = pd.DataFrame()
    for lab in [labels]:
        nts = _hdf5(hdf5path, interval, lab, sort_columns=sort_columns)
        result = result.join(nts, how="outer")
    result = tsutils.common_kwds(result, start_date=start_date, end_date=end_date)
    return tsutils.asbestfreq(result)


def main():
    """Set debug, register *_cli functions, and run cltoolbox.main function."""
    from argparse import RawTextHelpFormatter

    import cltoolbox

    if not _os_path.exists("debug_hsp2_reader"):
        _sys.tracebacklimit = 0

    tablefmt_docstring = r"""[optional, default is 'cvs_nos']

The table format.  Can be one of 'csv', 'tsv', 'csv_nos', 'tsv_nos',
'plain', 'simple', 'github', 'grid', 'fancy_grid', 'pipe', 'orgtbl',
'jira', 'presto', 'psql', 'rst', 'mediawiki', 'moinmoin', 'youtrack',
'html', 'latex', 'latex_raw', 'latex_booktabs' and 'textile'."""
    float_format_docstring = r"""[optional, default is 'g']

The format for floating point numbers in the output table."""

    @cltoolbox.command("about")
    def _about_cli():
        """Display version number and system information."""
        about_dict = about()
        for key in about_dict:
            print(f"{key}: {about_dict[key]}")

    @cltoolbox.command("hdf5", formatter_class=RawTextHelpFormatter)
    @cltoolbox.arg("tablefmt", help=tablefmt_docstring)
    @cltoolbox.arg("float_format", help=float_format_docstring)
    @tsutils.copy_doc(hdf5)
    def _hdf5_cli(
        hdf5path,
        interval,
        start_date=None,
        end_date=None,
        sort_columns=False,
        tablefmt="csv_nos",
        float_format="g",
        *labels,
    ):
        tsutils.printiso(
            hdf5(
                hdf5path,
                interval,
                *labels,
                start_date=start_date,
                end_date=end_date,
                sort_columns=sort_columns,
            ),
            tablefmt=tablefmt,
            float_format=float_format,
        )


    cltoolbox.main()


if __name__ == "__main__":
    main()
