x <- read.csv("~/workspace/mcmc_growth/data/ME_2a.csv", as.is=T)
#x <- read.csv("~/workspace/mcmc_growth/data/ME_2b.csv", as.is=T)
#Comment first line to exclude human interaction
#Comment second line to include human interaction
r1 <- x[["carb"]]
r2 <- x[["py"]]
x <- x[-c(nrow(x)),]
r1 <- r1[-c(1)]
r2 <- r2[-c(1)]
x["post_py"] <- r2
x["growth"] <- (x["carb"]-r1)/(x["py"]-x["post_py"])
x <- x[x[,"py"] %/% 10000 == x[,"post_py"] %/% 10000,]
x <- x[, names(x) %in% grep("(growth)|(py)|(post_py)|(lat)|(lon)|(carb)|(iv[0123456789.]+)", colnames(x), value=T)]
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