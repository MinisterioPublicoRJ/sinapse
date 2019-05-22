from collections import namedtuple
from unittest import TestCase

from solrclient.utils import solr2info
from solrclient.tests.fixtures import solr_pessoa_fisica


class ParseSolrResponse(TestCase):
    def test_parse_solr_response_of_person_to_info(self):
        """
            Transform the response from Solr API to info that will be
            used in get_person_photo and get_vehicle_photo functions
        """
        info = solr2info(
            solr_pessoa_fisica['pessoa']['response'],
            label='Pesoa',
            props=['uuid', 'rg']
        )

        info_obj = namedtuple('Pessoa', ['uuid', 'rg'])
        expected = [info_obj('3cffe', 123456)]

        self.assertEqual(info, expected)
