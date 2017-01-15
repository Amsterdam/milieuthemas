from collections import OrderedDict

from rest_framework import status
from rest_framework.test import APITestCase

from .. import batch


def test_response(testcase, response, expected_data):
    testcase.assertEqual(response.status_code, status.HTTP_200_OK)
    if expected_data:
        testcase.assertEqual(response.data, expected_data)


class ImportBomInslagTest(APITestCase):
    def setUp(self):
        batch.ImportInslagenTask(path='bommenkaart/csv/').execute()

    def test_overview(self):
        response = self.client.get('/milieuthemas/explosieven/inslagen/')
        test_response(self, response, None)
        data = response.data
        self.assertTrue('_links' in data)
        self.assertTrue('results' in data)
        self.assertEqual(len(data['results']), 25)
        self.assertEqual(data['results'][10]['dataset'], 'bommenkaart')
        self.assertEqual(data['results'][10]['kenmerk'], 'KR_430722011')
        self.assertEqual(data['results'][10]['type'], 'Krater')

    def test_first(self):
        response = self.client.get('/milieuthemas/explosieven/inslagen/1/')

        test_response(self, response, {
            '_links': OrderedDict([
                (
                    'self', {
                        'href': 'http://testserver/milieuthemas'
                                '/explosieven/inslagen/1/'
                    }
                )
            ]),
            'id': 1,
            'uri': 'https://api.datapunt.amsterdam.nl/milieuthemas'
                   '/explosieven/inslagen/1/',
            'bron': 'D-855_4042.jpg',
            'oorlogsinc': 'RAP_430717A',
            'type': 'Krater',
            'kenmerk': 'KR_430722001',
            'opmerkingen': '',
            'nauwkeurig': '5 meter',
            'datum': '1943-07-22',
            'pdf': 'https://atlas.amsterdam.nl/bommenkaart/RAP_430717A.pdf',
            'dataset': 'bommenkaart'
        })


class ImportGevrijwaardGebiedTest(APITestCase):
    def setUp(self):
        batch.ImportGevrijwaardTask(path='bommenkaart/csv/').execute()

    def test_overview(self):
        response = self.client.get('/milieuthemas'
                                   '/explosieven/gevrijwaardgebied/')
        test_response(self, response, None)
        data = response.data
        self.assertTrue('_links' in data)
        self.assertTrue('results' in data)
        self.assertEqual(len(data['results']), 19)
        self.assertEqual(data['results'][10]['dataset'], 'bommenkaart')
        self.assertEqual(data['results'][10]['kenmerk'], 'GG_009')
        self.assertEqual(data['results'][10]['type'], 'Vrijgave')

    def test_first(self):
        response = self.client.get('/milieuthemas'
                                   '/explosieven/gevrijwaardgebied/1/')

        test_response(self, response, {
            '_links': OrderedDict([('self', {
                'href': 'http://testserver/milieuthemas'
                        '/explosieven/gevrijwaardgebied/1/'})]),
            'id': 1,
            'uri': 'https://api.datapunt.amsterdam.nl/milieuthemas'
                   '/explosieven/gevrijwaardgebied/1/',
            'bron': '5150505-PVO-TEK-003',
            'kenmerk': 'GG_001A',
            'type': 'Vrijgave',
            'datum': '2015-07-10',
            'opmerkingen': 'Vrijgave tot 14,5 meter -mv '
                           'middels dieptedetectie en grondradar',
            'nauwkeurig': '',
            'dataset': 'bommenkaart'})


class ImportVerdachtGebiedTest(APITestCase):
    def setUp(self):
        batch.ImportVerdachtGebiedTask(path='bommenkaart/csv/').execute()

    def test_overview(self):
        response = self.client.get('/milieuthemas'
                                   '/explosieven/verdachtgebied/')
        test_response(self, response, None)
        data = response.data
        self.assertTrue('_links' in data)
        self.assertTrue('results' in data)
        self.assertEqual(len(data['results']), 4)
        self.assertEqual(data['results'][3]['dataset'], 'bommenkaart')
        self.assertEqual(data['results'][3]['kenmerk'], 'VGA_400815A')
        self.assertEqual(data['results'][3]['type'], 'Afwerpmunitie')

    def test_first(self):
        response = self.client.get('/milieuthemas'
                                   '/explosieven/verdachtgebied/1/')

        test_response(self, response, {
            '_links': OrderedDict([('self', {
                'href': 'http://testserver/milieuthemas'
                        '/explosieven/verdachtgebied/1/'})]),
            'id': 1,
            'uri': 'https://api.datapunt.amsterdam.nl'
                   '/milieuthemas/explosieven/verdachtgebied/1/',
            'bron': None,
            'kenmerk': 'VGA_400630B',
            'type': 'Afwerpmunitie',
            'afbakening': 'Blindganger',
            'aantal': '1 (blindganger)',
            'cartografie': '10 meter',
            'horizontaal': '25 meter (exc. Cartografische onnauwkeurigheid)',
            'kaliber': 'Onbekend',
            'subtype': 'Brisantbom(men)',
            'oorlogshandeling': 'RAP_400630B',
            'verschijning': 'Afgeworpen',
            'pdf': 'https://atlas.amsterdam.nl/bommenkaart/RAP_400630B.pdf',
            'dataset': 'bommenkaart'})


class ImportUitgevoedOnderzoekTest(APITestCase):
    def setUp(self):
        batch.ImportUitgevoerdOnderzoekTask(path='bommenkaart/csv/').execute()

    def test_overview(self):
        response = self.client.get('/milieuthemas'
                                   '/explosieven/uitgevoerdonderzoek/')
        test_response(self, response, None)
        data = response.data
        self.assertTrue('_links' in data)
        self.assertTrue('results' in data)
        self.assertEqual(len(data['results']), 9)
        self.assertEqual(data['results'][8]['dataset'], 'bommenkaart')
        self.assertEqual(data['results'][8]['kenmerk'], '-')
        self.assertEqual(data['results'][8]['type'], 'Detectie')

    def test_first(self):
        response = self.client.get('/milieuthemas'
                                   '/explosieven/uitgevoerdonderzoek/1/')

        test_response(self, response, {
            '_links': OrderedDict([('self', {
                'href': 'http://testserver/milieuthemas'
                        '/explosieven/uitgevoerdonderzoek/1/'})]),
            'id': 1,
            'uri': 'https://api.datapunt.amsterdam.nl/milieuthemas'
                   '/explosieven/uitgevoerdonderzoek/1/',
            'kenmerk': '128103',
            'type': 'Probleeminventarisatie',
            'opdrachtnemer': 'IBA',
            'verdacht_gebied': 'Gedeeltelijk',
            'onderzoeksgebied': 'Zeeburgereiland',
            'opdrachtgever': 'Projectbureau IJburg',
            'datum': '2006-01-06',
            'dataset': 'bommenkaart'})
