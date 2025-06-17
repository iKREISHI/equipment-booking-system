import pandas as pd
from datetime import datetime
from django.db import transaction

from apps.equipments.models import (
    InventoryEquipment,
    InventoryEquipmentStatus,
    InventoryImport,
)
from apps.locations.models import Location


def run_inventory_import(imp: InventoryImport) -> None:
    imp.status = "IN_PROGRESS"
    imp.save(update_fields=["status"])

    try:
        # 🔻 главное изменение — open() вместо .path
        with imp.file.open("rb") as uploaded:
            df = pd.read_excel(uploaded)

        # дальше код не менялся ↓↓↓
        mapping = {
            "Основное средство": "name",
            "Инвентарный номер": "inventory_number",
            "Дата принятия к учету": "registration_date",
            "Количество": "count",
        }
        for col in mapping:
            if col not in df.columns:
                raise ValueError(f"Нет столбца «{col}».")

        location, _ = Location.objects.get_or_create(name="Технопарк УПК")
        status, _ = InventoryEquipmentStatus.objects.get_or_create(name="Доступно")

        objs, duplicated, skipped = [], 0, 0
        for _, row in df.iterrows():
            raw_num = row["Инвентарный номер"]
            if pd.isna(raw_num):
                skipped += 1
                continue
            inv_number = f"{int(raw_num):d}" if isinstance(raw_num, float) else str(raw_num).strip()
            if InventoryEquipment.objects.filter(inventory_number=inv_number).exists():
                duplicated += 1
                continue

            try:
                reg_date = datetime.strptime(str(row["Дата принятия к учету"]).strip(), "%d.%m.%Y").date()
            except ValueError:
                reg_date = datetime.today().date()

            qty = int(row.get("Количество", 1) or 1)

            objs.append(
                InventoryEquipment(
                    owner=imp.created_by,
                    name=str(row["Основное средство"]).strip(),
                    inventory_number=inv_number,
                    registration_date=reg_date,
                    status=status,
                    location=location,
                    count=qty,
                )
            )

        with transaction.atomic():
            InventoryEquipment.objects.bulk_create(objs, batch_size=500)

        imp.status = "SUCCESS"
        imp.rows_created = len(objs)
        imp.rows_duplicated = duplicated
        imp.rows_skipped = skipped
        imp.save(update_fields=["status", "rows_created", "rows_duplicated", "rows_skipped"])

    except Exception as exc:
        imp.status = "FAILED"
        imp.error = str(exc)
        imp.save(update_fields=["status", "error"])
