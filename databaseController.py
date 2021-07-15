class DatabaseController:
    db_typeids_PATH = "./db/typeids.csv"
    db_typeids = None
    db_typevolumes_PATH = "./db/typevolume.csv"
    db_typevolumes = None

    def __init__(self):
        if not DatabaseController.db_typeids:
            DatabaseController.db_typeids = self.generate_dict_from_csv(DatabaseController.db_typeids_PATH)
        if not DatabaseController.db_typevolumes:
            DatabaseController.db_typevolumes = self.generate_dict_from_csv(DatabaseController.db_typevolumes_PATH)

    @staticmethod
    def generate_dict_from_csv(path):
        db_file = open(DatabaseController.db_typeids_PATH, mode='r', encoding='utf-8')
        DatabaseController.db_content = db_file.read()
        db_dict = {}
        for line in DatabaseController.db_content.split('\n'):
            if len(line.split(',')) > 1:
                db_dict[line.split(',')[1]] = line.split(',')[0]
        return db_dict

    @staticmethod
    def get_item_id(item_name):
        if item_name in DatabaseController.db_typeids:
            return DatabaseController.db_typeids[item_name]
        else:
            raise ValueError("Item does not exist in database")

    @staticmethod
    def get_item_name(item_id):
        for item_name in DatabaseController.db_typeids:
            if DatabaseController.db_typeids[item_name] == item_id:
                return item_name
        raise ValueError("Item ID does not exist in database")


""""
    @staticmethod
    def get_item_volume(self, item_name):
        try:
            item_id = DatabaseController.get_item_id(item_name)
            typevolumes = DatabaseController.db_typevolumes
            if item_id in typevolumes:
                return typevolumes[item_id]
            else:
                
        except ValueError as e:
            print("Error: Attempted to get volume for item {0} which does not exist in database.".format(item_name))
            return None
"""
