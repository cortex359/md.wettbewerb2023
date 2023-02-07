import java.io.IOException;

// 
// Decompiled by Procyon v0.5.36
// 

public class Main
{
    public static void main(final String[] array) {
        try {
            if (array.length < 2 || array.length > 2) {
                System.err.println("usage: java -jar checker.jar <inputfile> <resultfile>");
                System.exit(-1);
            }
            if (array.length == 2) {
                new Wald(array[0], array[1]);
            }
        }
        catch (IOException ex) {
            ex.printStackTrace();
            System.exit(-1);
        }
    }
}
