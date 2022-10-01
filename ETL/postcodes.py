import sys

from ETL.integration.integration import IntegrationPostCode

file_id = int(sys.argv[1])

IntegrationPostCode(file_id).execute()
