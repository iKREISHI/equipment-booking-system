EQUIPMENT_RIGHTS = [
    "add_inventoryequipment", "change_inventoryequipment",
    "delete_inventoryequipment", "view_inventoryequipment",
    "add_inventoryequipmentstatus", "change_inventoryequipmentstatus",
    "delete_inventoryequipmentstatus", "view_inventoryequipmentstatus",
]

LOCATION_RIGHTS = [
    "add_location", "change_location", "delete_location", "view_location",
]

MAINTENANCE_RIGHTS = [
    "add_maintenance", "change_maintenance", "delete_maintenance", "view_maintenance",
    "add_maintenancestatus", "change_maintenancestatus",
    "delete_maintenancestatus", "view_maintenancestatus",
]

RESERVATION_RIGHTS = [
    # Если модели Reservation ещё нет, строки ниже просто пропустятся
    "add_reservation", "change_reservation",
    "delete_reservation", "view_reservation",
]

USER_RIGHTS = [
    "add_user", "change_user", "delete_user", "view_user",
]

# ------------------------------
# Определение групп и их прав
# ------------------------------
GROUP_DEFINITIONS = {
    # 1) Администратор системы — все права
    "Администратор системы": "ALL",

    # 2) Материально ответственное лицо — всё на оборудование/локации/обслуживание/бронирование
    "Материально ответственное лицо": (
        EQUIPMENT_RIGHTS + LOCATION_RIGHTS + MAINTENANCE_RIGHTS + RESERVATION_RIGHTS
    ),

    # 3) Модератор — всё на пользователей, оборудование, локации, обслуживание
    "Модератор": (
        USER_RIGHTS + EQUIPMENT_RIGHTS + LOCATION_RIGHTS + MAINTENANCE_RIGHTS
    ),

    # 4) Обслуживающий персонал — всё на обслуживание, чтение остального
    "Обслуживающий персонал": (
        MAINTENANCE_RIGHTS  # полный доступ
        # «view_*» на всё, кроме обслуживания, мы добавим динамически ниже
    ),

    # 5) Арендатор — чтение оборудования/локаций, полные права на бронирования
    "Арендатор": (
        ["view_inventoryequipment", "view_inventoryequipmentstatus"] +
        ["view_location"] +
        RESERVATION_RIGHTS
    ),
}