class MenuRouter:
    """
    A router to control all database operations on models in the
    menu application.
    """
    route_app_labels = {
        'menu',
    }

    def db_for_read(self, model, **hints):
        """
        Attempts to read menu models go to menu_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'menu_db'

        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write menu models go to menu_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'menu_db'

        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the menu or ... apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the menu and ... apps only appear in the
        'menu_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'menu_db'
        return None
