import json

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from urban_environment.models import Alerts


@api_view(['GET', 'POST', 'PATCH'])
def alerts(request, alert_id=None):
    if request.method == 'GET':
        # help tip - DON'T FORGOT TO DELETE
        # Tem de permitir a filtragem de ocorrencias por autor, por categoria e por localizacao (raio de alcance)

        to_return = []

        author = request.POST.get('author', None)
        category = request.POST.get('category', None)
        # longitude = request.POST.get('longitude', 0)
        # latitude = request.POST.get('latitude', 0)
        # radius = request.POST.get('radius', 10)

        source = Alerts.objects

        if author:
            source.filter(author=author)

        if category:
            source.filter(category=category)

        # if longitude and latitude and radius:
        #    source.filter(location__distance_lt=(Point(longitude, latitude), Distance(Km=radius)))

        for a in source:
            to_return.append(a)

        return Response(json.dumps({"message": to_return}))

    elif request.method == 'POST':
        # help tip - DON'T FORGOT TO DELETE
        # Tem de permitir a adicao de ocorrencias (com a localizacao geografica, e autor associados). Nota: O
        # estado default sera sempre por validar quando estas sao criadas.
        if request.user.is_staff:
            # longitude = request.POST.get('longitude', 0)
            # latitude = request.POST.get('latitude', 0)

            a = Alerts()
            a.description = request.POST.get('description', None)
            # a.location = Point(longitude, latitude, srid=4326)
            a.author = request.user

            a.save()

            if a.id:
                return Response(json.dumps({"message": "__success__"}), status=status.HTTP_201_CREATED)
            else:
                return Response(json.dumps({"message": "__permissions_in_fault__"}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(json.dumps({"message": "__permissions_in_fault__"}), status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'PATCH':
        # help tip - DON'T FORGOT TO DELETE
        # Tem de permitir a actualizacao de ocorrencias (para mudar o estado das mesmas para "validadas" por
        # um administrador do sistema)

        if request.user.is_staff:
            post_status = request.POST.get('status', None)
            post_status = Alerts.STATUS_CHOICES.get(post_status, None)

            if post_status:
                if alert_id:
                    try:
                        a = Alerts.objects.get(id=alert_id)
                    except Alerts.DoesNotExist:
                        return Response(json.dumps({"message": "__entry_not_found__"}), status=status.HTTP_404_NOT_FOUND)
                    else:
                        a.status = post_status
            else:
                return Response(json.dumps({"message": "__fields_in_fault__"}), status=status.HTTP_400_BAD_REQUEST)

        return Response(json.dumps({"message": "__permissions_in_fault__"}), status=status.HTTP_403_FORBIDDEN)
