import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

public class App {
    public static void main(String[] args) {
        ActionHandler action = new ActionHandler();
        // Создание окна (Frame)
        JFrame frame = new JFrame("Пример Приложения");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 480);

        // 1. Отключаем менеджер компоновки
        frame.setLayout(null); 

        // Создание панели и компонентов
        JPanel panel = new JPanel();
        panel.setLayout(null);
        panel.setBounds(0, 0, 800, 480); // x, y, width, height
        JButton button = new JButton("Нажми меня");
        button.setBounds(10, 10, 120, 30);
        JLabel label = new JLabel("Привет, VS Code!");
        label.setBounds(150, 10, 120, 30);
        button.addActionListener(e-> action.data_bind(label));
        panel.add(button);
        panel.add(label);        

    
        // Добавление панели в окно
        frame.add(panel);
        // Отображение окна
        frame.setVisible(true);
    }
}

class ActionHandler {
    public void handle() {
        System.out.println("Действие из другого класса");
    }

    public void data_bind(JLabel label){

        label.setText("Изменено из метода");
        System.out.println("Пример изменения текста"); 
             
    }
}