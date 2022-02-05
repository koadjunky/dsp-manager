from pydantic import BaseModel, validator

from dsp_be.logic.machine import machines
from dsp_be.logic.recipe import recipes


class FactoryCreateDto(BaseModel):
    star_name: str
    planet_name: str
    name: str
    machine: str
    recipe: str
    count: int

    @validator("recipe")
    def recipe_must_be_known_and_matching_machine(cls, recipe_name, values):
        machine_name = values["machine"]
        if not recipes.has(recipe_name):
            raise ValueError(f"Recipe {recipe_name} is invalid")
        recipe = recipes.get(recipe_name)
        if machine_name not in machines:
            raise ValueError(f"Machine {machine_name} is invalid")
        machine = machines[machine_name]
        if recipe.machine != machine.type:
            raise ValueError(
                f"Recipe {recipe_name} does not match machine {machine_name}"
            )
        return recipe_name


class FactoryUpdateDto(FactoryCreateDto):
    id: str


class FactoryDeleteDto(BaseModel):
    id: str