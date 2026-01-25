# Kobold Clash

## Overview
Kobold Clash is a dungeon crawler developed in Python using the Pygame library. The project serves as a deep dive into high-performance game development, focusing on Object-Oriented Programming (OOP), design patterns, and algorithmic optimization to maintain an efficient, scalable codebase.

## Core Technical Features
* Optimized Rendering: Custom dynamic lighting engine utilizing surface blending to minimize draw calls and a memory-efficient chunk-based tile system.
* Procedural Generation: Seed-based dungeon generation with integrated "Room Type" decoration handlers and a fog-of-war minimap system.
* Advanced AI & Pathfinding: Scalable entity behaviors using A* pathfinding with Path Request Throttling to maintain performance during high-density combat.
* Logic Task Scheduling: A specialized Logic Queue system that staggers intensive event handling (e.g., Awakening Director mutations) to eliminate micro-stutter and frame-time spikes.
* State & Data Management: Centralized State Manager for scene transitions and JSON-based serialization for persistent inventory and world states.
* Performance-First Particles: A high-volume particle engine utilizing Object Pooling to eliminate the overhead of frequent memory allocation/garbage collection.
* Dynamic Pacing Director: A systemic event coordinator utilizing an internal Aggro Budget to orchestrate procedural mutations, ambushes, and environmental hazards based on real-time player events.
