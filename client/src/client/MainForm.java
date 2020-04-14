package client;

import java.awt.FlowLayout;
import javax.swing.JFrame;
import javax.swing.JTextArea;

public class MainForm extends JFrame implements Callback {

    private JTextArea textarea;
    private ClientThread client;

    public MainForm() {
        initializeComponents();

        client = new ClientThread(this, "172.16.20.9", 80);
        new Thread(client).start();
    }

    @Override
    public void MessageReceived(String message) {
        textarea.append(message + "\n");
    }

    private void initializeComponents() {
        setTitle("Client");
        setSize(400, 300);
        setLayout(new FlowLayout());

        textarea = new JTextArea(10, 30);
        add(textarea);

        setVisible(true);
    }
}