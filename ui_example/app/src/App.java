import java.awt.*;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;

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
        panel.setLayout(new FlowLayout());

        JLabel label = new JLabel("Привет, VS Code!");
        JButton button = new JButton("Нажми меня");
        button.setBounds(50, 30, 120, 30); 
        JButton button1 = new JButton("Это новая кнопка");

        // Добавление компонентов на панель
        panel.add(label);
        panel.add(button);
        panel.add(button1);
        button.addActionListener(e -> action.handle());
        // Данные и заголовки
        String[] columns = {"ID", "Имя", "Возраст"};
        Object[][] data = {
            {"1", "Алексей", "25"},
            {"2", "Мария", "30"},
            {"3", "Иван", "22"}
        };

        // Создание модели и таблицы
        DefaultTableModel model = new DefaultTableModel(data, columns);
        JTable table = new JTable(model);
        panel.add(table);      
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

    public void data_bind(){
        System.out.println("Заполнение таблицы данными"); 
             
    }
}