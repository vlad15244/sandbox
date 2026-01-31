public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");

        var example = new Fisrt[3];

        example[0] = new Fisrt("1", "2");
        example[1] = new Fisrt("3", "4");
        example[2] = new Fisrt("5", "6");

        for (Fisrt e: example)
            e.Print();

        for (Fisrt e: example)
            System.out.println(e.getCounter());


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