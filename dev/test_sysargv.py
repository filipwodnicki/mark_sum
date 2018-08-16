import sys

def main():
	print ( 'Number of arguments:', len(sys.argv), 'arguments.' )
	print ( 'Argument List:', str(sys.argv) )
	print ( 'Arg #0:', str(sys.argv[0]))
	print ( 'Arg #1:', str(sys.argv[1]))

if __name__ == '__main__':
	main()