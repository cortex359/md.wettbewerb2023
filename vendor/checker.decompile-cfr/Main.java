/*
 * Decompiled with CFR 0.150.
 */
import java.io.IOException;

public class Main {
    public static void main(String[] arrstring) {
        try {
            if (arrstring.length < 2 || arrstring.length > 2) {
                System.err.println("usage: java -jar checker.jar <inputfile> <resultfile>");
                System.exit(-1);
            }
            if (arrstring.length == 2) {
                new Wald(arrstring[0], arrstring[1]);
            }
        }
        catch (IOException iOException) {
            iOException.printStackTrace();
            System.exit(-1);
        }
    }
}

