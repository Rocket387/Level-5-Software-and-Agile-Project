from NoteKeeper import create_app

#### Start command for executing the app first time ####
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    

