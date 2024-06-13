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
    STOP_WORDS = set([
        "a", "an", "the", "and", "but", "its", "or", "for", "nor", "so", "yet",
        "at", "by", "in", "of", "on", "to", "with", "be", "have", "are", "do",
        "that", "this", "which", "were", "what", "all", "any", "as", "both",
        "down", "in", "he", "has", "from", "few", "for", "from", "into", "is",
        "it", "more", "most", "no", "not", "only", "out", "over", "up", "very",
        "will", "was"
    ])

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

        filtered_words = [word for word in words if word not in STOP_WORDS]

        most_common_words = Counter(filtered_words).most_common(5)

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
