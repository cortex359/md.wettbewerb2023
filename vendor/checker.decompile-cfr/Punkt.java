/*
 * Decompiled with CFR 0.150.
 */
public class Punkt {
    double x;
    double y;

    public Punkt(double d, double d2) {
        this.x = d;
        this.y = d2;
    }

    public double berechneAbstandZuPunkt(Punkt punkt) {
        return Math.sqrt(Math.pow(this.x - punkt.x, 2.0) + Math.pow(this.y - punkt.y, 2.0));
    }
}

