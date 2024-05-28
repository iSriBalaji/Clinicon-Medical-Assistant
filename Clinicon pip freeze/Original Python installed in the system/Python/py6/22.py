while(1):
    try:
        no=int(input())
        break
    except ValueError:
        print("found")
while(1):
    n=int(input())
    if(n==5):
        print("you guessed it")
        break
    else:
        print("Try again")
        
