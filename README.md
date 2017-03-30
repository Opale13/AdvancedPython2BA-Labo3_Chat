Kirstein Julien & Merel Ludovic

Hello, to use our application, it is necessary:
1) Run the application with "server" as argument in a command prompt.
2) Run the application with "client" as argument in another command prompt.

In the client part, u can use two commands to communicate with the server:
1) /clients : the server will give you users logged in with their ip adress.
2) /exit : you will be disconnected from the server.

In the same part, u can use commands for communicate with another client:
1) /join [ip] : Allows to connect to another client with its ip address.
2) /send [message] : Sends a message to the person.
3) /quit : Cuts the connection

Communication protocol server-client/client-server:
The communication is a TCP.
1) Data frame server-client:
The server sends the data frame "server message" on the port 5001 of the client.
2) Client-server:
The client sends a message on the port 5000 of the server.

Communication protocol client-client:
The communication is UDP.
When a client sends a message, the data frame is :
- The number of characters in the user, plus
- the user, plus
- The numbers of characters in the message, plus
- The message
