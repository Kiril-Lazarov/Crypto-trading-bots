from test_strategy_carrusel.asset import Asset
from binance.client import Client

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)


class Methods(Asset):
    # Dictionary of exact decimal places for the specified currency pairs.
    asset_pairs_precision = {'ETHEUR': (4, 2),
                             'EURBUSD': (1, 3),
                             'ETHBUSD': (4, 2)}

    # calculates the exact amount of currency to be traded
    @classmethod
    def get_precise_qty(cls, obj_qty, precise_num):
        qty = str(obj_qty)
        qty = qty.split('.')
        right_side = qty[-1][:precise_num]
        result = qty[0] + '.' + right_side
        if precise_num == 0:
            result = qty[0]
        return float(result)

    # calculates whether current prices are suitable for trading profit
    @classmethod
    def check_for_profit(cls, asset_on_charge_qty, other_qty, price, profit_percentage, operation):
        if operation == 'multiply':
            relation = (asset_on_charge_qty * price) / other_qty
            if relation >= profit_percentage:
                return True
        else:
            relation = (asset_on_charge_qty / price) / other_qty
            if relation >= profit_percentage:
                return True
        return False

    @classmethod
    def execution(cls, obj_on_charge, other_obj, operation, objects, transactions_count):
        message= f'\n-------EXECUTION-------\nPair: active - {obj_on_charge.name}  nonactive - {other_obj.name}' \
                 f'\nOrder count: {transactions_count}'
        Methods.print_method(message)
        if operation == 'multiply':
            pair = f'{obj_on_charge.name}{other_obj.name}'
            precise_num = Methods.asset_pairs_precision[pair][0]
            trade_quantity = Methods.get_precise_qty(obj_on_charge.real_quantity, precise_num)
            curr_price = float(client.get_symbol_ticker(symbol=pair)['price'])
            other_obj.on_charge = True
            obj_on_charge.on_charge = False
            other_obj.real_quantity = trade_quantity * curr_price
            message = f'{trade_quantity} {obj_on_charge.name} on price {curr_price} -> {other_obj.real_quantity}'
            Methods.print_method(message)

        else:
            pair = f'{other_obj.name}{obj_on_charge.name}'
            precise_num = Methods.asset_pairs_precision[pair][1]
            trade_quantity = Methods.get_precise_qty(obj_on_charge.real_quantity, precise_num)
            curr_price = float(client.get_symbol_ticker(symbol=pair)['price']) * 1.0001
            trade_quantity /= curr_price
            precise_num = Methods.asset_pairs_precision[pair][0]
            trade_quantity = Methods.get_precise_qty(trade_quantity, precise_num)
            other_obj.on_charge = True
            obj_on_charge.on_charge = False
            curr_price = float(client.get_symbol_ticker(symbol=pair)['price'])
            other_obj.real_quantity = trade_quantity
            message = f'{trade_quantity * curr_price} {obj_on_charge.name} на цена {curr_price} -> {trade_quantity}'
            Methods.print_method(message)
        message = 'Active currencies:'
        Methods.print_method(message)
        for obj in objects:
            if obj.on_charge:
                message = f'{obj.name} profit {(obj.real_quantity / obj.init_qty - 1) * 100:.2f}%'
                Methods.print_method(message)

    @staticmethod
    def print_method(message):
        print(message)
