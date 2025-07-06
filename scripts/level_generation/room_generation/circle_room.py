from scripts.level_generation.dungeon_enum_keys import *
from scripts.engine.keys.keys import keys


class Circle_Room():

    @staticmethod
    def Room_Structure_Circle(map, center_x, center_y, radius):
        for y in range(center_y - radius, center_y + radius + 1):
            for x in range(center_x - radius, center_x + radius + 1):
                # Calculate the distance from the center
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                if distance == radius:
                    Circle_Room.Spawn_Door_Circle_Room(map, center_x, x, center_y, y)
                        

                elif distance <= radius:
                    # Floor inside the circle
                    map[x][y] = FLOOR
                elif distance <= radius + 1:
                    # Walls around the circular floor
                    map[x][y] = WALL

    @staticmethod
    def Spawn_Door_Circle_Room(map, center_x, x, center_y, y):
        # Check if door is being spawned on x or y axis
        
        if y == center_y: # x axis
            map[x][y] = DOOR
            
        elif x == center_x: # y axis
            map[x][y] = WALL

        return

