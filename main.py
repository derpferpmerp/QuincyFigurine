import numpy as np

class Figurine(object):
    """docstring for Figurine"""
    def __init__(self,
        start:int=None,
        sellback:float=None,
        rounding:int=None,
        starting_cost:int=None
    ):
        if start is None: self.start = 1
        else: self.start = start
        if sellback is None:
            self.sellback = 0.95
        else: self.sellback = sellback
        if rounding is None: self.rounding = 0
        else: self.rounding = rounding
        if starting_cost is None: self.starting_cost = 750 # Medium Mode Pricing
        else: self.starting_cost = starting_cost


    def _apply_sellback(self, cost:float):
        return self.sellback * cost

        
    def _determine_quincy_cost(self, rcurr:int):
        '''
        Function: determine_quincy_cost
        Summary: Determines Figurine Cost Based on Current Round
        Examples: object.determine_quincy_cost(20)
        Attributes: 
            @param (rcurr:int): Current Round (Round to Calculate to)
        Returns: Float
        '''
        if rcurr <= 30 and rcurr > self.start:
            hyp_sell = self.starting_cost * pow(1.1, rcurr - self.start)
        elif rcurr <= 80 and rcurr > 30: 
            hyp_sell = self.starting_cost * pow(1.1, 31 - self.start) * pow(1.05, rcurr - 31)
        elif rcurr > 80:
            hyp_sell = self.starting_cost * pow(1.1, 31 - self.start) * pow(1.05, 50) * pow(1.02, rcurr - 81)

        return hyp_sell

    def _full_cost(self, rcurr:int):
        unmod_cost = self._determine_quincy_cost(rcurr)
        sell_cost = self._apply_sellback(unmod_cost)
        round_cost = round(sell_cost, self.rounding)
        return round_cost

    def _calc_cost(self, rcurr):
        if isinstance(rcurr, list):
            return np.array([self._full_cost(rnd) for rnd in rcurr], dtype=np.float64)
        else:
            return self._full_cost(rcurr)

    def _GRS(self, round_number, cost):
        # GRS = Generate Round String
        return f"  Round {str(round_number)} : ${cost}"

    def _generate_profit_string(self, profit_item, rcurr):
        lst_out = []
        conv_list = lambda alpha, beta: lst_out.append(self._GRS(alpha, beta))
        if not isinstance(profit_item, float):
            for i, profit in enumerate(profit_item):
                conv_list(rcurr[i], profit)
        else:
            conv_list(rcurr, profit_item)
        return "\n".join(lst_out)

    def _display_profit(self, profit_string):
        print(*[
            "\n -- Quincy Action Figurine Calculator -- ",
            "",
            " - Setup Info - ",
            f"  Starting Round : {self.start}",
            f"  Sellback Value: {int(self.sellback * 100)}%",
            "",
            " - Total Profit - ",
            f"{profit_string}\n"
        ], sep="\n")

    def calc_profit(self, rcurr):
        original_cost = float(self.starting_cost)
        sellback_value = self._calc_cost(rcurr)
        total_profit = sellback_value - original_cost
        profit_string = self._generate_profit_string(total_profit, rcurr)
        self._display_profit(profit_string)
        return total_profit

if __name__ == "__main__":
    quincy = Figurine()
    lst = quincy.calc_profit([21,51,81,100])
    print(lst)
