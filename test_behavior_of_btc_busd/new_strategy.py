'''
    Description:

    Testing the behavior of two crypto assets - BTC and BUSD - according to
price changes. The price is controlled by the user - 'w' key for
moving up, 's' key for moving down. 'Step' class variable defines the size of the price
'jumps' in percentage - 1.01 is 1%. 'Percent_to_decrease_qty' controls how much
of the asset will be traded on as percentage too. The program calculates total quantities of both assets.
'''

class NewStrategy:
    # Measured as percentage
    step = 1.01
    INIT_PRICE = 20000
    percent_to_decrease_qty = 1.20
    BTC = 0.05
    BUSD = BTC * INIT_PRICE

    def get_total_qties(self, btc, busd, price):
        total_busd = busd + btc * price
        total_btc = btc + busd / price
        return total_btc, total_busd

    def control_price_movement(self):
        while True:
            choice = input('Choose direction: "w" for up, "s" for down: ')
            if choice == 'w':
                self.INIT_PRICE *= self.step
            elif choice == 's':
                self.INIT_PRICE /= self.step
            else:
                print('Wrong key! Try again...')
                continue
            new_btc_qty = self.BTC / self.percent_to_decrease_qty
            diff_btc = self.BTC - new_btc_qty
            self.BUSD += diff_btc * self.INIT_PRICE
            self.BTC = new_btc_qty
            total_btc, total_busd = self.get_total_qties(self.BTC, self.BUSD, self.INIT_PRICE)
            print('/' * 50)
            print(f'BTC: {self.BTC:.5f}, BUSD: {self.BUSD:.2f} PRICE: {self.INIT_PRICE:.2f}\n'
                  f'Total BTC: {total_btc:.5f} Total BUSD: {total_busd:.2f}')
            print('/' * 50)


controller = NewStrategy()
print(controller.get_total_qties(controller.BTC, controller.BUSD, controller.INIT_PRICE))
controller.control_price_movement()


