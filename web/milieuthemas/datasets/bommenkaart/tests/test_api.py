from collections import OrderedDict

from rest_framework import status
from rest_framework.test import APITestCase

from datasets.bommenkaart import batch


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
        self.assertEqual(data['results'][10]['_display'], 'KR_430722011')
        self.assertEqual(data['results'][10]['dataset'], 'bommenkaart')
        self.assertEqual(data['results'][10]['kenmerk'], 'KR_430722011')
        self.assertEqual(data['results'][10]['type'], 'Krater')

    def test_first(self):
        response = self.client.get('/milieuthemas/explosieven/inslagen/1/')
        print(response.data)
        test_response(self, response, {
            '_display': 'KR_430722001',
            '_links': OrderedDict([
                (
                    'self', {
                        'href': 'http://testserver/milieuthemas'
                                '/explosieven/inslagen/1/'
                    }
                )
            ]),
            'id': 1,
            'bron': 'D-855_4042.jpg',
            'oorlogsinc': 'RAP_430717A',
            'type': 'Krater',
            'kenmerk': 'KR_430722001',
            'opmerkingen': '',
            'nauwkeurig': '5 meter',
            'datum': '1943-07-22',
            'datum_inslag': None,
            'pdf': 'https://data.amsterdam.nl/bommenkaart/RAP_430717A.pdf',
            'intekening': 'Luchtfoto',
            'geometrie': {
                'type': 'Point',
                'coordinates': [
                    122060.259199999,
                    489504.4465
                ]
            },
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
        self.assertEqual(data['results'][10]['_display'], 'GG_009')
        self.assertEqual(data['results'][10]['dataset'], 'bommenkaart')
        self.assertEqual(data['results'][10]['kenmerk'], 'GG_009')
        self.assertEqual(data['results'][10]['type'], 'Vrijgave')

    def test_first(self):
        response = self.client.get('/milieuthemas'
                                   '/explosieven/gevrijwaardgebied/1/')

        test_response(self, response, {
            '_display': 'GG_001A',
            '_links': OrderedDict([('self', {
                'href': 'http://testserver/milieuthemas'
                        '/explosieven/gevrijwaardgebied/1/'})]),
            'id': 1,
            'bron': '5150505-PVO-TEK-003',
            'kenmerk': 'GG_001A',
            'type': 'Vrijgave',
            'datum': '2015-07-10',
            'opmerkingen': 'Vrijgave tot 14,5 meter -mv '
                           'middels dieptedetectie en grondradar',
            'nauwkeurig': '',
            'intekening': 'Kaartmateriaal',
            'geometrie': {
                'type': 'MultiPolygon', 'coordinates': [
                    [[
                        [122171.601500001, 490002.997099999],
                        [122102.783199999, 489895.681899998],
                        [122063.968699999, 489920.685],
                        [122132.548900001, 490027.7621],
                        [122171.601500001, 490002.997099999]
                    ]],
                    [[
                        [122129.7707, 490041.9703],
                        [122050.0781, 489917.271899998],
                        [122041.346799999, 489922.986900002],
                        [122121.039500002, 490047.209100001],
                        [122129.7707, 490041.9703]
                    ], [
                        [122085.8488, 489976.401700001],
                        [122085.696600001, 489976.526799999],
                        [122085.444643167, 489976.648263474],
                        [122085.175666507, 489976.724991428],
                        [122084.897546355, 489976.754737068],
                        [122084.618426786, 489976.736629364],
                        [122084.346481145, 489976.671198558],
                        [122084.089672702, 489976.560360631],
                        [122083.855521473, 489976.407361207],
                        [122083.65088401, 489976.216680502],
                        [122083.481752628, 489975.993902141],
                        [122083.353079931, 489975.745549651],
                        [122083.268633789, 489975.478895434],
                        [122083.230887002, 489975.201747816],
                        [122083.240944894, 489974.922222395],
                        [122083.298512945, 489974.648504398],
                        [122083.401905412, 489974.388608995],
                        [122083.548094697, 489974.150146598],
                        [122083.732799999, 489973.940099999],
                        [122083.962868904, 489973.788587571],
                        [122084.215230079, 489973.678126926],
                        [122084.482626737, 489973.611894424],
                        [122084.757369735, 489973.591794619],
                        [122085.031558681, 489973.61840549],
                        [122085.297309118, 489973.690961828],
                        [122085.546979241, 489973.807377234],
                        [122085.773389643, 489973.964304116],
                        [122085.970029766, 489974.157229954],
                        [122086.131245111, 489974.380607056],
                        [122086.25239984, 489974.628012086],
                        [122086.330010078, 489974.892330771],
                        [122086.361844101, 489975.16596248],
                        [122086.346986502, 489975.441038776],
                        [122086.285864521, 489975.709649685],
                        [122086.180235754, 489975.964071147],
                        [122086.033137617, 489976.19698713],
                        [122085.8488, 489976.401700001]
                    ]]
                ]
            },
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
        self.assertEqual(data['results'][3]['_display'], 'VGA_400815A')
        self.assertEqual(data['results'][3]['dataset'], 'bommenkaart')
        self.assertEqual(data['results'][3]['kenmerk'], 'VGA_400815A')
        self.assertEqual(data['results'][3]['type'], 'Afwerpmunitie')

    def test_first(self):
        response = self.client.get('/milieuthemas'
                                   '/explosieven/verdachtgebied/1/')

        test_response(self, response, {
            '_display': 'VGA_400630B',
            '_links': OrderedDict([('self', {
                'href': 'http://testserver/milieuthemas'
                        '/explosieven/verdachtgebied/1/'})]),
            'id': 1,
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
            'pdf': 'https://data.amsterdam.nl/bommenkaart/RAP_400630B.pdf',
            'opmerkingen': 'afbakening conform Saricon 11S037-VO-01',
            'geometrie': {
                'type': 'MultiPolygon',
                'coordinates': [[[
                    [125802.0, 489744.0],
                    [125807.216479316, 489743.609078918],
                    [125812.316431104, 489742.445048203],
                    [125817.185930869, 489740.533910377],
                    [125821.716202032, 489737.918357101],
                    [125825.806045822, 489734.656815514],
                    [125829.364101886, 489730.822143065],
                    [125832.310889132, 489726.5],
                    [125834.580581203, 489721.786935853],
                    [125836.122476926, 489716.788232688],
                    [125836.902132901, 489711.615553276],
                    [125836.902132901, 489706.384446724],
                    [125836.122476926, 489701.211767312],
                    [125834.580581203, 489696.213064147],
                    [125832.310889132, 489691.5],
                    [125829.364101886, 489687.177856935],
                    [125825.806045822, 489683.343184486],
                    [125821.716202032, 489680.081642899],
                    [125817.185930869, 489677.466089623],
                    [125812.316431104, 489675.554951797],
                    [125807.216479316, 489674.390921082],
                    [125802.0, 489674.0],
                    [125796.783520684, 489674.390921082],
                    [125791.683568896, 489675.554951797],
                    [125786.814069131, 489677.466089623],
                    [125782.283797968, 489680.081642899],
                    [125778.193954178, 489683.343184486],
                    [125774.635898114, 489687.177856935],
                    [125771.689110868, 489691.5],
                    [125769.419418797, 489696.213064147],
                    [125767.877523074, 489701.211767312],
                    [125767.097867099, 489706.384446724],
                    [125767.097867099, 489711.615553276],
                    [125767.877523074, 489716.788232688],
                    [125769.419418797, 489721.786935853],
                    [125771.689110868, 489726.5],
                    [125774.635898114, 489730.822143065],
                    [125778.193954178, 489734.656815514],
                    [125782.283797968, 489737.918357101],
                    [125786.814069131, 489740.533910377],
                    [125791.683568896, 489742.445048203],
                    [125796.783520684, 489743.609078918],
                    [125802.0, 489744.0]
                ]]]},
            'dataset': 'bommenkaart'})

    class ImportUitgevoedOnderzoekTest(APITestCase):
        def setUp(self):
            batch.ImportUitgevoerdOnderzoekTask(
                path='bommenkaart/csv/').execute()

        def test_overview(self):
            response = self.client.get('/milieuthemas'
                                       '/explosieven/uitgevoerdonderzoek/')
            test_response(self, response, None)
            data = response.data
            self.assertTrue('_links' in data)
            self.assertTrue('results' in data)
            self.assertEqual(len(data['results']), 9)
            self.assertEqual(data['results'][8]['_display'], '-')
            self.assertEqual(data['results'][8]['dataset'], 'bommenkaart')
            self.assertEqual(data['results'][8]['kenmerk'], '-')
            self.assertEqual(data['results'][8]['type'], 'Detectie')

        def test_first(self):
            response = self.client.get('/milieuthemas'
                                       '/explosieven/uitgevoerdonderzoek/1/')

            test_response(self, response, {
                '_display': '128103',
                '_links': OrderedDict([('self', {
                    'href': 'http://testserver/milieuthemas'
                            '/explosieven/uitgevoerdonderzoek/1/'})]),
                'id': 1,
                'kenmerk': '128103',
                'type': 'Probleeminventarisatie',
                'opdrachtnemer': 'IBA',
                'verdacht_gebied': 'Gedeeltelijk',
                'onderzoeksgebied': 'Zeeburgereiland',
                'opdrachtgever': 'Projectbureau IJburg',
                'datum': '2006-01-06',
                'geometrie': {
                    'type': 'MultiPolygon', 'coordinates': [
                        [[
                            [125804.538400002, 488112.9804],
                            [127097.999200001, 486977.0986],
                            [127252.295299999, 486878.611699998],
                            [127193.203200001, 486835.934099998],
                            [125725.7489, 486812.9538],
                            [125758.577799998, 486904.874899998],
                            [125653.525199998, 487679.6382],
                            [125620.696199998, 487692.7698],
                            [125597.716, 487879.894900002],
                            [125804.538400002, 488112.9804]
                        ]]
                    ]},
                'dataset': 'bommenkaart'})
