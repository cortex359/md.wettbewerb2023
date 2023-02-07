// 
// Decompiled by Procyon v0.5.36
// 

public class Punkt
{
    double x;
    double y;
    
    public Punkt(final double x, final double y) {
        this.x = x;
        this.y = y;
    }
    
    public double berechneAbstandZuPunkt(final Punkt punkt) {
        return Math.sqrt(Math.pow(this.x - punkt.x, 2.0) + Math.pow(this.y - punkt.y, 2.0));
    }
}
