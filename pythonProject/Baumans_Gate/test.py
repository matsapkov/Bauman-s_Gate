from Baumans_Gate.Town.GenericBuilding import GenericBuilding
from Baumans_Gate.Town.Arsenal import Arsenal
from Baumans_Gate.Town.Forge import Forge

forge1 = Forge()
forge2 = Forge()

print(isinstance(forge1, forge2.__class__))


