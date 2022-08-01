from main import Figurine

def create(DICT_DATA):
	modes_vals = {"Easy": 635, "Medium": 750, "Hard": 810, "Impoppable": 900}
	STARTING_ROUND = DICT_DATA["STARTING_ROUND"]
	FINAL_ROUND = DICT_DATA["FINAL_ROUND"]
	STARTING_COST = modes_vals[DICT_DATA["GAME_MODE"]]
	SELLBACK_PERCENT = DICT_DATA["SELLBACK_PERCENT"]
	ROUNDING_DIGITS = DICT_DATA["ROUNDING_DIGITS"]
	fig = Figurine(
		start=STARTING_ROUND,
		sellback=SELLBACK_PERCENT,
		rounding=ROUNDING_DIGITS,
		starting_cost=STARTING_COST,
	)
	return fig.calc_profit(FINAL_ROUND)