from rest_framework.test import APITestCase, APITransactionTestCase

from datasets.bommenkaart import batch
from datasets.bommenkaart.batch import TEST_INSLAGEN_PATH, TEST_GEVRIJWAARD_GEBIED_PATH, TEST_VERDACHTE_GEBIEDEN_PATH, \
    TEST_UITGEVOERD_ONDERZOEK_PATH


class BrowseDatasetsTestCase(APITransactionTestCase):
    """
    Verifies that browsing the API works correctly.
    """
    root = 'milieuthemas'
    datasets = [
        'explosieven/inslagen',
        'explosieven/gevrijwaardgebied',
        'explosieven/verdachtgebied',
        'explosieven/uitgevoerdonderzoek'
    ]

    def setUp(self):
        batch.ImportInslagenTask(path=TEST_INSLAGEN_PATH).execute()
        batch.ImportGevrijwaardTask(path=TEST_GEVRIJWAARD_GEBIED_PATH).execute()
        batch.ImportVerdachtGebiedTask(path=TEST_VERDACHTE_GEBIEDEN_PATH).execute()
        batch.ImportUitgevoerdOnderzoekTask(path=TEST_UITGEVOERD_ONDERZOEK_PATH).execute()
        # pass

    def test_root(self):
        response = self.client.get('/{}/'.format(self.root))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        for url in self.datasets:
            self.assertIn(url, response.data)

    def test_dataset_root(self):

        for url in self.datasets:
            response = self.client.get('/{}/{}/?format=api'.format(
                self.root, url))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response['Content-Type'], 'text/html; charset=utf-8')

    def test_lists(self):
        for url in self.datasets:
            response = self.client.get('/{}/{}/'.format(self.root, url))

            self.assertEqual(response.status_code, 200,
                             'Wrong response code for {}'.format(url))
            self.assertEqual(response['Content-Type'], 'application/json',
                             'Wrong Content-Type for {}'.format(url))

            self.assertIn('count', response.data,
                          'No count attribute in {}'.format(url))
            self.assertNotEqual(response.data['count'], 0,
                                'Wrong result count for {}'.format(url))

    def test_details(self):
        for url in self.datasets:
            response = self.client.get('/{}/{}/'.format(self.root, url))

            url = response.data['results'][0]['_links']['self']['href']
            detail = self.client.get(url)

            self.assertEqual(detail.status_code, 200,
                             'Wrong response code for {}'.format(url))
            self.assertEqual(detail['Content-Type'], 'application/json',
                             'Wrong Content-Type for {}'.format(url))
            self.assertIn('id', detail.data)
