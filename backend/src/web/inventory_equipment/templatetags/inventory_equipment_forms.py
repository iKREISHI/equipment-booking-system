from django import template
from web.inventory_equipment.forms.inventory_equipment import InventoryEquipmentForm

register = template.Library()

@register.simple_tag
def inventory_equipment_form(equipment=None):
    if equipment:
        return InventoryEquipmentForm(instance=equipment)
    return InventoryEquipmentForm()
