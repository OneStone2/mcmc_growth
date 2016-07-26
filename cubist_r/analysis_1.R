setwd('~/workspace/mcmc_growth')
x <- read.csv("data/ME/ME_2a.csv", as.is=T)
r1 <- x[["carb"]]
r2 <- x[["py"]]
r3 <- x[["human_p"]]
r4 <- x[["human_n"]]
x <- x[-c(nrow(x)),]
r1 <- r1[-c(1)]
r2 <- r2[-c(1)]
r3 <- r3[-c(1)]
r4 <- r4[-c(1)]
x["post_py"] <- r2
x["growth"] <- (x["carb"]-r1)/(x["py"]-x["post_py"])
x["human_p"] <- r3
x["human_n"] <- r4
x <- x[x[,"py"] %/% 10000 == x[,"post_py"] %/% 10000,]
#x <- x[, names(x) %in% c("py","post_py","growth","carb","lat","lon")]
row.names(x) <- 1:nrow(x)

X <- x[, !names(x) %in% c("growth","py","post_py")]
Y <- x[,names(x) %in% "growth"]

groups <- split(1:nrow(x), sample(1:10, nrow(x), replace=T))

min_mse = Inf
for (i in 1:10) {
  rows <- groups[[i]]
  X1 <- X[-rows, ]
  X2 <- X[rows, ]
  Y1 <- Y[-rows]
  Y2 <- Y[rows]
   
  pkgs <- c('doMC', 'Cubist', 'caret')
  lapply(pkgs, require, character.only = T)
  registerDoMC(core = 7)
  mdl2 <- cubist(x = X1, y = Y1, commitees = 1, control = cubistControl(unbiased = TRUE, rules = 999, label = "growth"))
  mse <- sqrt(sum((Y2 -predict(mdl2, newdata = X2)) ^ 2)/length(Y2))
  if (mse < min_mse) min_mse <- mse
}
print(min_mse)