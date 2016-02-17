from django.core.management import BaseCommand

from datapunt_generic.batch import batch

import datasets.themas.batch
import datasets.schiphol.batch
import datasets.bodeminformatie.batch
import datasets.geluidzone.batch
import datasets.veiligheidsafstanden.batch
import datasets.risicozones_bedrijven.batch
import datasets.risicozones_infrastructuur.batch


class Command(BaseCommand):
    ordered = [
        'themas',
        'schiphol',
        'bodeminformatie',
        'geluidzone',
        'risicozones_bedrijven',
        'risicozones_infrastructuur',
    ]

    imports = dict(
        themas=[
            datasets.themas.batch.ImportThemasJob,
        ],
        schiphol=[
            datasets.schiphol.batch.ImportSchipholJob,
        ],
        bodeminformatie=[
            datasets.bodeminformatie.batch.ImportBodeminformatieJob,
        ],
        geluidzone=[
            datasets.geluidzone.batch.ImportGeluidzoneJob,
        ],
        veiligheidsafstanden=[
            datasets.veiligheidsafstanden.batch.ImportVeiligheidsafstandenJob,
        ],
        risicozones_bedrijven=[
            datasets.risicozones_bedrijven.batch.ImportRisicozonesBedrijvenJob,
        ],
        risicozones_infrastructuur=[
            datasets.risicozones_infrastructuur.batch.ImportRisicozonesInfrastructuurJob,
        ],
    )

    def add_arguments(self, parser):
        parser.add_argument('dataset',
                            nargs='*',
                            default=self.ordered,
                            help="Dataset to import, choose from {}".format(', '.join(self.imports.keys())))

        parser.add_argument('--no-import',
                            action='store_false',
                            dest='run-import',
                            default=True,
                            help='Skip database importing')

    def handle(self, *args, **options):
        dataset = options['dataset']

        for ds in dataset:
            if ds not in self.imports.keys():
                self.stderr.write("Unkown dataset: {}".format(ds))
                return

        sets = [ds for ds in self.ordered if ds in dataset]     # enforce order

        self.stdout.write("Importing {}".format(", ".join(sets)))

        for ds in sets:
            if options['run-import']:
                for job_class in self.imports[ds]:
                    batch.execute(job_class())
