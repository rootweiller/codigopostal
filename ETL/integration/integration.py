import logging
import os
from asyncio import sleep
from datetime import datetime

import requests
from decouple import config

from ETL import constants
from ETL.integration.models import ConfigDatabase, FileUploader, PostCode, Code, PostCodeRAW, Country
from ETL.integration.parser import ParserCSV


class IntegrationPostCode:
    """
    class for integration API
    """

    def __init__(self, file_id):

        self.db = ConfigDatabase()
        self.file_path = config('FILES', None)
        self.parser = ParserCSV()
        self.url = config('URL_POSTCODE')
        self.file_id = file_id

    def execute(self):
        pending_files = self.db.session.query(FileUploader).filter(
            FileUploader.processed.is_(False), FileUploader.id == self.file_id).all()
        if pending_files:
            self.extract_data()
        else:
            logging.info("No pending files to process")

    def extract_data(self):
        extract_data_csv = self.parser.read_files(self.file_path)
        if extract_data_csv:
            logging.info("Extract data succeeded")

    def get_postcode_api(self, data_type):
        data_api = self.db.session.query(PostCode).filter(PostCode.processed.is_(False)).limit(10000)
        for item in data_api:
            result = self.connect_postcode(item, data_type)
            if result:
                self.transform_load_csv(result[0])
                self.update_postcode(item)
            else:
                print("Location not Found %s" % item)

    def update_postcode(self, item):
        try:
            self.db.session.query(PostCode).filter(PostCode.id == item.id).update({
                'processed': True
            })
            self.db.session.commit()
        except Exception as error:
            self.db.session.rollback()
            logging.info("Not working save into DB {0} with error {1}".format(item.id, error))

    def connect_postcode(self, item, data_type):
        url = self.url + data_type +'?longitude={0}&latitude={1}'.format(item.lon, item.lat)

        response = requests.get(url)
        if response.status_code == 200:
            r = response.json()
            result = r['result']
            self.load_data_raw(r, data_type, item.id)
            return result
        else:
            return None

    def transform_load_csv(self, data):
        country = self.add_country(data['country'])
        try:
            data = Code(postcode=data['outcode'],
                        country=country, latitude=data['latitude'], longitude=data['longitude'],
                        created_at=datetime.now())
            self.db.session.add(data)
            self.db.session.commit()
        except Exception as error:
            print("Error when %s" % error)
            self.db.session.rollback()
            raise

    def add_country(self, countries):
        for item in countries:
            country = self.db.session.query(Country).filter(Country.name == item).first()
            if country:
                return country
            else:
                add_country = Country(name=item, created_at=datetime.utcnow())
                self.db.session.add(add_country)
                self.db.session.commit()
                return add_country

    def load_data_raw(self, data, data_type, _id):
        try:
            data = PostCodeRAW(postcode_id=_id, data_type=data_type, json_data=data, created_at=datetime.now())
            self.db.session.add(data)
            self.db.session.commit()
        except Exception as error:
            print("Error when %s" % error)
            self.db.session.rollback()
            raise

