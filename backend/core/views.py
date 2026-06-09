from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_home(request):
    return Response({
        'project': 'EduRPG Platform',
        'status': 'Backend is working',
        'version': '0.1.0',
        'modules': [
            'users',
            'subjects',
            'quests',
            'duels',
            'shop',
            'leaderboard',
        ]
    })