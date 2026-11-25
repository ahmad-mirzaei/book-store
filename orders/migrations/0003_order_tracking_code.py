
import uuid
from django.db import migrations, models


def generate_tracking_codes(apps, schema_editor):
    Order = apps.get_model("orders", "Order")

    for order in Order.objects.filter(
        tracking_code__isnull=True
    ).iterator():
        order.tracking_code = uuid.uuid4()
        order.save(update_fields=["tracking_code"])


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_order_address_order_full_name_order_phone_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="tracking_code",
            field=models.UUIDField(
                null=True,
                editable=False,
                verbose_name="کد پیگیری",
            ),
        ),

        migrations.RunPython(
            generate_tracking_codes,
            migrations.RunPython.noop,
        ),

        migrations.AlterField(
            model_name="order",
            name="tracking_code",
            field=models.UUIDField(
                default=uuid.uuid4,
                unique=True,
                editable=False,
                verbose_name="کد پیگیری",
            ),
        ),
    ]
