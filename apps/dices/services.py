import math
import random


class RollService:
    @classmethod
    def roll_dice(cls, sides, number, modifier, modifier_value, result_operation):
        modifier = None if modifier == "none" else modifier
        modifier_value = None if modifier_value == "" else int(modifier_value)
        modifiers = {
            "+": RollService.add,
            "-": RollService.subtract,
            "*": RollService.multiply,
            "/": RollService.split,
        }
        symbol_modifier = {
            "+": "✛",
            "-": "-",
            "*": "*",
            "/": "/",
        }
        result = f"Lanzar {number} dados de {sides} caras"

        dices = []

        for dice in range(0, number):
            dices.append(random.randint(1, sides))

        result_dices = dices.copy()

        if modifier and modifier_value:
            modifier_function = modifiers.get(modifier)
            emoji = symbol_modifier.get(modifier)
            modifier_dices = [
                f"({dice}{emoji}{modifier_value}={modifier_function(dice, modifier_value)})"  # noqa E501
                for dice in dices
            ]
            result_dices = [
                modifier_function(dice, modifier_value) for dice in dices
            ]  # noqa E501
            result += f" con un modificador de {emoji}{modifier_value}"
        else:
            modifier_dices = [str(dice) for dice in dices]

        if result_operation:
            inst_result = sum(result_dices)
            result += " sumando los resultados: <br /><br />"
            result += (
                f"{symbol_modifier.get('+')}".join(modifier_dices)
                + "="
                + str(inst_result)
            )
        else:
            result += " con resultados individuales: <br /><br />"
            join_results = (
                "<br />".join(modifier_dices).replace("(", "").replace(")", "")
            )
            result += join_results

        return result

    @classmethod
    def add(cls, first_number, second_number):
        return int(first_number + second_number)

    @classmethod
    def subtract(cls, first_number, second_number):
        return int(first_number - second_number)

    @classmethod
    def multiply(cls, first_number, second_number):
        return int(first_number * second_number)

    @classmethod
    def split(cls, first_number, second_number):
        return int(math.ceil(first_number / second_number))
