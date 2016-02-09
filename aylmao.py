import SocketServer
MINCLIENTS = 0

players = {}

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        player, playerX, playerY, bulletX, bulletY = self.data.split(",")
        playerCoords = map(int, [playerX, playerY, bulletX, bulletY])
        players += {player: playerCoords}
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())
    def checkBullets(self):
        for p in players:


if __name__ == "__main__":
    HOST, PORT = "localhost", 5000

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
