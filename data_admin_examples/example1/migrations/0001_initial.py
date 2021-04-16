from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "lft",
                    models.PositiveIntegerField(
                        blank=True, db_index=True, editable=False, null=True
                    ),
                ),
                (
                    "rght",
                    models.PositiveIntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "lvl",
                    models.PositiveIntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Unique identifier",
                        max_length=300,
                        primary_key=True,
                        serialize=False,
                        verbose_name="name",
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=300,
                        null=True,
                        verbose_name="source",
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="last modified",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="description",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=300,
                        null=True,
                        verbose_name="category",
                    ),
                ),
                (
                    "subcategory",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=300,
                        null=True,
                        verbose_name="subcategory",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        help_text="Hierarchical parent",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="xchildren",
                        to="example1.Customer",
                        verbose_name="owner",
                    ),
                ),
            ],
            options={
                "verbose_name": "customer",
                "verbose_name_plural": "customers",
                "db_table": "customer",
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "lft",
                    models.PositiveIntegerField(
                        blank=True, db_index=True, editable=False, null=True
                    ),
                ),
                (
                    "rght",
                    models.PositiveIntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "lvl",
                    models.PositiveIntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Unique identifier",
                        max_length=300,
                        primary_key=True,
                        serialize=False,
                        verbose_name="name",
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=300,
                        null=True,
                        verbose_name="source",
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="last modified",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="description",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=300,
                        null=True,
                        verbose_name="category",
                    ),
                ),
                (
                    "subcategory",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=300,
                        null=True,
                        verbose_name="subcategory",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        help_text="Hierarchical parent",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="xchildren",
                        to="example1.Location",
                        verbose_name="owner",
                    ),
                ),
            ],
            options={
                "verbose_name": "location",
                "verbose_name_plural": "locations",
                "db_table": "location",
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "lft",
                    models.PositiveIntegerField(
                        blank=True, db_index=True, editable=False, null=True
                    ),
                ),
                (
                    "rght",
                    models.PositiveIntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "lvl",
                    models.PositiveIntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Unique identifier",
                        max_length=300,
                        primary_key=True,
                        serialize=False,
                        verbose_name="name",
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=300,
                        null=True,
                        verbose_name="source",
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="last modified",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="description",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=300,
                        null=True,
                        verbose_name="category",
                    ),
                ),
                (
                    "subcategory",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=300,
                        null=True,
                        verbose_name="subcategory",
                    ),
                ),
                (
                    "cost",
                    models.DecimalField(
                        blank=True,
                        decimal_places=8,
                        help_text="Cost of the item",
                        max_digits=20,
                        null=True,
                        verbose_name="cost",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("make to stock", "make to stock"),
                            ("make to order", "make to order"),
                        ],
                        max_length=20,
                        null=True,
                        verbose_name="type",
                    ),
                ),
                (
                    "weight",
                    models.DecimalField(
                        blank=True,
                        decimal_places=8,
                        help_text="Weight of the item",
                        max_digits=20,
                        null=True,
                        verbose_name="weight",
                    ),
                ),
                (
                    "volume",
                    models.DecimalField(
                        blank=True,
                        decimal_places=8,
                        help_text="Volume of the item",
                        max_digits=20,
                        null=True,
                        verbose_name="volume",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        help_text="Hierarchical parent",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="xchildren",
                        to="example1.Item",
                        verbose_name="owner",
                    ),
                ),
            ],
            options={
                "verbose_name": "item",
                "verbose_name_plural": "items",
                "db_table": "item",
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Demand",
            fields=[
                (
                    "lft",
                    models.PositiveIntegerField(
                        blank=True, db_index=True, editable=False, null=True
                    ),
                ),
                (
                    "rght",
                    models.PositiveIntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "lvl",
                    models.PositiveIntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Unique identifier",
                        max_length=300,
                        primary_key=True,
                        serialize=False,
                        verbose_name="name",
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=300,
                        null=True,
                        verbose_name="source",
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="last modified",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="description",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=300,
                        null=True,
                        verbose_name="category",
                    ),
                ),
                (
                    "subcategory",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=300,
                        null=True,
                        verbose_name="subcategory",
                    ),
                ),
                (
                    "due",
                    models.DateTimeField(
                        db_index=True,
                        help_text="Due date of the sales order",
                        verbose_name="due",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("inquiry", "inquiry"),
                            ("quote", "quote"),
                            ("open", "open"),
                            ("closed", "closed"),
                            ("canceled", "canceled"),
                        ],
                        default="open",
                        help_text='Status of the demand. Only "open" demands are planned',
                        max_length=10,
                        null=True,
                        verbose_name="status",
                    ),
                ),
                (
                    "quantity",
                    models.DecimalField(
                        decimal_places=8,
                        default=1,
                        max_digits=20,
                        verbose_name="quantity",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="example1.Customer",
                        verbose_name="customer",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="example1.Item",
                        verbose_name="item",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="example1.Location",
                        verbose_name="location",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        help_text="Hierarchical parent",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="xchildren",
                        to="example1.Demand",
                        verbose_name="owner",
                    ),
                ),
            ],
            options={
                "verbose_name": "sales order",
                "verbose_name_plural": "sales orders",
                "db_table": "demand",
                "ordering": ["name"],
                "abstract": False,
            },
        ),
    ]
