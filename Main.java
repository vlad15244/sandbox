public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");

        Fisrt fisrt_ex = new Fisrt("null", "null");
        fisrt_ex.Print();

    }


}


class Fisrt{
    private String name;
    private String value;

    public Fisrt(String name, String value){
        this.name = name;
        this.value = value;
    }

    public void Print(){
        System.out.println(this.name);        
    }

}