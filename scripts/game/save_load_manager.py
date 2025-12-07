import pickle
import os
from scripts.engine.keys.keys import keys

class Save_Load_Manager():
    def __init__(self, game, file_extension, save_folder):
        self.game = game
        self.file_extension = file_extension
        self.save_folder = save_folder
        self.data_structures = []
        self.entities_to_load = []
        self.data_structure_names = []
        self.saved_data = {}


    def Load_Game_Data(self, data):
        # Iterate over the data and assign it correctly to the appropriate entity
        for index, name in enumerate(self.entities_to_load_names):
            entity = self.entities_to_load[index]
            entity_data = data[name]
            entity.Load_Data(entity_data)


    def Clear_Data_File(self, name):
        file_name = self.save_folder+"/"+name+self.file_extension
        if not self.Check_For_File(file_name):
            print("File not found\t", file_name)
            exit(0)
        try:
            os.remove(file_name)
            print(f"File deleted: {file_name}")
        except Exception as e:
            print(f"Error deleting file: {file_name}\n{e}")
            exit(0)


    def Check_For_File(self, file_name):
        return os.path.exists(file_name)


    def Save_Game_Data(self, name):
        file_path = (self.save_folder+"/"+name+self.file_extension)
        try:
            os.remove(file_path)
        except FileNotFoundError:
            print("File not found")
        data_file = open(self.save_folder+"/"+name+self.file_extension, "wb")
        try:
            pickle.dump(self.saved_data, data_file)
        except Exception as e:
            print("Error pickling save file", e)

    # Initialise the data that needs to be saved
    def Save_Data(self):
        self.game.player.Save_Data()
        self.game.enemy_handler.Save_Enemy_Data()
        self.game.item_handler.Save_Item_Data()
        self.game.rune_handler.Save_Rune_Data()
        self.game.trap_handler.Save_Trap_Data()
        self.game.decoration_handler.Save_Decoration_Data()
        self.game.inventory.Save_Inventory_Data()
        self.game.level_loader.Save_Level_Data()
        # self.Save_Game_Data(self.saved_data['game'])
        
    # # Save game values such as depth
    # def Save_Game_Data(self, save_data):
    #     save_data['depth'] = self.game.depth

    def Save_Data_Structure(self):
        self.Save_Data()

        self.data_structures = [self.game.player.saved_data,
                                self.game.item_handler.saved_data,
                                self.game.rune_handler.saved_data,
                                self.game.enemy_handler.saved_data,
                                self.game.trap_handler.saved_data,
                                self.game.inventory.saved_data,
                                self.game.decoration_handler.saved_data,
                                self.game.level_loader.saved_data,
                                ]
        
        self.data_structure_names = ['player',
                                    'item_handler',
                                    'rune_handler',
                                    'enemy_handler',
                                    'trap_handler',
                                    'inventory',
                                    'decoration_handler',
                                    'level_loader'
                                    ]
        
        for index, name in enumerate(self.data_structure_names):
            self.saved_data[name] = self.data_structures[index]
            


        self.Save_Game_Data('save_Data')


    def Load_Data_Structure(self, data):
        self.entities_to_load = [self.game.player,
                                self.game.item_handler,
                                self.game.rune_handler,
                                self.game.enemy_handler,
                                self.game.trap_handler,
                                self.game.inventory,
                                self.game.decoration_handler,
                                ]
        
        self.entities_to_load_names = ['player',
                                    'item_handler',
                                    'rune_handler',
                                     'enemy_handler',
                                    'trap_handler',
                                     'inventory',
                                    'decoration_handler',
                                    ]
        self.Load_Game_Data(data)
        