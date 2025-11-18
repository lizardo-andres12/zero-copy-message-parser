#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <inttypes.h>
#include <vector>


struct __attribute__((packed)) Message {
    std::uint64_t header;
    char symbol[8];
    std::uint64_t price;
    std::uint32_t quantity;
};


int main(int argc, char** argv) {
    if (argc != 2) {
	fprintf(stderr, "Usage: %s <symbol>\n", argv[0]);
	return 1;
    }

    const char* inputSymbol = argv[1];
    char targetSymbol[8] = {0};
    for (int i = 0; inputSymbol[i] != '\0' && i < 8; ++i) {
	targetSymbol[i] = inputSymbol[i];
    }

    freopen(nullptr, "rb", stdin);

    fseek(stdin, 0, SEEK_END);
    std::size_t fileSize = ftell(stdin);
    fseek(stdin, 0, SEEK_SET);

    std::vector<std::uint8_t> buffer(fileSize);
    fread(buffer.data(), 1, fileSize, stdin);

    const std::uint8_t* bufferPtr = buffer.data();
    const std::uint64_t numMessages = *reinterpret_cast<const std::uint64_t*>(bufferPtr);
    bufferPtr += sizeof(std::uint64_t);
    const Message* messages = reinterpret_cast<const Message*>(bufferPtr);

    std::uint64_t totalPriceByVolume = 0;
    std::uint64_t totalVolume = 0;
    for (std::uint64_t i = 0; i < numMessages; ++i) {
	const Message& curMessage = messages[i];
	if (std::memcmp(curMessage.symbol, targetSymbol, 8) == 0) {
	    totalPriceByVolume += curMessage.price * curMessage.quantity;
	    totalVolume += curMessage.quantity;
	}
    }

    std::uint64_t vwap = totalVolume == 0 ? 0 : totalPriceByVolume / totalVolume;
    fprintf(stdout, "%s %" PRIu64 ".%" PRIu64 " %" PRIu64 "\n", targetSymbol, (vwap / 100), (vwap % 100), totalVolume);
    return 0;
}
