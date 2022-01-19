'Ref: https://github.com/jakobbossek/ecr2
 Ref: http://www.jakobbossek.de/pdf/B2017ecr.pdf
'

# Load Libraries
library(ecr)
library(ggplot2)
library(smoof)


# Find Global Minima of Ackley-Funciton
fn = makeAckleyFunction(1L)
autoplot(fn, show.optimum=TRUE, length.out = 1000)
