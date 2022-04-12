# ZombieHunter
Zombie Hunter is a tile-based 2D shooter game with a top-down view developed with the purpose to learn Pygame and game dev related concepts.

# Demo
[<p align="center"><img alt="alt_text" width="800px" height="500px" src="assets/Demo.gif" /></p>](https://www.youtube.com/watch?v=zhnfb5-xbZY)

# Setup
In order to run the project you need to have already installed a Python interpreter (>= 3.7), the Python Package Installer (Pip) and git on your machine.

To clone the git project and configure its dependencies you have to run these commands:
```sh
git clone https://github.com/WarriorsSami/ZombieHunter.git
cd ZombieHunter
pip install -r requirements.txt
python main.py
```

# Commands and HUDs
Head-Up Display Components:
- player health bar
- mobs counter
- player score (related to rotations, collision with mobs, items and shots)
- player hit flags for collisions with walls, health packs and mobs

Command List:
- ```W/Arrow Up``` to move forward
- ```S/Arrow Down``` to move backward
- ```A/Arrow Left``` to rotate to the left
- ```D/Arrow Right``` to rotate to the right
- ```Space``` to shoot
- ```Q``` to switch between weapons
- ```P``` to pause the game
- ```N``` to switch between day and night mode
- ```Esc``` to quit the game
- ```F1``` to see colliders

# Todo List
- [x] add Camera
- [x] add Tiled Map
- [x] add Night Mode
- [x] add Items to pick-up
- [ ] add Grenade Launcher
- [ ] add Explosion Animation
- [ ] add multiple levels and maps
- [ ] add civilians to be rescued
- [ ] add multiple sorts of mobs
- [ ] add guns to mobs
- [ ] add obstacles that can be manipulated

## References and Sources:
- framework docs: [Pygame Docs](https://www.pygame.org/docs/)
- base project: [KidsCanCode Tile-based game Tutorial](https://www.youtube.com/playlist?list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i)
- visual and audio assets: [Kenney top-down shooter Pack](https://www.kenney.nl/assets/topdown-shooter) and [Kenney Particle Pack](https://www.kenney.nl/assets/particle-pack)
