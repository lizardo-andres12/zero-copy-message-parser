"""
Script meant to generate test data for the trading message parser.

Data has the following format:
    [Header: 8 bytes][Symbol: 8 bytes][Price: 8 bytes][Quantity: 4 bytes] Total: 28 bytes per message

The script uses the random library to randomly generate stock data and store it in a messages list. A
hardcoded variant would look like this:
    messages = [
        (1, b'AAPL\x00\x00\x00\x00', 15025, 100),  # $150.25, 100 shares
        (1, b'GOOGL\x00\x00\x00', 280050, 50),     # $2800.50, 50 shares
        (1, b'AAPL\x00\x00\x00\x00', 15050, 200),  # $150.50, 200 shares
        (1, b'AAPL\x00\x00\x00\x00', 15030, 150),  # $150.30, 150 shares
        (1, b'GOOGL\x00\x00\x00', 280100, 75),     # $2801.00, 75 shares
    ]

Prices for each symbol are generated and the `random` library will then generate small deviations. For example,
AAPL is randomly assigned the price 15000. The random number generator outputs 45, so the stored message would
be (1, AAPL..., 15045, ...). Quantity of shares is randomly generated as well and is guaranteed to be positive
and non-zero.
"""


import struct
import os
from random import choice, randint


DEBUG = os.getenv("DEBUG", 0)


symbols = [
    b'GOOGL\x00\x00\x00',
    b'AAPL\x00\x00\x00\x00',
    b'NVDA\x00\x00\x00\x00',
    b'PLTR\x00\x00\x00\x00',
    b'MSFT\x00\x00\x00\x00',
    b'AMZN\x00\x00\x00\x00'
]


def random_message_generator(num_messages: int):
    # This will store the first price generated as baseline for deviations
    symbol_to_base_price_map = {}

    for _ in range(num_messages):
        symbol = choice(symbols)

        if symbol not in symbol_to_base_price_map:
            large_order_price = randint(1, 20) * 10_000 # This will be the full dollar amount in hundreds
            small_order_price = randint(1, 9) * 10 # This will be the "cents"

            symbol_to_base_price_map[symbol] = large_order_price + small_order_price

        base_price = symbol_to_base_price_map[symbol]
        deviation = randint(-10, 10) * 10
        quantity = randint(1, 20) * 10
        yield (1, symbol, base_price + deviation, quantity)


def create_message_list():
    # Somewehere between 800-1200 messages generated
    num_messages = randint(800, 1200)
    return [message for message in random_message_generator(num_messages)]


def generate_test_data(filename):
    
    with open(filename, 'wb') as f:
        messages = create_message_list()

        # Write number of messages
        f.write(struct.pack('<Q', len(messages)))
        
        # Write each message
        for header, symbol, price, quantity in messages:
            f.write(struct.pack('<Q', header))
            f.write(symbol)
            f.write(struct.pack('<Q', price))
            f.write(struct.pack('<I', quantity))

        if DEBUG:
            print(f'num_messages: {len(messages)}\nmessages:')
            for message in messages:
                print(f'symbol: {message[1]}, price: {message[2]}, quantity: {message[3]}')

if __name__ == '__main__':
    generate_test_data('market_data.bin')
    print("Generated market_data.bin")

