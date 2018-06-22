from .tasks import download_async_collection, check_completeness
from rest_framework.decorators import api_view

@api_view(['POST'])
def download_collection(request):
    url = request.data.get('url', None)
    if not url:
        return Response({'message':'Please provide valid url'})
    try:
        result = download_async_collection.delay(url)
        result.ready()
        result.get()
        result2 = check_completeness.delay()
        result2.ready()
        result2.get()
    except Exception as e:
        pass
    return Response({'message': 'Job Started Successfully',
                    'task_id':result.task_id})
