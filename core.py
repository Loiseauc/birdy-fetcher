#!/usr/bin/python

doc = """Core.

Usage:
  core [-v | -d ] [-f] [PATH] [DIRECTORY] [--nocache]
  core (-h | --help)

Examples:
  core -i ~/home/foo/

Arguments
  PATH
  DIRECTORY  bla

Options:
  -h --help  Show this screen.
  -v         verbose, print INFO, WARNING, ERROR and CRITICAL logs
  -d         Debug, print DEBUGG, INFO, WARNING, ERROR and CRITICAL logs
  -f         Print logs (if not, print logs in file 'converter.log')
  --nocache  Reload all ID.

"""

from docopt import docopt
from schema import Schema, And, Use, SchemaError, Optional
from subprocess import call
from db_fetcher import fetcher, config, converter

import os
import logging


def mkdir(path):
    command = 'mkdir ' + path
    call(command, shell=True)


def log(name, arg):
    if arg['-v']:
        level = logging.INFO
    elif arg['-d']:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    if arg['-f']:
        filelog = ''
    else:
        filelog = name

    logging.basicConfig(
        filename=filelog,
        format='%(asctime)s %(levelname)s:%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO)


def validation(args):
    """Data validation

    Checks arguments

    Args:
        args : all arguments

    Returns:
        right arguments
    """

    logging.info('Checks arguments')

    schema = Schema({
        Optional('n'): And(
            Use(int),
            lambda n: 1 <= n <= 50,
            error="'family_file_nb' should be an integer between 1 and 50"),
        Optional('m'): And(
            Use(int),
            lambda n: 1 <= n <= 50,
            error="'nb_align' should be an integer between 1 and 50"),
        Optional('fmt_conv'): And(list),
        Optional('search'): And(str, error='search sould be a string'),
        Optional('fpf'): And(
            Use(int), lambda n: 1 <= n <= 99,
            error='file_per_format should be an integer between 1 and 99'),
        Optional('dbN'): And(list, error='db_NCBI should be a list'),
        Optional('dbK'): And(list, error='db_KEGG should be a list'),
        Optional('cache'): And(bool, error='cache should be a boolean'),
        Optional('dataset'): And(
            str,
            lambda s: '.fasta' not in s,
            error="dataset can't contain '.fasta'"),
        Optional('fmt_fetch'): And(list),
        Optional('path'): And(os.path.exists, error='PATH should exist'),
        Optional('log_name'): And(
            Use(str), error="'log_name' sould be a string")})

    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    return args


def main():

    arg = docopt(doc)
    name = config.log_name
    convert = False
    formats_convert = [
        'CODATA', 'EMBL', 'GCG', 'GDE', 'GENBANK', 'IG', 'NBRF', 'RAW',
        'SWISSPROT', 'CLUSTAL', 'MEGA', 'MSF', 'NEXUS', 'PHYLIP', 'STOCKHOLM']
    # cache = arg['--nocache']
    cache = config.cache
    log(name, arg)
    logging.info('Arguments validation')
    if arg['PATH']:
        path = arg['PATH']
        pathverif = arg['PATH']
    else:
        path = config.path
        pathverif = './' + path

    if arg['DIRECTORY']:
        directory = path + arg['DIRECTORY'] + '/'
    else:
        directory = path + config.dataset + '/'

    args = {
        'n': config.family_file_nb,
        'm': config.nb_align,
        'fmt_conv': config.formats_converter,
        'search': config.search,
        'fpf': config.file_per_format,
        'dbN': config.db_NCBI,
        'dbK': config.db_KEGG,
        'cache': cache,
        'dataset': config.dataset,
        'fmt_fetch': config.formats_fetcher,
        'path': pathverif,
        'log_name': config.log_name}

    args = validation(args)

    mkdir(directory)
    logging.info('Arguments validation ... ok\n')

    logging.info('Started : fetcher')
    #fetcher.main(directory, cache)
    logging.info('Fetcher ... ok\n')    

    for fmt in config.formats_converter:
        if fmt in formats_convert:
            convert = True
    if convert:
        logging.info('Started : converter')
        converter.main(directory, cache)
        logging.info('Converter ... ok\n') 

    logging.info('The End\n\n\n\n\n')

if __name__ == "__main__":
    # execute only if run as a script
    main()