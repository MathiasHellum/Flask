from src import app

if __name__ == '__main__':
    app.run(host="localhost", debug=True)# debug=True gir live-endringer i localhost ved kode oppdatering
    # set host="0.0.0.0" to make available on local network, i.e. available to others on the same network.
