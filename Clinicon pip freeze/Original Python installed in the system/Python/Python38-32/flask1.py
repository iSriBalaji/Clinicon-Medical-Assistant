from flask import Flask  
  
app = Flask(__name__) #creating the Flask class object   
app.debug=True
@app.route('/') #decorator drfines the   
def home():  
    return "hello, this is our first flask website";  
  
if __name__ =='__main__':  
    app.run()  
    app.run(debug=True)
