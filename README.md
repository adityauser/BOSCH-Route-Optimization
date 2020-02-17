# BOSCH-Route-Optimization
This repository contain code which we submitted for BOSCH Route Optimization at Inter IIT Tech Meet 8.0

## Problem Statement
To develop a route optimization algorithm considering following
constraints:
* Minimize operational cost.
* Number of buses
* Vehicle occupancy should be at least 85%.
* Time window for pick up and drop off.

## Solution Approach
There are two approaches to solve this problem:
* Mathematical Model
* Meta-Heuristic Algorithm

### Mathematical Model
**Objective**: Minimize operational cost
Constraints:
* Only one bus will visit one bus stop once in a day.
* Path defining contraints.
* Distance and time limit contraints.
* Capacity and subtour elimination contraints.

### Ant Colony Method 
* The edge selection is biased towards exploitation (i.e. favoring the probability of selecting the shortest edges with a large amount of pheromone).
* Ants change the pheromone level of the edges they are selecting by applying a local pheromone updating rule 
* The best ant is allowed to update the trails by applying a modified global pheromone updating rule.

## Content
* <a href="https://github.com/adityauser/BOSCH-Route-Optimization/blob/master/BOSCH_PS.pdf">Probelem Discription</a>
* <a href="https://github.com/adityauser/BOSCH-Route-Optimization/blob/master/Input Data.xlsx">Input Data(i.e. Locations)</a>
* <a href="https://github.com/adityauser/BOSCH-Route-Optimization/blob/master/a.xlsx">Processed data</a>: Distance and Time matrix
* <a href="https://github.com/adityauser/BOSCH-Route-Optimization/blob/master/BOSCH_MP.py">Mathematical Model</a>
* <a href="https://github.com/adityauser/BOSCH-Route-Optimization/blob/master/AntColonyMethod.py">Ant Colony Method</a>
* <a href="https://github.com/adityauser/BOSCH-Route-Optimization/blob/master/Presentation.pptx">Presentation</a>




