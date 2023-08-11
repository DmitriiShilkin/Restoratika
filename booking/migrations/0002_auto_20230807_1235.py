from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
                INSERT INTO booking_hall (name, description) VALUES ('Главный', '');
                INSERT INTO booking_table (number, description, hall_id, occupied) VALUES ('Не выбран', '', 1, '[]');
                INSERT INTO booking_table (number, description, hall_id, occupied) VALUES ('1 стол', '', 1, '[]');
                INSERT INTO booking_table (number, description, hall_id, occupied) VALUES ('2 стол', '', 1, '[]');
                INSERT INTO booking_table (number, description, hall_id, occupied) VALUES ('3 стол', '', 1, '[]');
                INSERT INTO booking_table (number, description, hall_id, occupied) VALUES ('4 стол', '', 1, '[]');
                INSERT INTO booking_table (number, description, hall_id, occupied) VALUES ('5 стол', '', 1, '[]');
                INSERT INTO booking_table (number, description, hall_id, occupied) VALUES ('6 стол', '', 1, '[]');
                INSERT INTO booking_table (number, description, hall_id, occupied) VALUES ('7 стол', '', 1, '[]');
                INSERT INTO booking_table (number, description, hall_id, occupied) VALUES ('8 стол', '', 1, '[]');
                INSERT INTO booking_table (number, description, hall_id, occupied) VALUES ('9 стол', '', 1, '[]');
                INSERT INTO booking_table (number, description, hall_id, occupied) VALUES ('10 стол', '', 1, '[]');
                INSERT INTO booking_table (number, description, hall_id, occupied) VALUES ('11 стол', '', 1, '[]');
                INSERT INTO booking_table (number, description, hall_id, occupied) VALUES ('12 стол', '', 1, '[]');
            """
        ),
    ]
