class Pathfind_To_Player():
    def __init__(self, game):
        self.game = game


    def Check_Path_Finding_To_Player(self, check_for_path_to_player, player_pos, floor_tile):
        if not check_for_path_to_player:
            return True

        a_star = self.game.a_star
        tilemap = self.game.tilemap

        dest_x = round(player_pos[0] // tilemap.tile_size) - a_star.min_x 
        dest_y = round(player_pos[1] // tilemap.tile_size) - a_star.min_y 

        src_x = floor_tile.pos[0] - a_star.min_x 
        src_y = floor_tile.pos[1] - a_star.min_y
        
        path = a_star.a_star_search([src_x, src_y], [dest_x, dest_y])
        if not path:
            return False
        return True
        
