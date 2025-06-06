# Generated by Django 5.2 on 2025-06-04 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0005_record_picture2_record_picture3_record_picture4_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='monument_type',
            field=models.CharField(choices=[('banjo_enclosure', 'Banjo enclosure'), ('curvilinear_enclosure', 'Curvilinear enclosure'), ('defended_enclosure', 'Defended enclosure'), ('causewayed_enclosure', 'Causewayed enclosure'), ('rectilinear_enclosure', 'Rectilinear enclosure'), ('hillfort', 'Hillfort'), ('promontory_fort', 'Promontory fort'), ('round_barrow', 'Round barrow'), ('cairn', 'Cairn'), ('platform_mound', 'Platform mound'), ('burial_mound', 'Burial mound'), ('field_system', 'Field system'), ('ridge_and_furrow', 'Ridge and furrow'), ('lynchet', 'Lynchet'), ('strip_field_system', 'Strip field system'), ('roman_villa', 'Roman villa'), ('farmstead', 'Farmstead'), ('hamlet', 'Hamlet'), ('deserted_medieval_village', 'Deserted medieval village'), ('hollow_way', 'Hollow way'), ('trackway', 'Trackway'), ('causeway', 'Causeway'), ('tramway', 'Tramway'), ('quarry', 'Quarry'), ('mine_shaft', 'Mine shaft'), ('leat', 'Leat'), ('mill', 'Mill'), ('quarry_pit', 'Quarry pit'), ('extraction_pit', 'Extraction pit'), ('boundary_bank', 'Boundary bank'), ('defensive_bank', 'Defensive bank'), ('field_boundary', 'Field boundary'), ('defensive_ditch', 'Defensive ditch'), ('drainage_ditch', 'Drainage ditch'), ('boundary_ditch', 'Boundary ditch'), ('earthwork', 'Earthwork'), ('cropmark', 'Cropmark'), ('structure', 'Structure (undefined)'), ('other', 'Other'), ('unknown', 'Unknown')], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='record',
            name='site_type',
            field=models.CharField(choices=[('bank', 'Bank'), ('ditch', 'Ditch'), ('enclosure', 'Enclosure'), ('field_system', 'Field System'), ('industrial', 'Industrial'), ('mound', 'Mound'), ('pit', 'Pit'), ('settlement', 'Settlement'), ('trackway', 'Trackway'), ('other', 'Other'), ('unknown', 'Unknown')], max_length=100),
        ),
    ]
