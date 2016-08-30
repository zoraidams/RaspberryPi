import numpy
import cv2

# ninputs numbers of inputs
noutputs = 3 # or 4 depends if it's movement o motor
nhidden = 1
# inputs
# targets

# layers
nnet = cv2.ANN_MLP(layers)

# Some parameters for learning. Step size is the gradient step size for backpropagation
step_size = 0.01

# Max steps of training
nsteps = 10000

# Error threshold for halting training
max_err = 0.0001

# When to stop: whichever comes first, count or error
condition = cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS

# Tuple of termination criteria: first condition, then # steps, then
# error tolerance second and third things are ignored if not implied
# by condition
criteria = (condition, nsteps, max_err)

# params is a dictionary with relevant things for NNet training.
params = dict( term_crit = criteria, 
               train_method = cv2.ANN_MLP_TRAIN_PARAMS_BACKPROP, 
               bp_dw_scale = step_size, 
               bp_moment_scale = momentum )

# Train our network
num_iter = nnet.train(inputs, targets,
                      None, params=params)

# Create a matrix of predictions
predictions = numpy.empty_like(targets)

# See how the network did.
nnet.predict(inputs, predictions)

# Compute sum of squared errors
sse = numpy.sum( (targets - predictions)**2 )

# Compute # correct
true_labels = numpy.argmax( targets, axis=0 )
pred_labels = numpy.argmax( predictions, axis=0 )
num_correct = numpy.sum( true_labels == pred_labels )

print 'ran for %d iterations' % num_iter
print 'inputs:'
print inputs
print 'targets:'
print targets
print 'predictions:'
print predictions
print 'sum sq. err:', sse
print 'accuracy:', float(num_correct) / len(true_labels)
