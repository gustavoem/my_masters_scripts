CFLAGS = -g -Wall -O0 -ansi -pedantic -Wno-unused-result
CC = gcc
LDFLAGS = -I/usr/local/include  -L/usr/local/lib -lsundials_cvode \
	-lsundials_nvecserial -lm /usr/lib/x86_64-linux-gnu/librt.so \
	-Wl,-rpath,/usr/local/lib 
integrate: integrate.o scvodew.o
	$(CC) integrate.o  scvodew.o -o integrate $(LDFLAGS)

integrate.o: integrate.c scvodew.o
	$(CC) -I/home/gustavo/cs/SimpleCVODEWrapper -c integrate.c

scvodew.o: /home/gustavo/cs/SimpleCVODEWrapper/scvodew.h /home/gustavo/cs/SimpleCVODEWrapper/scvodew.c
	$(CC) -I/home/gustavo/cs/SimpleCVODEWrapper -c /home/gustavo/cs/SimpleCVODEWrapper/scvodew.c

clean:
	rm *.o
