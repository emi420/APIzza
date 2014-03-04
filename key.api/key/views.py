from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from key.models import App

@api_view(['GET'])
def check_key(request):
    ''' Check if a key is valid '''

    app = request.META.get('HTTP_X_VOOLKS_APP_ID')
    key = request.META.get('HTTP_X_VOOLKS_API_KEY')

    # If parameters missing, return error

    if not app or not key:
        return Response({'code':1,'text': 'Parameters not found'},status=status.HTTP_400_BAD_REQUEST)

    try:

        # Get and return App object

        app = App.objects.get(id_aplicacion=app,api_key=key)
        return Response({'id': app.id},status=status.HTTP_200_OK)

    except App.DoesNotExist:

        # Or an error if App doesn't exist

        return Response({'code':2,'text': 'Incorrect parameters'},status=status.HTTP_400_BAD_REQUEST)

