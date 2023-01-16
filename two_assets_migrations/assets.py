from binance.client import Client

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)


class Assets:
    asset_pairs_precision = {'ETHEUR': (4, 2), 'BTCEUR': (5, 2),
                             'EURBUSD': (1, 3),'ETHBTC': (4, 6),
                             'ETHBUSD': (4, 2), 'BTCBUSD': (5, 2)}

    def __init__(self, name, init_quantity):
        self.init_quantity = init_quantity
        self.name = name
        self.quantity = self.init_quantity
        self.assets = {'ETH': 0, 'BTC': 0, 'EUR': 0, 'BUSD': 0}

    @staticmethod
    def get_accuracy_num(asset_pair):
        return Assets.asset_pairs_precision[asset_pair]

    @staticmethod
    def get_precise_qty(obj_qty, precise_num):
        obj_qty = str(obj_qty)
        obj_qty = obj_qty.split('.')
        right_side = obj_qty[-1][:precise_num]
        result = obj_qty[0] + '.' + right_side
        if precise_num == 0:
            result = obj_qty[0]
        return float(result)

    def take_new_quantities(self, active_asset_name, price_dict):
        for asset, value in self.assets.items():
            if asset == active_asset_name:
                self.assets[asset] = self.quantity

            else:
                for asset_pair, price in price_dict.items():
                    if asset in asset_pair and active_asset_name in asset_pair:
                        if f'{asset}/{active_asset_name}' == asset_pair:
                            self.assets[asset] = self.quantity / price

                            break
                        else:
                            self.assets[asset] = self.quantity * price

                            break
        print('---------')
        for asset, value in self.assets.items():
            print(f'Currency: {asset}, Quantity: {value}')

    def __repr__(self):
        return f'Currency: {self.name}, Initial value: {self.init_quantity} ' \
               f'Current active value: {self.quantity}'

    def check_for_profit(self, obj, other_obj, profit_percentage, price_dict):
        max_profits = []

        for asset, qty in self.assets.items():
            if asset != obj.name:
                pair = f'{asset}/{obj.name}'
                if pair in price_dict:
                    possible_profit = (obj.quantity / price_dict[pair]) / self.assets[asset]
                    if possible_profit >= profit_percentage:
                        max_profits.append((asset, possible_profit, pair))
                else:
                    pair = f'{obj.name}/{asset}'
                    possible_profit = (obj.quantity * price_dict[pair]) / self.assets[asset]
                    if possible_profit >= profit_percentage:
                        max_profits.append((asset, possible_profit, pair))

        if not max_profits:
            return False, ''
        sorted_max_profits = sorted(max_profits, key=lambda x: x[1], reverse=True)
        pair = sorted_max_profits[0][2]
        return True, pair

    def execution(self, obj, pair, index):
        print('-------EXECUTION-------')

        symbol = ''.join(pair.split('/'))

        price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        left_asset, right_asset = pair.split('/')
        if obj.name == left_asset:
            precise_num = Assets.get_accuracy_num(symbol)[0]
            trade_qty = Assets.get_precise_qty(obj.quantity, precise_num)
            print(f'Quantity for trade: {trade_qty}')
            self.assets[right_asset] = trade_qty * price
            print(f'{trade_qty} {obj.name} -> {self.assets[right_asset]} {right_asset} на цена {price}')
            obj.name = right_asset
            obj.quantity = self.assets[right_asset]


        else:
            precise_num = Assets.get_accuracy_num(symbol)[1]
            trade_qty = Assets.get_precise_qty(obj.quantity, precise_num)
            print(f'Quantity for trade: {trade_qty}')
            self.assets[left_asset] = trade_qty / price
            print(f'{trade_qty} {obj.name} -> {self.assets[left_asset]} {left_asset} on price {price}')
            obj.name = left_asset
            obj.quantity = self.assets[left_asset]

        print('---------')
        for asset, value in self.assets.items():
            print(f'Currency: {asset}, quantity: {value}')

    def get_next_prices(self, asset_on_charge, asset_pairs_list, profit_percentage):
        asset_on_charge_qty = self.assets[asset_on_charge]
        result = ''
        for asset, quantity in self.assets.items():
            if asset != asset_on_charge:

                if f'{asset_on_charge}/{asset}' in asset_pairs_list:

                    price = quantity * profit_percentage / asset_on_charge_qty
                    result += f'{asset} Next up price: {price}\n'
                else:
                    price = asset_on_charge_qty / (quantity * profit_percentage)
                    result += f'{asset} Next down price: {price}\n'
        return result.strip()
