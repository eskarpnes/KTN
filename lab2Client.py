# This skeleton is valid for both Python 2.7 and Python 3.
# You should be aware of your additional code for compatibility of the Python version of your choice.

from time import *
from socket import *

def get_time_millis():
    return round(time()*1000)

# Get the server hostname and port as command line arguments
host = input("Please enter the hostname: ")
port = int(input("Please enter the port: "))
timeoutTime = 1  # in seconds

# Create UDP client socket
# FILL IN START
clientSocket = socket(AF_INET, SOCK_DGRAM)
# Note the second parameter is NOT SOCK_STREAM
# but the corresponding to UDP

# Set socket timeout as 1 second
clientSocket.settimeout(timeoutTime)

# FILL IN END

# Sequence number of the ping message
ptime = 0

# Ping for 10 times
while ptime < 10:
    ptime += 1
    # Format the message to be sent as in the Lab description

    sentTime = get_time_millis()

    data = "Ping " + str(ptime) + " " + str(sentTime)

    try:
        # Send the UDP packet with the ping message
        clientSocket.sendto(data.encode(), (host, port))
        # Receive the server response
        returned, server_address = clientSocket.recvfrom(1024)
        # Record the "received time"
        receiveTime = get_time_millis()
        # Display the server response as an output
        print(returned)
        # Round trip time is the difference between sent and received time
        print("Sent: " + str(sentTime))
        print("Received: " + str(receiveTime))
        print("RTT: " + str(receiveTime-sentTime) + "ms")
    except timeout:
        # Server does not response
        # Assume the packet is lost
        print("Request timed out.")
        continue

# Close the client socket
clientSocket.close()

