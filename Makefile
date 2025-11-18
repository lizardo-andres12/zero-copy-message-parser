compile: main.cpp
	g++ -Wall -Werror -pedantic-errors -O3 -march=native main.cpp -o main.out

run: main.out market_data.bin
	./main.out AAPL < market_data.bin

clean:
	@rm -rf *.out *.o

gentest: test_generator.py
	@python test_generator.py

gentest-dbg: test_generator.py
	@DEBUG=1 python test_generator.py > output.txt
	@echo "Debug output written to output.txt"
