# Kobold Clash

## Overview
Kobold Clash is a dungeon crawler developed in Python using the Pygame library. The project serves as a deep dive into high-performance game development, focusing on Object-Oriented Programming (OOP), design patterns, and algorithmic optimization to maintain an efficient, scalable codebase.

## Core Technical Features
* Optimized Rendering: A custom dynamic lighting engine designed to minimize draw calls and a memory-efficient tile system that manages collisions, entities, and light data.
* Procedural Generation: Dynamic dungeon generation that ensures a unique layout every session, integrated with a Minimap system to track player exploration.
* Advanced AI & Pathfinding: Scalable enemy AI that increases in complexity based on player proximity, utilizing robust pathfinding for both navigation and strategic item spawning.
* State & Data Management: A centralized State Manager for seamless scene transitions and a JSON-based Save/Load system to persist game states.
* Scalable Architecture: A central dictionary for string-key consistency across modules and an automated asset management system for handling texture atlases and audio files.
* Interactive Systems: A comprehensive inventory system with hybrid mouse/keyboard support and an environment that reacts dynamically to player behavior.
* Performance-First Particles: A dynamic particle system utilizing Object Pooling for efficient spawning and high-volume visual effects.
