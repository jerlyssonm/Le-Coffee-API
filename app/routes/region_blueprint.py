from flask import Blueprint

from app.controllers import region_controller


bp_region = Blueprint("regions", __name__, url_prefix = "/regions")

bp_region.get("")(region_controller.get_regions)
bp_region.post("")(region_controller.create_region)
bp_region.delete("<region_id>")(region_controller.delete_region)
bp_region.patch("<region_id>")(region_controller.update_region)