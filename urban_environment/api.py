import json

# from django.contrib.gis.geos import Point
# from django.contrib.gis.measure import Distance
from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

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

        author = request.GET.get('author', None)
        category = request.GET.get('category', None)
        latitude = request.GET.get('latitude', None)
        longitude = request.GET.get('longitude', None)
        radius = request.GET.get('radius', None)
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 20))

        f = Q()

        if author:
            f = Q(f, Q(author=author))

        if category:
            f = Q(f, Q(category=category))

        if latitude and longitude and radius:
            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(radius)

            f = Q(
                f,
                Q(latitude__gte=(latitude - radius)),
                Q(latitude__lte=(latitude + radius)),
                Q(longitude__gte=(longitude - radius)),
                Q(longitude__lte=(longitude + radius))
            )

        source = Alerts.objects.filter(f)

        to_return['total'] = source.count()

        for a in source[offset:offset+limit]:
            to_return['list'].append(a.get_json())

        return Response({"message": to_return})

    elif request.method == 'POST':
        # help tip - DON'T FORGOT TO DELETE
        # Tem de permitir a adicao de ocorrencias (com a localizacao geografica, e autor associados).
        # Nota: O estado default sera sempre por validar quando estas sao criadas.
        if request.user.is_authenticated():
            longitude = request.POST.get('latitude', None)
            latitude = request.POST.get('longitude', None)
            description = request.POST.get('description', None)
            category = request.POST.get('category', None)

            if latitude and longitude and description and category:
                try:
                    a = Alerts()
                    a.category = Alerts.CATEGORIES_CHOICES[int(category)][0]
                    a.description = description
                    a.latitude = float(latitude)
                    a.longitude = float(longitude)
                    # a.location = Point(longitude, latitude, srid=4326)
                    a.author = request.user

                    a.save()
                except Exception as e:
                    return Response({"message": "__exception__", "exception": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"message": "__success__"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "__fields_in_fault__"}, status=status.HTTP_400_BAD_REQUEST)

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
