from django_elasticsearch_dsl import DocType, Index, fields
from django.contrib.auth.models import User
from concordia.models import Asset, Collection

# Name of the Elasticsearch index
user = Index('users')
# See Elasticsearch Indices API reference for available settings
user.settings(
    number_of_shards=1,
    number_of_replicas=0
)

collection = Index('collections')
collection.settings(
    number_of_shards=1,
    number_of_replicas=0
)

asset = Index('assets')
asset.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@user.doc_type
class UserDocument(DocType):
    class Meta:
        model = User  # The model associated with this DocType

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'last_login',
            'date_joined'
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True
        # Don't perform an index refresh after every update
        # (overrides global setting):
        # auto_refresh = False
        # Paginate the django queryset used to populate the index with
        # the specified size
        # (by default there is no pagination)
        # queryset_pagination = 5000


@collection.doc_type
class CollectionDocument(DocType):
    class Meta:
        model = Collection

        fields = [
            'title',
            'slug',
            'status'
        ]


@asset.doc_type
class AssetDocument(DocType):
    collection = fields.ObjectField(properties={
        'title': fields.TextField(),
        'slug': fields.TextField(),
    })

    class Meta:
        model = Asset

        fields = [
            'title',
            'slug',
            'status',
            'sequence'
        ]

        related_models = [Collection]

    def get_queryset(self):
        """
        Not mandatory but to improve performance we can select related
        in one sql request.
        """
        return super(AssetDocument, self).get_queryset().select_related(
            'collection'
        )

    def get_instances_from_related(self, related_instance):
        """
        If related_models is set, define how to retrieve the Car instance(s)
        from the related model. The related_models option should be used with
        caution because it can lead in the index to the updating
        of a lot of items.
        """
        if isinstance(related_instance, Collection):
            return related_instance.asset_set.all()
