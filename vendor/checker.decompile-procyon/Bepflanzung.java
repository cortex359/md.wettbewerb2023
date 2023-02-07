// 
// Decompiled by Procyon v0.5.36
// 

public class Bepflanzung
{
    Punkt p;
    int i;
    
    public Bepflanzung(final Punkt p2, final int i) {
        this.p = p2;
        this.i = i;
    }
    
    public void gibAus(final double[] array) {
        System.out.printf("x=%.15f, y=%.15f, r=%.15f\n", this.p.x, this.p.y, array[this.i]);
    }
    
    public String toString(final double[] array) {
        return invokedynamic(makeConcatWithConstants:(DDDI)Ljava/lang/String;, this.p.x, this.p.y, array[this.i], this.i);
    }
    
    public String toString(final double[] array, final int n) {
        return invokedynamic(makeConcatWithConstants:(ILjava/lang/String;)Ljava/lang/String;, n, this.toString(array));
    }
}
