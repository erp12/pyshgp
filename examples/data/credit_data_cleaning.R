library(dplyr)
library(ROCR)
library(glmnet)


credit_df <- read.csv("credit_approval.csv", stringsAsFactors = T)

smp_size <- floor(0.75 * nrow(credit_df))
train_ind <- sample(seq_len(nrow(credit_df)), size = smp_size)

train <- credit_df[train_ind, ]
test <- credit_df[-train_ind, ]

fit <- glm(V16~., train, family=binomial())

p <- predict(fit, newdata = test, type = "response")
pred <- prediction(p, test$V16)
perf <- performance(pred,"tpr","fpr")


par(mar=c(5,5,2,2),xaxs = "i",yaxs = "i",cex.axis=1.3,cex.lab=1.4)
plot(perf,col="black",lty=3, lwd=3)
auc <- performance(pred,"auc")
auc <- unlist(slot(auc, "y.values"))
minauc<-min(round(auc, digits = 2))
maxauc<-max(round(auc, digits = 2))
minauct <- paste(c("min(AUC)  = "),minauc,sep="")
maxauct <- paste(c("max(AUC) = "),maxauc,sep="")
legend(0.3,0.6,c(minauct,maxauct,"\n"),border="white",cex=1.7,box.col = "white")
