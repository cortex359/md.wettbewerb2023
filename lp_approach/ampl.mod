reset;

param container_width := 50 ;
param container_height := 20 ;

set circle_radius := {3, 4, 6, 9, 12};

param n := 20;

# Define variables
#var num_circles integer >= 1; # Anzahl der Kreise

var x{i in 1..n};  # x-coordinate of center of circle i
var y{i in 1..n};  # y-coordinate of center of circle i
#var r{i in 1..n} integer <= 5;
var r{i in 1..n} in circle_radius;

# Define objective function
maximize area: sum{i in 1..n} r[i] ^2;


# Kreis darf generell nicht größer als Feld sein
#subject to circ_max_radius{i in 1..n}: r[i] <= container_height;
 

# Kreis muss vollständig im rechteckigen Feld liegen
subject to circ_in_rect_w1{i in 1..n}: x[i] + r[i] <= container_width;
subject to circ_in_rect_w0{i in 1..n}: x[i] - r[i] >= 0;
subject to circ_in_rect_h1{i in 1..n}: y[i] + r[i] <= container_height;
subject to circ_in_rect_h0{i in 1..n}: y[i] - r[i] >= 0;

# Kreise dürfen sich nicht überschneiden
subject to no_overlap{i in 1..n, j in 1..n: j > i}: 
	(x[i] - x[j])^2 + (y[i] - y[j])^2 >= (r[i] + r[j])^2;


option solver gurobi;
option gurobi_options 'NonConvex=2';

solve;

# Display the solution
printf "Area: %d\n", (sum{i in 1..n} r[i] ^2 * 3.14159265);

for{i in 1..n}{
  printf "Circle %d: Center (%g,%g), Radius %g\n", i, x[i], y[i], r[i];
}
