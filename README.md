## How segregation formed?

### -Simulation of Schelling's model of segregation.

Schelling's model of segregation is a classic example of agent-based model developed by economist Thomas Schelling in 2010. By simulation settlement and migration of different groups of agents, the model shows that even without external factors, people's in-group preference may lead different groups tends to becoming more segregated.

### Model Description
The model is set in a n $\times$ n grid, where each point means a space for agents to occupy. Agents will be split into two or more groups. The initial distribution of agents is random. Since we suppose agents have preference towards their own group, they may choose to relocate if the fraction is not high enough.

### Basic Assumption
$\bullet$ The model is set in a 500 $\times$ 500 grid, with 90% empty ratio, which means there’re 25,000 agents in this model;

$\bullet$ There is no more than one agent in a square at one time;

$\bullet$ We set two different groups, one colored in red and another in blue, the ratio is 7:3;

$\bullet$ Initial distribution and relocation are totally random, and we use random.seed to make sure the result is repeatable;

$\bullet$ **Relocation rule**: If the number of same-group agents out of the nearest s agents is less than t, then this agent relocates. By the way, we use Manhattan distance in our model since it’s set in a grid.

### Different Strategy
**Model 1**: s=5, t=3;

**Model 1.5**: s=8, t=5;

**Model 2**: s=5, t=3; A certain ratio(2%) agents moving in or out; this rule’s priority higher than relocation criterion;

**Model 3**: s=5, t=3; There exists one leader(no-moving) for each group, and sgents adjacent to leader of his group won’t move(highest priority); A certain ratio(2%) agents moving in or out;
