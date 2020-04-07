---
layout: post
title: "Agent Based Modeling: Diffusion"
date: 2020-08-03 16:48:38 -0400
category: mathematical-modeling
author: teddy
short-description: A first glance at diffusion processes via an agent based model.
---

# Agent-Based Models (ABMs) 
ABMs are computer programs that model each agent individually. These kind of models allow for a greater level of granularlity than models of system dynamics which represent an entire population with a single variable. ABMs place agents in space and can
include behavioral density. Behvaioral density is something we see in social revolutions, epidemics birds flocking (murmurations). These added degrees of freedom offer their own advantages, but with any kind of modelling, too much detail undermines some
of our reasons to model.


## Diffusion
This model shows 1000 agents in space. 200 are immune (labeled as "Recovered"), 100 are infected and 700 are susceptible. We might think about this as a virus diffusing amongs the agents or a rumor spreading
amongst a group of people. It is up to you to define how the diffusion occurs. Beware, the parameters are sensitive and can suddenly change the entire state of the model.

Go and play with the model [here](https://teddypender.github.io/abm_diffusion).

## More soon.
