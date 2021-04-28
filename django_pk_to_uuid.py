# Please go through the attached README. I have defined all the steps in it.

from django.db import migrations, models
import uuid


def office_uuid_forward(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Office = apps.get_model('app', 'Office')
    for office in Office.objects.using(db_alias).all():
        office.office_uuid = uuid.uuid4()
        office.save()


def employee_office_uuid_forward(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Office = apps.get_model('app', 'Office')
    Employee = apps.get_model('app', 'Employee')
    for employee in Employee.objects.using(db_alias).all():
        employee.office_uuid = Office.objects.get(office_id=employee.office_id).office_uuid
        employee.save()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='office_uuid',
            field=models.UUIDField(null=True),
        ),
        migrations.RunPython(office_uuid_forward),
        migrations.AlterField(
            model_name='office',
            name='office_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, serialize=False),
        ),
        
        migrations.AddField(
            model_name='employee',
            name='office_uuid',
            field=models.UUIDField(null=True),
        ),
        migrations.RunPython(employee_office_uuid_forward),
        migrations.RemoveField(
            model_name='employee',
            name='office',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='office_uuid',
            new_name='office',
        ),

        migrations.RemoveField(
            model_name='office',
            name='office_id',
        ),
        migrations.RenameField(
            model_name='office',
            old_name='office_uuid',
            new_name='office_id',
        ),
        migrations.AlterField(
            model_name='office',
            name='office_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),

        migrations.AlterField(
            model_name='employee',
            name='office',
            field=models.ForeignKey(on_delete=models.CASCADE, to='app.office')
        ),
    ]
