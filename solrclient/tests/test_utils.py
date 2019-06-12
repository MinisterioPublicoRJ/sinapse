from collections import namedtuple
from unittest import TestCase

from solrclient.utils import solr2info
from solrclient.tests.fixtures import (
    solr_pessoa_fisica,
    solr_veiculo,
    solr_pessoa_fisica_2
)


class ParseSolrResponse(TestCase):
    def test_parse_solr_response_of_person_to_info(self):
        """
            Transform the response from Solr API to info that will be
            used in get_person_photo and get_vehicle_photo functions
        """
        info = solr2info(
            solr_pessoa_fisica['pessoa'],
            label='Pessoa',
            props=['uuid', 'rg']
        )

        info_obj = namedtuple('Pessoa', ['uuid', 'rg'])
        expected = [info_obj('3cffe', '123456')._asdict()]

        self.assertEqual(info, expected)

    def test_parse_solr_response_of_vehicle_to_info(self):
        """
            Transform the response from Solr API to info that will be
            used in get_person_photo and get_vehicle_photo functions
        """
        info = solr2info(
            solr_veiculo['veiculo'],
            label='Veiculo',
            props=['uuid', 'marca_modelo', 'ano_modelo', 'cor']
        )

        info_obj = namedtuple(
            'Veiculo',
            ['uuid', 'marca_modelo', 'ano_modelo', 'cor']
        )
        expected = [
            info_obj('3ad66', "HONDA/CG 125 FAN ESD", "2014", "PRETA")._asdict(),
            info_obj('37464', "CITROEN/XSARA PICASSO GX", "2001", "CINZA")._asdict()
        ]

        self.assertEqual(info, expected)

    def test_parse_solr_response_ignore_person_without_rg(self):
        """
            Ignore persons without rg
        """
        info = solr2info(
            solr_pessoa_fisica_2['pessoa'],
            label='Pesoa',
            props=['uuid', 'rg']
        )

        info_obj = namedtuple('Pessoa', ['uuid', 'rg'])
        expected = [info_obj('3cffe', '123456')._asdict()]

        self.assertEqual(info, expected)
