import javax.swing.*;
import java.time.*;
import java.util.ArrayList;

public class Main {



    public static void main(String[] args) {
        System.out.println("Hello, World!");

        var example = new Fisrt[3];

        example[0] = new Fisrt("1", "2");
        example[1] = new Fisrt("3", "4");
        example[2] = new Fisrt("5", "6");

        for (Fisrt e : example)
            e.Print();

        for (Fisrt e : example)
            System.out.println(e.getCounter());

        if (example[0] instanceof Fisrt) {
            System.out.println("This is instance");
        }
        var worker1 = new Worker("vlad", "null");
        System.out.println(worker1.getDescription());
        var workers = new ArrayList<Worker>();
        workers.add(new Worker("jack", "nil"));
        Worker w1 = workers.get(0);
        System.out.println(w1.frm(1.0,2.0,3.0));
        workers.add(new Worker("bill", "oops"));

        for (Worker w : workers)
            System.out.println(w.getDescription());

        workers.remove(1);

        for (Worker w : workers)
            System.out.println(w.getDescription());
    }
}

class Fisrt{
    private String name;
    private String value;
    private Integer counter;
    public static Integer id = 1;

    public Fisrt(String name, String value){
        this.name = name;
        this.value = value;
    }

    public void setCounter(Integer counter) {
        this.counter = counter;
    }

    public String getCounter(){
        if (this.counter == null)
            {
                return "Crash";
            }
        else
        {
            return this.counter.toString();
        }

    }

    public void PlusCounter(){
        this.counter++;
        System.out.println(this.counter);
    }

    public void Print(){
        System.out.println(this.name + "__" + this.value);
    }

}

class Second extends Fisrt{

    public Second(String name, String value) {
        super(name, value);
        this.bonus = 0;
    }

    private double bonus;

    public void setBonus(double b){
        this.bonus = b;

    }

    public double getBonus(){
        return this.bonus;
    }

    @Override
    public String getCounter() {
        return super.getCounter();
    }
}

final class Third extends Fisrt{
    public Third(String name, String value){
        super(name, value);

    }
}

abstract class Person{
    private String name;

    public Person(String name)
    {
        this.name = name;
    }

    public abstract String getDescription();

    public String getName(){
        return this.name;
    }
}

class Worker extends Person{
    private String magor;

    public Worker(String name, String major){
        super(name);
        this.magor = major;
    }

    public String getDescription(){
        return "a worker " + this.getName() + " in " + this.magor;
    }

    public String frm(Double... values){
        String result = "";
        for (Double v : values){
            result = result + v.toString();
        }
        return result.toString();
    }
}