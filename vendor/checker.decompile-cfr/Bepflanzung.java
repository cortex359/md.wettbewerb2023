/*
 * Decompiled with CFR 0.150.
 */
public class Bepflanzung {
    Punkt p;
    int i;

    public Bepflanzung(Punkt punkt, int n) {
        this.p = punkt;
        this.i = n;
    }

    public void gibAus(double[] arrd) {
        System.out.printf("x=%.15f, y=%.15f, r=%.15f\n", this.p.x, this.p.y, arrd[this.i]);
    }

    public String toString(double[] arrd) {
        return this.p.x + " " + this.p.y + " " + arrd[this.i] + " " + this.i;
    }

    public String toString(double[] arrd, int n) {
        return "  " + n + ": " + this.toString(arrd);
    }
}

