from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .importer import RegaliaImporter
from .generator import RegaliaGenerator


@csrf_exempt
@permission_classes([AllowAny, ])
@api_view(['POST'])
def genreg(request):
    if not request.FILES:
        ins = request.data
        importer = RegaliaImporter(ins)
        ins = importer.import_one_object()
        generator = RegaliaGenerator()
        generator.generate_one(ins=ins)
        archname = generator.save_to_archive()
        url = generator.get_url_to_archive(archname)
        return Response({"url": url})

    else:
        importer = RegaliaImporter(file=request.FILES['file'])
        qs = importer.import_from_excel()
        generator = RegaliaGenerator(qs=qs)
        generator.generate_all()
        archname = generator.save_to_archive()
        url = generator.get_url_to_archive(archname)
        return Response({"url": url})

