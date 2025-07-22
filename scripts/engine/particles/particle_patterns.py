import random
import math
import numpy as np

class Particle_Patterns():

    @staticmethod
    def Dash_Particle():
        angle = random.random() * math.pi * 2
        speed = random.random() * 40
        velocity = [
                    math.cos(angle) * speed,
                    math.sin(angle) * speed
                    ]
        
        return velocity
    
    @staticmethod
    # Constrain most of the motion to upward directions with slight spread
    def Fire_Particle():
        base_angle = math.pi/2  # Straight up (90 degrees)
        angle_variation = math.pi/8  # 22.5 degrees spread in each direction
        angle = base_angle + random.uniform(-angle_variation, angle_variation)
        
        # Fire tends to have faster initial speeds that taper off
        speed = - (random.random() * 30)
        velocity = [
            math.cos(angle) * speed,  
            math.sin(angle) * speed   
        ]
        return velocity
    

    # Shoot the particles out straight
    @staticmethod
    def Spark_Particle():
        velocity = np.array([random.uniform(-10, 10), random.uniform(-10, 10)])
        velocity *= 10
        norm = np.linalg.norm(velocity)
        if norm == 0:  # Avoid division by zero
            return (0,0)
        
        return (velocity / norm).tolist()  # Normalize and convert to a list
    
    @staticmethod
    def Soul_Particle():
        velocity = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
        norm = np.linalg.norm(velocity)
        if norm == 0:  # Avoid division by zero
            return (0,0)
        
        return ((velocity / norm) * 15).tolist()  # Normalize and convert to a list half speed of normal sparks

    @staticmethod
    def Vampire_Particle():
        # Constrain most of the motion to upward directions with slight spread
        base_angle = math.pi  # Straight up (180 degrees)
        angle_variation = math.pi/4  # 45 degrees spread in each direction
        angle = base_angle + random.uniform(-angle_variation, angle_variation)
        
        # Fire tends to have faster initial speeds that taper off
        speed = - (random.random() * 30)
        velocity = [
            math.cos(angle) * speed,
            math.sin(angle) * speed  
        ]
        return velocity
    
    @staticmethod
    def Player_Particle():
        # Constrain most of the motion to upward directions with slight spread
        base_angle = math.pi/2  # Straight up (90 degrees)
        angle_variation = math.pi/4  # 45 degrees spread in each direction
        angle = base_angle + random.uniform(-angle_variation, angle_variation)
        
        # Fire tends to have faster initial speeds that taper off
        speed = - (random.random() * 30)
        velocity = [
            math.cos(angle) * speed,  
            math.sin(angle) * speed   
        ]
        return velocity