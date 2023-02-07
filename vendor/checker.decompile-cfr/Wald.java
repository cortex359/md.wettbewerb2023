/*
 * Decompiled with CFR 0.150.
 */
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Scanner;

public class Wald {
    private String name;
    double breite;
    double tiefe;
    double[] radien;
    String[] names;
    private List<Bepflanzung> aktBepflanzung = new ArrayList<Bepflanzung>();
    private static final double EPSILON = 1.0E-10;

    private void readInput(String string) throws IOException {
        Scanner scanner = new Scanner(new File(string));
        this.name = scanner.nextLine();
        Scanner scanner2 = new Scanner(scanner.nextLine());
        this.breite = scanner2.nextDouble();
        this.tiefe = scanner2.nextDouble();
        scanner2.close();
        ArrayList<Double> arrayList = new ArrayList<Double>();
        ArrayList<String> arrayList2 = new ArrayList<String>();
        while (scanner.hasNextLine()) {
            arrayList.add(scanner.nextDouble());
            arrayList2.add(scanner.nextLine());
        }
        this.radien = new double[arrayList.size()];
        this.names = new String[arrayList.size()];
        for (int i = 0; i < arrayList.size(); ++i) {
            this.radien[i] = (Double)arrayList.get(i);
            this.names[i] = (String)arrayList2.get(i);
        }
        scanner.close();
    }

    private void errorQuit(String string, int n, String string2) {
        System.err.println("Fehler in Zeile " + n + ": " + string + "!");
        if (string2 != "") {
            System.out.println("  " + n + ": " + string2);
        }
        System.out.println();
        System.exit(-1);
    }

    private void readResult(String string) throws IOException {
        Scanner scanner = new Scanner(new File(string));
        scanner.useLocale(Locale.US);
        int n = 1;
        while (scanner.hasNextLine()) {
            double d = scanner.nextDouble();
            double d2 = scanner.nextDouble();
            double d3 = scanner.nextDouble();
            int n2 = scanner.nextInt();
            scanner.nextLine();
            String string2 = d + " " + d2 + " " + d3 + " " + n2;
            if (n2 < 0 || n2 >= this.radien.length) {
                this.errorQuit("Index nicht im gueltigen Bereich (0 <= index < " + this.radien.length + ")", n, string2);
            }
            if (d3 != this.radien[n2]) {
                this.errorQuit("Radius ist " + d3 + ", sollte sein " + this.radien[n2], n, string2);
            }
            Punkt punkt = new Punkt(d, d2);
            this.aktBepflanzung.add(new Bepflanzung(punkt, n2));
            ++n;
        }
    }

    private String testRadius(Bepflanzung bepflanzung) {
        Object object = "";
        Punkt punkt = bepflanzung.p;
        int n = bepflanzung.i;
        int n2 = 1;
        for (Bepflanzung bepflanzung2 : this.aktBepflanzung) {
            if (punkt.berechneAbstandZuPunkt(bepflanzung2.p) < this.radien[bepflanzung2.i] + this.radien[n] - 1.0E-10 && bepflanzung != bepflanzung2) {
                object = bepflanzung.toString(this.radien) + "\n";
                object = (String)object + "    ueberschneidet Radius von Punkt\n";
                object = (String)object + bepflanzung2.toString(this.radien, n2);
                return object;
            }
            ++n2;
        }
        return object;
    }

    public Wald(String string, String string2) throws IOException {
        this.readInput(string);
        System.out.println("Pruefe Datei " + string2);
        this.readResult(string2);
        int n = 1;
        for (Bepflanzung bepflanzung : this.aktBepflanzung) {
            String string3;
            double d = this.radien[bepflanzung.i];
            if (bepflanzung.p.x - d < 0.0 || bepflanzung.p.x + d > this.breite || bepflanzung.p.y - d < 0.0 || bepflanzung.p.y + d > this.tiefe) {
                this.errorQuit("Radius geht ueber die Feldbegrenzung hinaus", n, bepflanzung.toString(this.radien));
            }
            if ((string3 = this.testRadius(bepflanzung)) != "") {
                this.errorQuit("Radien ueberlappen sich", n, string3);
            }
            ++n;
        }
        System.out.println("Datei " + string2 + " ist OK!");
        System.out.println();
    }
}

