import json

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.core.serializers import serialize

from urban_environment.models import Alerts


@api_view(['GET', 'POST', 'PATCH'])
@permission_classes((permissions.AllowAny,))
def alerts(request, alert_id=None):
    if request.method == 'GET':
        # help tip - DON'T FORGOT TO DELETE
        # Tem de permitir a filtragem de ocorrencias por autor, por categoria e por localizacao (raio de alcance)

        to_return = {
            'total': 0,     # number of entries in the BD, FE can use it to calculate pagination
            'list': []      # list of entries
        }

        author = request.POST.get('author', None)
        category = request.POST.get('category', None)
        # longitude = request.POST.get('longitude', 0)
        # latitude = request.POST.get('latitude', 0)
        # radius = request.POST.get('radius', 10)

        source = Alerts.objects.all()

        if author:
            source.filter(author=author)

        if category:
            source.filter(category=category)

        # if longitude and latitude and radius:
        #    source.filter(location__distance_lt=(Point(longitude, latitude), Distance(Km=radius)))

        to_return['total']= source.count()

        for a in source:
            to_return['list'].append(a.get_json())

        return Response({"message": to_return})

    elif request.method == 'POST':
        # help tip - DON'T FORGOT TO DELETE
        # Tem de permitir a adicao de ocorrencias (com a localizacao geografica, e autor associados).
        # Nota: O estado default sera sempre por validar quando estas sao criadas.
        if request.user.is_authenticated():
            # longitude = request.POST.get('longitude', 0)
            # latitude = request.POST.get('latitude', 0)

            category = int(request.POST.get('category', 0))

            try:
                a = Alerts()
                a.category = Alerts.CATEGORIES_CHOICES[category][0]
                a.description = request.POST.get('description', None)
                # a.location = Point(longitude, latitude, srid=4326)
                a.author = request.user

                a.save()
            except Exception as e:
                return Response({"message": "__exception__", "exception": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"message": "__success__"}, status=status.HTTP_201_CREATED)

        return Response({"message": "__authentication_required__"}, status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'PATCH':
        # help tip - DON'T FORGOT TO DELETE
        # Tem de permitir a actualizacao de ocorrencias (para mudar o estado das mesmas para "validadas" por
        # um administrador do sistema)

        if request.user.is_authenticated():
            if request.user.is_staff:
                post_status = int(request.POST.get('status', None))

                if post_status and alert_id:
                    try:
                        post_status = Alerts.STATUS_CHOICES[post_status][0]
                        a = Alerts.objects.get(id=alert_id)
                        a.status = post_status
                        a.save()
                    except Alerts.DoesNotExist:
                        return Response({"message": "__entry_not_found__"}, status=status.HTTP_404_NOT_FOUND)
                    except Exception as e:
                        return Response({"message": "__exception__", "exception": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        return Response({"message": "__success__"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "__fields_in_fault__"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "__permissions_in_fault__"}, status=status.HTTP_403_FORBIDDEN)

        return Response({"message": "__authentication_required__"}, status=status.HTTP_403_FORBIDDEN)
