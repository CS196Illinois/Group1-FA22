int main() {
    // I'm not using encapsulation here for the sake of brevity...
    public class Person {
        public String name;
    }
    // Student extends Person and so inherits its state and behavior
    public class Student extends Person {
        public String level;
    }
    
    Student you = new Student();
    // This already makes sense to us: Student has an String instance variable named level
    // It's declared in the declaration of Student
    you.level = "Freshman";
    // But where is this instance variable coming from?
    // It's inherited from Person!
    you.name = "Excellent Student";
    System.out.println(you.name + " is a " + you.level);
}