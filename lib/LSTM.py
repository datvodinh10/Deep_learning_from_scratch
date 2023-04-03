import numpy as np

def sigmoid(x):
    return 1 / (1 + np.e**x)

def forward(X,C_t,h_t,W_f,W_i,W_o,W_C,b_f,b_i,b_o,b_C):
    f_t = sigmoid(np.concatenate([h_t.T,X.T]).T.dot(W_f) + b_f)
    i_t = sigmoid(np.concatenate([h_t.T,X.T]).T.dot(W_i) + b_i)
    C_candidate = np.tanh(np.concatenate([h_t.T,X.T]).T.dot(W_C) + b_C)
    C_new = np.multiply(f_t,C_t) + np.multiply(i_t,C_candidate)
    o_t = sigmoid(np.concatenate([h_t.T,X.T]).T.dot(W_o)+b_o)
    h_new = np.multiply(o_t,np.tanh(C_new))
    return C_new,h_new,f_t,i_t,o_t,C_candidate

def backward(X,y,C_new,h_new,f_t,i_t,o_t,C_candidate,C_t,h_t,W_f,W_i,W_o,W_C,b_f,b_i,b_o,b_C,lr):
    # Calculate gradient
    dL_dh = h_new - y
    dL_do = np.multiply(dL_dh,np.tanh(C_new))
    dL_dC = np.multiply(dL_dh,np.multiply(o_t,1-np.tanh(C_new)**2))
    dL_df = np.multiply(dL_dC,C_t)
    dL_di = np.multiply(dL_dC,C_candidate) 
    dL_dCc = np.multiply(dL_dC,i_t)

    dL_dWo = np.concatenate([h_t.T,X.T]).dot(np.multiply(dL_do,np.multiply(o_t,1-o_t)))
    dL_dWi = np.concatenate([h_t.T,X.T]).dot(np.multiply(dL_di,np.multiply(i_t,1-i_t)))
    dL_dWf = np.concatenate([h_t.T,X.T]).dot(np.multiply(dL_df,np.multiply(f_t,1-f_t)))
    dL_dWc = np.concatenate([h_t.T,X.T]).dot(np.multiply(dL_dCc,np.multiply(C_candidate,1-C_candidate)))

    dL_dbo = np.mean(np.multiply(dL_do,np.multiply(o_t,1-o_t)),axis=1)
    dL_dbi = np.mean(np.multiply(dL_di,np.multiply(i_t,1-i_t)),axis=1)
    dL_dbf = np.mean(np.multiply(dL_df,np.multiply(f_t,1-f_t)),axis=1)
    dL_dbc = np.mean(np.multiply(dL_dCc,np.multiply(C_candidate,1-C_candidate)),axis=1)

    #Update weights and biases
    W_f = W_f - lr * dL_dWf
    W_i = W_i - lr * dL_dWi
    W_o = W_o - lr * dL_dWo
    W_C = W_C - lr * dL_dWc

    b_f = b_f - lr * dL_dbf
    b_i = b_i - lr * dL_dbi
    b_o = b_o - lr * dL_dbo
    b_C = b_C - lr * dL_dbc
    
    return W_f,W_i,W_o,W_C,b_f,b_i,b_o,b_C