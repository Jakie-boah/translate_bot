from dotenv import load_dotenv
import os
from pyairtable import Table
from pyairtable.formulas import match
from loguru import logger
load_dotenv()
import json


class AirtableParser:

    airtable_api_key = os.getenv('airtable_api_key')
    base_id = 'app91VxghIKC1C1q4'
    table_name = 'City'

    def __init__(self, tg_id=None):
        self.tg_id = tg_id

    @classmethod
    def _get_table(cls):
        table = Table(cls.airtable_api_key, cls.base_id, cls.table_name)
        return table

    async def update_table(self):
        table = self._get_table()
        records = table.all(view='Grid 2 copy')
        json_dump = {}

        for record in records:
            try:
                json_dump[record['fields']['IDtg']] = record['fields']['Themes']
            except KeyError:
                pass

        with open('handlers/data.json', 'w') as f:
            json.dump(json_dump, f)

        logger.success('Данные обновлены')

    def get_dict(self):
        with open('handlers/data.json') as f:
            json_dump = json.load(f)

        return self._parse_themes(json_dump[str(self.tg_id)])

    @staticmethod
    def _parse_themes(row):

        # AirtableParser.validate_on_themes(row)
        themes = row
        theme_field = themes.split(', ')
        translate_dict = {}
        for lan_con in theme_field:
            # translate_dict.append(lan_con)
            translate_dict[lan_con[:2]] = lan_con

        return translate_dict

    @staticmethod
    def validate_on_themes(row):
        try:
            row['fields']['Themes']
        except KeyError:
            raise KeyError('Клетка Themes не заполнена')
#
