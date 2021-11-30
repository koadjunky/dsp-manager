from dataclasses import dataclass


@dataclass
class Machine:
    name: str
    type: str
    speed: float


machines = {
    "assembler1": Machine("assembler1", "assembler", 0.75),
    "assembler2": Machine("assembler2", "assembler", 1.0),
    "assembler3": Machine("assembler3", "assembler", 1.5),
    "arc_smelter": Machine("arc_smelter", "smelter", 1.0),
    "plane_smelter": Machine("plane_smelter", "smelter", 2.0),
    "refinery": Machine("refinery", "refinery", 1.0),
    "chemical_plant": Machine("chemical_plant", "chemical_plant", 1.0),
    "fractinator": Machine("fractinator", "fractinator", 1.0),
    "particle_collider": Machine("particle_collider", "particle_collider", 1.0),
    "matrix_lab": Machine("matrix_lab", "matrix_lab", 1.0),
}
