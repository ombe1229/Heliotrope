from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

from heliotrope.database.query import get_galleryinfo
from heliotrope.utils.hitomi.models import HitomiGalleryInfoModel
from heliotrope.utils.response import not_found
from heliotrope.utils.typed import HeliotropeRequest

hitomi_galleyinfo = Blueprint("hitomi_galleyinfo", url_prefix="/galleryinfo")


class HitomiGalleryInfoView(HTTPMethodView):
    async def get(self, request: HeliotropeRequest, index: int):
        if galleryinfo := await get_galleryinfo(index):
            if request.headers.get("raw") in ["True", "true"]:
                return json({"status": 200, **galleryinfo})

            parsed_galleryinfo_model = HitomiGalleryInfoModel.parse_galleryinfo(
                galleryinfo, True
            )
            return json(
                {
                    "status": 200,
                    "language_localname": parsed_galleryinfo_model.language_localname,
                    "language": parsed_galleryinfo_model.language,
                    "date": parsed_galleryinfo_model.date,
                    "files": parsed_galleryinfo_model.files,
                    "tags": list(parsed_galleryinfo_model.tags),
                    "japanese_title": parsed_galleryinfo_model.japanese_title,
                    "title": parsed_galleryinfo_model.title,
                    "id": parsed_galleryinfo_model.galleryid,
                    "type": parsed_galleryinfo_model.hitomi_type,
                }
            )

        return not_found


hitomi_galleyinfo.add_route(HitomiGalleryInfoView.as_view(), "/<index:int>")