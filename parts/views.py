import re
from collections import Counter

from django.db import DatabaseError
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Part
from .serializers import PartSerializer


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer


@api_view(["GET"])
def most_common_words():
    """
    Return the five most common words in part descriptions
    """
    try:
        descriptions = Part.objects.values_list("description", flat=True)

        if not descriptions.exists():
            return Response(
                {"message": "No descriptions found"},
                status=status.HTTP_204_NO_CONTENT
            )

        all_words = " ".join(descriptions).lower()
        words = re.findall(r"\b\w+\b", all_words)

        if not words:
            return Response(
                {"message": "No words found in descriptions"},
                status=status.HTTP_204_NO_CONTENT
            )

        most_common_words = Counter(words).most_common(5)

        response_data = {
            "most_common_words": dict(most_common_words)
        }

        return Response(
            response_data,
            status=status.HTTP_200_OK
        )

    except DatabaseError:
        return Response(
            {"error": "Database error occurred"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
