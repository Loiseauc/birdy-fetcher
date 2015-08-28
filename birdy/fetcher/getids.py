import os
import logging

from .. import config

def get_ids_from_env(birdy_ids):

	environ_variable_id = os.environ.get(birdy_ids, None)
	logging.info(birdy_ids)
	logging.info(environ_variable_id)
	if environ_variable_id is None:
		ids = None
	else:
		ids = environ_variable_id.split(':')
	return ids
