from website import create_app

app = create_app()


 # only if we run this file, are we going to execute this line
    # we dont want to run the web server

if __name__ == '__main__':
    app.run(debug=True) #going to run the flask application. if any changes are made in our code, 
    #it will automatically run the website again

