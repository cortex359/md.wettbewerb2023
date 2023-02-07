import java.util.Iterator;
import java.util.Locale;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;
import java.io.File;
import java.util.List;

// 
// Decompiled by Procyon v0.5.36
// 

public class Wald
{
    private String name;
    double breite;
    double tiefe;
    double[] radien;
    String[] names;
    private List<Bepflanzung> aktBepflanzung;
    private static final double EPSILON = 1.0E-10;
    
    private void readInput(final String pathname) throws IOException {
        final Scanner scanner = new Scanner(new File(pathname));
        this.name = scanner.nextLine();
        final Scanner scanner2 = new Scanner(scanner.nextLine());
        this.breite = scanner2.nextDouble();
        this.tiefe = scanner2.nextDouble();
        scanner2.close();
        final ArrayList<Double> list = new ArrayList<Double>();
        final ArrayList<String> list2 = new ArrayList<String>();
        while (scanner.hasNextLine()) {
            list.add(scanner.nextDouble());
            list2.add(scanner.nextLine());
        }
        this.radien = new double[list.size()];
        this.names = new String[list.size()];
        for (int i = 0; i < list.size(); ++i) {
            this.radien[i] = list.get(i);
            this.names[i] = list2.get(i);
        }
        scanner.close();
    }
    
    private void errorQuit(final String s, final int n, final String s2) {
        System.err.println(invokedynamic(makeConcatWithConstants:(ILjava/lang/String;)Ljava/lang/String;, n, s));
        if (s2 != "") {
            System.out.println(invokedynamic(makeConcatWithConstants:(ILjava/lang/String;)Ljava/lang/String;, n, s2));
        }
        System.out.println();
        System.exit(-1);
    }
    
    private void readResult(final String pathname) throws IOException {
        final Scanner scanner = new Scanner(new File(pathname));
        scanner.useLocale(Locale.US);
        int n = 1;
        while (scanner.hasNextLine()) {
            final double nextDouble = scanner.nextDouble();
            final double nextDouble2 = scanner.nextDouble();
            final double nextDouble3 = scanner.nextDouble();
            final int nextInt = scanner.nextInt();
            scanner.nextLine();
            final String s = invokedynamic(makeConcatWithConstants:(DDDI)Ljava/lang/String;, nextDouble, nextDouble2, nextDouble3, nextInt);
            if (nextInt < 0 || nextInt >= this.radien.length) {
                this.errorQuit(invokedynamic(makeConcatWithConstants:(I)Ljava/lang/String;, this.radien.length), n, s);
            }
            if (nextDouble3 != this.radien[nextInt]) {
                this.errorQuit(invokedynamic(makeConcatWithConstants:(DD)Ljava/lang/String;, nextDouble3, this.radien[nextInt]), n, s);
            }
            this.aktBepflanzung.add(new Bepflanzung(new Punkt(nextDouble, nextDouble2), nextInt));
            ++n;
        }
    }
    
    private String testRadius(final Bepflanzung bepflanzung) {
        final String s = "";
        final Punkt p = bepflanzung.p;
        final int i = bepflanzung.i;
        int n = 1;
        for (final Bepflanzung bepflanzung2 : this.aktBepflanzung) {
            if (p.berechneAbstandZuPunkt(bepflanzung2.p) < this.radien[bepflanzung2.i] + this.radien[i] - 1.0E-10 && bepflanzung != bepflanzung2) {
                return invokedynamic(makeConcatWithConstants:(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;, invokedynamic(makeConcatWithConstants:(Ljava/lang/String;)Ljava/lang/String;, invokedynamic(makeConcatWithConstants:(Ljava/lang/String;)Ljava/lang/String;, bepflanzung.toString(this.radien))), bepflanzung2.toString(this.radien, n));
            }
            ++n;
        }
        return s;
    }
    
    public Wald(final String s, final String s2) throws IOException {
        this.aktBepflanzung = new ArrayList<Bepflanzung>();
        this.readInput(s);
        System.out.println(invokedynamic(makeConcatWithConstants:(Ljava/lang/String;)Ljava/lang/String;, s2));
        this.readResult(s2);
        int n = 1;
        for (final Bepflanzung bepflanzung : this.aktBepflanzung) {
            final double n2 = this.radien[bepflanzung.i];
            if (bepflanzung.p.x - n2 < 0.0 || bepflanzung.p.x + n2 > this.breite || bepflanzung.p.y - n2 < 0.0 || bepflanzung.p.y + n2 > this.tiefe) {
                this.errorQuit("Radius geht ueber die Feldbegrenzung hinaus", n, bepflanzung.toString(this.radien));
            }
            final String testRadius = this.testRadius(bepflanzung);
            if (testRadius != "") {
                this.errorQuit("Radien ueberlappen sich", n, testRadius);
            }
            ++n;
        }
        System.out.println(invokedynamic(makeConcatWithConstants:(Ljava/lang/String;)Ljava/lang/String;, s2));
        System.out.println();
    }
}
