from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    logger = logging.getLogger(__name__)

    if response is not None:
        # Log all errors except 400 (validation)
        if response.status_code >= 500 or response.status_code == 403:
            logger.error(f"{exc} | Context: {context}")
        return response
    # Handle unhandled exceptions
    logger.error(f"Unhandled exception: {exc} | Context: {context}")
    return Response({'detail': 'Internal server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 