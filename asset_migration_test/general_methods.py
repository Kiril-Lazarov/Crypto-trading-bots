from asset_migration_test.asset import Asset


class GeneralMethods(Asset):

    def __init__(self, init_qty, name):
        super().__init__(init_qty, name)

    @staticmethod
    def multiply(x, y):
        return x * y

    @staticmethod
    def summation(x, y):
        return x + y

    @staticmethod
    def first_char(asset, pair):
        if asset[0] != pair[0]:
            return -1
        return 1

    @staticmethod
    def cycling_objects(obj_list, asset_on_charge):
        for object in obj_list:
            if object.name == asset_on_charge:
                return object

    @staticmethod
    def check_for_profit(asset_on_charge, prices_dict, obj_list, profit_percentage):
        max_profits_list = []

        for pair, price in prices_dict.items():
            if asset_on_charge == pair.split('/')[0]:
                object1 = GeneralMethods.cycling_objects(obj_list, asset_on_charge)
                object2 = GeneralMethods.cycling_objects(obj_list, pair.split('/')[1])
                trade_qty = GeneralMethods.multiply(object1.quantity, price)
                possible_profit = object2.quantity * profit_percentage
                if trade_qty >= possible_profit:
                    max_profits_list.append((object2, trade_qty, price, object2.name))

            elif asset_on_charge == pair.split('/')[1]:
                object1 = GeneralMethods.cycling_objects(obj_list, asset_on_charge)
                object2 = GeneralMethods.cycling_objects(obj_list, pair.split('/')[0])
                trade_qty = GeneralMethods.multiply(object1.quantity, 1 / price)
                possible_profit = object2.quantity * profit_percentage
                if trade_qty >= possible_profit:
                    max_profits_list.append((object2, trade_qty, price, object2.name))

        if not max_profits_list:
            return asset_on_charge, 0
        object2, final_trade_qty, price, object2_name = \
            sorted(max_profits_list, key=lambda x: x[1], reverse=True)[0]
        print(f'Price {asset_on_charge}/{object2_name}: {price}')
        object2.quantity = final_trade_qty

        return object2.name, price

    @staticmethod
    def execution_report(previous_asset, asset_on_charge, price, transaction_count):

        return f'--------EXECUTION--------\n' \
               f'Order count: {transaction_count}\n' \
               f'{previous_asset} -> {asset_on_charge} на цена: {price}'

    @staticmethod
    def next_prices(asset_on_charge, asset_dict, asset_pairs_list, profit_percentage):
        asset_on_charge_qty = asset_dict[asset_on_charge]
        result = ''
        for asset, quantity in asset_dict.items():
            if asset != asset_on_charge:
                if f'{asset_on_charge}/{asset}' in asset_pairs_list:
                    price = quantity * profit_percentage / asset_on_charge_qty
                    result += f'{asset} Next high price: {price}\n'
                else:
                    price = asset_on_charge_qty / (quantity * profit_percentage)
                    result += f'{asset} Next low price: {price}\n'
        return result.strip()

    @classmethod
    def normalize_quantities(cls, asset_on_charge, obj_list, prices_dict):
        object1 = GeneralMethods.cycling_objects(obj_list, asset_on_charge)
        result = '\n--------RENORMING---------\n'
        for object in obj_list:
            if obj_list.index(object) < obj_list.index(object1):
                object.quantity = GeneralMethods.multiply(object1.quantity,
                                                          1 / prices_dict[f'{object.name}/{object1.name}'])
            elif obj_list.index(object) > obj_list.index(object1):
                object.quantity = GeneralMethods.multiply(object1.quantity,
                                                          prices_dict[f'{object1.name}/{object.name}'])
        for object in obj_list:
            result += f'{object.name}: {object.quantity} Печалба: {(object.quantity / object.init_qty - 1) * 100:.2f}%\n'
        return result.strip()
