import sys

from ETL import constants
from ETL.integration.integration import IntegrationPostCode

file_id = int(sys.argv[1])

IntegrationPostCode(file_id).get_postcode_api(constants.DATA_TYPE)
