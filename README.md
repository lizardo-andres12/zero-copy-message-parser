## **Task 4: Trade Message Parser with Zero-Copy**
**Difficulty: Advanced**

Program to parse binary market data messages **without copying data**.

### Background:
Market data comes in binary format. A simplified trade message looks like this:

```
[Header: 8 bytes][Symbol: 8 bytes][Price: 8 bytes][Quantity: 4 bytes]
Total: 28 bytes per message
```

**Binary Layout:**
- **Header** (uint64_t): Message type (1=Trade, 2=Quote, etc.) + timestamp
- **Symbol** (char[8]): Stock symbol, null-padded (e.g., "AAPL\0\0\0\0")
- **Price** (uint64_t): Price in cents (e.g., 15025 = $150.25)
- **Quantity** (uint32_t): Number of shares

### Requirements:

Write a program that:

1. Reads binary messages from stdin (use `freopen` for binary mode or redirect binary file)
2. Parses messages **without copying** (use pointers/references to the buffer)
3. Filters for a specific symbol (command line arg)
4. Calculates the VWAP for that symbol across all trades
5. Outputs: `<symbol> <vwap> <total_quantity>`

### Input Format:

- First 8 bytes: number of messages (uint64_t, little-endian)
- Followed by N messages of 28 bytes each

### Example (conceptual):

If you had 3 trades for "AAPL":
- Trade 1: $150.25, 100 shares
- Trade 2: $150.50, 200 shares  
- Trade 3: $150.30, 150 shares

Output:
```
AAPL 150.36 450
```

### Constraints:
- Up to 100,000,000 messages in the input file
- Multiple symbols intermixed
- Messages are in little-endian format (x86/x64 standard)

### Test Data Generation:
I created this Python script to generate test data:

```python
import struct
import sys

def generate_test_data(filename):
    messages = [
        (1, b'AAPL\x00\x00\x00\x00', 15025, 100),  # $150.25, 100 shares
        (1, b'GOOGL\x00\x00\x00', 280050, 50),     # $2800.50, 50 shares
        (1, b'AAPL\x00\x00\x00\x00', 15050, 200),  # $150.50, 200 shares
        (1, b'AAPL\x00\x00\x00\x00', 15030, 150),  # $150.30, 150 shares
        (1, b'GOOGL\x00\x00\x00', 280100, 75),     # $2801.00, 75 shares
    ]
    
    with open(filename, 'wb') as f:
        # Write number of messages
        f.write(struct.pack('<Q', len(messages)))
        
        # Write each message
        for header, symbol, price, quantity in messages:
            f.write(struct.pack('<Q', header))
            f.write(symbol)
            f.write(struct.pack('<Q', price))
            f.write(struct.pack('<I', quantity))

if __name__ == '__main__':
    generate_test_data('market_data.bin')
    print("Generated market_data.bin")
```

Run with: `./main.out AAPL < market_data.bin`
Expected output: `AAPL 150.366667 450`
