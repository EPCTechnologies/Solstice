# Solstice

An algorithm is proposed in Python to automate the sorting of music tracks to generate a feasible tracklist for listening or DJ-ing purposes.
The problem is formulated as a Hamiltonian Path Problem reduced to an Assymetric Travelling Salesman Problem,
with individual tracks in a user's music library represented nodes in a complete directed graph,
and whereby the starting and ending nodes are different and free for optimization.
The edge weights are calculated based on the two key metrics:
the discrepancy between track BPMs, and the incompatibility of the tracks' musical keys.
The incompatibility between keys are measured using common key mixing heuristics using the Camelot wheel
as well as using the Vassilakis' equation for root tone dissonance.
The metrics are passed through a sigmoid squashing function to introduce nonlinearity and then combined using the Cobb-Douglas function.
The problem is solved using a version of the heuristic Genetic Algorithm modified to preserve the properties of the formulated problem.
Applications of this algorithm include the smart sorting of consumers' music libraries in online music streaming platforms, as well as the automated generation of tracklists in radio stations or DJ sets.