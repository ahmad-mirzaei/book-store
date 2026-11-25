
import secrets
import string
import orders.models
from django.db import migrations, models


def populate_short_codes(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    characters = string.ascii_uppercase + string.digits

    for order in Order.objects.all().iterator():
        while True:
            code = ''.join(
                secrets.choice(characters)
                for _ in range(12)
            )

            if not Order.objects.filter(
                tracking_code_short=code
            ).exists():
                break

        order.tracking_code_short = code
        order.save(update_fields=["tracking_code_short"])


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_tracking_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='tracking_code_short',
            field=models.CharField(
                max_length=12,
                null=True,
                editable=False,
            ),
        ),
        migrations.RunPython(
            populate_short_codes,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name='order',
            name='tracking_code_short',
            field=models.CharField(
                max_length=12,
                unique=True,
                editable=False,
            ),
        ),
        migrations.RemoveField(
            model_name='order',
            name='tracking_code',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='tracking_code_short',
            new_name='tracking_code',
        ),
        migrations.AlterField(
            model_name='order',
            name='tracking_code',
            field=models.CharField(
                default=orders.models.generate_tracking_code,
                max_length=12,
                unique=True,
                editable=False,
                verbose_name='کد پیگیری',
            ),
        ),
    ]
