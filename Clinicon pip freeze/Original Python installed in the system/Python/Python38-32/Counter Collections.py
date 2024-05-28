from collections import Counter 
'''a = Counter("geeksforgeeks")
nm=a.elements()
for i in nm: 
	print ( i, end = " ") 
print() 
	
b = Counter({'geeks' : 4, 'for' : 1, 
			'gfg' : 2, 'python' : 3}) 

for i in b.elements(): 
	print ( i, end = " ") 
print() 
'''
c = Counter([1, 2, 3,2,2,4,4,1,1]) 
print(c)			 
				
d = Counter( [3,3,2,2,4,1,1]) 
print(d)

print(c+d)
print(c-d)
print(d-c)
