package client;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class ClientThread implements Runnable {
    private Socket socket;
    private BufferedReader reader;
    private PrintWriter writer;

    private Callback callback;
    private String hostname;
    private int port;

    private boolean running = true;

    public ClientThread(Callback callback, String hostname, int port) {
        this.callback = callback;
        this.hostname = hostname;
        this.port = port;
    }

    @Override
    public void run() {
        try {
            socket = new Socket(hostname, port);
            writer = new PrintWriter(socket.getOutputStream(), true);
            reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            while (running) {
                String message = reader.readLine();

                if (message == null)
                    break;

                callback.MessageReceived(message);
            }
        } catch (Exception ex) {
            System.out.println(ex.toString());
        }
    }
}