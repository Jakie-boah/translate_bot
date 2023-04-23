from dotenv import load_dotenv
import os
from pyairtable import Table
from pyairtable.formulas import match
load_dotenv()


class AirtableParser:

    airtable_api_key = os.getenv('airtable_api_key')
    base_id = 'app91VxghIKC1C1q4'
    table_name = 'City'

    def __init__(self, tg_id):
        self.tg_id = tg_id

    @classmethod
    def _get_table(cls):
        table = Table(cls.airtable_api_key, cls.base_id, cls.table_name)
        return table

    def get_dict(self):
        table = self._get_table()
        formula = match({"IDtg": f"{self.tg_id}"})
        row = table.first(formula=formula, view='viw1Tvc8dmggJm9pe')
        return self._parse_themes(row)

    @staticmethod
    def _parse_themes(row):

        AirtableParser.validate_on_themes(row)
        themes = row['fields']['Themes']
        theme_field = themes.split(', ')
        translate_dict = {}
        for lan_con in theme_field:
            lan_row = lan_con.split('-')
            translate_dict[int(lan_row[1])] = lan_row[0]

        return translate_dict

    @staticmethod
    def validate_on_themes(row):
        try:
            row['fields']['Themes']
        except KeyError:
            raise KeyError('Клетка Themes не заполнена')
#
#
a = (AirtableParser(-1001728616773).get_dict())
print(a)