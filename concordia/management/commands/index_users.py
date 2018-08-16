from pyelasticsearch import ElasticSearch, IndexAlreadyExistsError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '''
    Create an elastic search index to track total number of users.
    
    The index will track total number of registered users (+1 anonymous user).
    '''

    def add_arguments(self, parser):
        parser.add_argument(
            '--es-host',
            required=True,
            default='http://localhost:9200/',
            dest='es_host',
            help='Name of the index to track registered users',
        )
        parser.add_argument(
            '--index-name',
            required=True,
            dest='index_name',
            help='Name of the index to track registered users',
        )

    def handle(self, *args, **options):
        index_name = options['index_name']
        es_host = options['es_host']

        es = ElasticSearch(es_host)

        try:
            # TODO: determine settings key value pairs dict
            # TODO: determine query_params (mappings) key value pairs dict
            es.create_index(index=index_name, settings={}, query_params={})
        except IndexAlreadyExistsError as _:
            self.stdout.write(
                'Skipping index creation because it already exists.')
