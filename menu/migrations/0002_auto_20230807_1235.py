from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
                INSERT INTO menu_store (name, description) VALUES ('Ресторан', '');
                INSERT INTO menu_store (name, description) VALUES ('Лавка', '');
                INSERT INTO menu_store (name, description) VALUES ('Пекарня', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Салаты', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Супы', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Горячие закуски', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Мясо', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Рыба и морские гады', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Варенье и десерты', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Холодные закуски', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Паста', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Сладости', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Молочная продукция', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Сыры', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Консервированные продукты', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Выпечка', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Масло, соусы', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Кофе, напитки и специи', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Мыло', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Хлеб', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Десерты', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Печенье', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Торты', '');
                INSERT INTO menu_menusection (name, description) VALUES ('Паста (лавка)', '');
            """
        ),
    ]
