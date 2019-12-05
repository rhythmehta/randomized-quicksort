#!/usr/bin/env python
# coding: utf-8

# ## Part A. Median-of-3 partitioning quicksort 
# 
# ## Question 1.
# 
# Read through the following Python code. What does each function (i.e., median, qsort, randomized_qsort, test_qsort) do? Comment in details each function. 
# 

# In[2]:


import timeit
import random

eps = 1e-16
N = 10000
locations = [0.0, 0.5, 1.0 - eps]

#find median value in ascending order of given 3 variables
def median(x1, x2, x3):
    if (x1 < x2 < x3) or (x3 < x2 < x1): #if x2 is middle?
        return x2
    elif (x1 < x3 < x2) or (x2 < x3 < x1): #if x3 is middle?
        return x3
    else:
        return x1 #else x1

#sort an array using quicksor
def qsort(lst):
    indices = [(0, len(lst))] #stores the indices of the first and last element of the list

    while indices:
        (frm, to) = indices.pop()
        if frm == to:
            continue

        # Find the partition:
        N = to - frm
        inds = [frm + int(N * n) for n in locations]
        values = [lst[ind] for ind in inds]
        partition = median(*values)

        # Split into lists:
        lower = [a for a in lst[frm:to] if a < partition]
        upper = [a for a in lst[frm:to] if a > partition]
        counts = sum([1 for a in lst[frm:to] if a == partition])

        ind1 = frm + len(lower)
        ind2 = ind1 + counts

        # Push back into correct place:
        lst[frm:ind1] = lower
        lst[ind1:ind2] = [partition] * counts
        lst[ind2:to] = upper

        # Enqueue other locations
        indices.append((frm, ind1))
        indices.append((ind2, to))
    return lst

def randomized_quicksort():
    lst = [i for i in range(N)] #create a uniform list of ascending order list (eg. 1,2,3,4,5....)
    random.shuffle(lst) #randomly shuffle it
    return qsort(lst) #sort it using qsort

def test_quicksort():
    lst = randomized_quicksort() #obtain sorted list from function above
    assert (lst == [i for i in range(N)]) #the sorted list should be uniform ascending order of counting as created initially


# Is our algorithm correct
test_quicksort()

# How fast is our algorithm
print(timeit.timeit(randomized_quicksort, number=1))


# ## Question 2.
# 
# What are the main differences between the `randomized_quicksort` in the code and $RANDOMIZED-QUICKSORT$ in Cormen et al., besides that the partition of `randomized_quicksort` uses a median of 3 as a pivot?

# Cormen uses recursive calls to the funct randmized-quicksort where he uses a base case function to check before calling in the recursion part. While in the code there is usage of loop than recursion. Also, in the code we shuffle the input which Cormen takes the input as in the given order.

# ## Question 3.
# What is the time complexity of this `randomized_qsort`? Time the algorithm on lists of various lengths, each list being a list of the first $n$ consecutive positive integers. Produce a graph with list lengths on the x axis and running time on the y axis. As always, don’t forget to time the algorithm several times for each list’s length and then average the results. 

# In[5]:


import time
from matplotlib import pyplot as plt

def randomized_quicksort(lst):
    random.shuffle(lst)
    return qsort(lst)

timeset = [] #stores the time for each algorithm
for j in range(1,16):
    value = []
    for k in range(1,10):
        list_k = [i for i in range(100*j)] #creates a list
        t_start_1 = time.time() #calcs time
        randomized_quicksort(list_k)
        value.append(time.time()-t_start_1)
    timeset.append(sum(value)/10)

#plots each graph
plt.plot([i for i in range(1,16)],timeset, label='QuickSort')
plt.xlabel("Input Size in Hundreds")
plt.ylabel("Time in Seconds")
plt.legend()
plt.show()


# ## Question 4.
# 
# ### Question 4a.
# 
# Change the `qsort()` function in a way that you **don’t** separate the items that are equal to the partition. 
# 

# In[6]:


def qsort(lst):
    indices = [(0, len(lst))] #first and last element index

    while indices: #as long as array inn't empty
        # Get the last start-end indice
        (frm, to) = indices.pop()
        # check if the length of subarray has 2 or less elements
        if abs(frm-to) <=2:
            # Sort the elments
            a = lst[frm]
            b = lst[to-1]
            lst[frm] = min(a,b)
            lst[to-1] = max(a,b)
            continue

        # Find the partition:
        N = to - frm # Length of subarray
        inds = [frm + int(N * n) for n in locations] # indices we want to check for median
        values = [lst[ind] for ind in inds] # Values corresponding to the indices we want to check for median
        # Find pivot, the value that is in the middle (start, end, or middle of subarray)
        partition = median(*values)

        # Split into lists:
        lower = [a for a in lst[frm:to] if a < partition] #Array of values less than pivot
        upper = [a for a in lst[frm:to] if a >= partition] #Array of values greater than pivot

        # The index seperating values lower than pivot and pivot
        ind1 = frm + len(lower) 


        # Push back into correct place:
        lst[frm:ind1] = lower # Replace all begining values in subarray with values less than pivot
        lst[ind1:to] = upper # Replace all end values in subarray with values greater than pivot

        # Enqueue other locations
        indices.append((frm, ind1)) # append the subarray indices for values lower than pivot
        indices.append((ind1, to))# append the subarray indices for values greater than pivot
    return lst


# In[7]:


assert(qsort([4,2,1])==[1,2,4])
assert(qsort([0])==[0])


# ### Question 4b.
# 
# Now time the algorithm on the same inputs you have used in question 3, adding one more line in the previous graph you have produced. 

# In[12]:


def qsort2(lst):
    
    indices = [(0, len(lst))] #first and last element index

    while indices: #while th array is not empty
        (frm, to) = indices.pop() # Get the last start-end indice

        if frm == to:
            continue

        #find partition:
        N = to - frm #length of sub
        inds = [frm + int(N * n) for n in locations] #elements to get median from
        values = [lst[ind] for ind in inds] #Gets values of given indices
        partition = median(*values) #finds the median

        #splitting into lists:
        lower = [a for a in lst[frm:to] if a < partition]  #element smaller goes into lower partition
        upper = [a for a in lst[frm:to] if a > partition]  #element bigger goes into upper partition
        
        counts = sum([1 for a in lst[frm:to] if a == partition]) #summmation of elements with same vale as partition

        ind1 = frm + len(lower) #last index of the sub array
        ind2 = ind1 + counts

        #pushing back into correct place:
        lst[frm:ind1] = lower  #swapping with existing list
        lst[ind2:to] = upper

        #queueing other locations
        indices.append((frm, ind1))
        indices.append((ind2, to))

def randomized_quicksort(lst):
    random.shuffle(lst)
    return qsort(lst)

def randomized_quicksort2(lst):
    random.shuffle(lst)
    return qsort2(lst)

#stores the time for each algorithm
times1, times2 = [], []

for j in range(1,16): #iterating with input sizes
    value = []
    for k in range(1,10):
        list_k = [i for i in range(100*j)] #creates a list
        t_startq = time.time() #calculating time for quick sort
        randomized_quicksort(list_k)
        value.append(time.time()-t_startq)
    times1.append(sum(value)/10)
    
for j in range(1,16):
    value = []
    for k in range(1,10):
        #creates a list
        list_k = [i for i in range(100*j)]
        #measures time quick sort
        t_start2 = time.time()
        randomized_quicksort2(list_k)
        value.append(time.time()-t_start2)
    times2.append(sum(value)/10)


#plots each graph
plt.plot([i for i in range(1,16)],times1, label='Quick Sort W/O Parititon')
plt.plot([i for i in range(1,16)],times2, label='Quick Sort Original')
plt.xlabel("Input Size in Hundreds")
plt.ylabel("Time in Seconds")
plt.legend()
plt.show()


# ## Question 5.
# 
# ### Question 5a.
# 
# Remove the median-of-3 partitioning, and just use the first element in the array. 

# In[13]:


def qsort(lst): 
    indices = [(0, len(lst))]

    while indices:
        (frm, to) = indices.pop()
        if frm == to:
            continue

        # Find the partition:
        N = to - frm
        inds = [frm + int(N * n) for n in locations]
        values = [lst[ind] for ind in inds]
        partition = lst[0]
        

        # Split into lists:
        lower = [a for a in lst[frm:to] if a < partition]
        upper = [a for a in lst[frm:to] if a > partition]
        counts = sum([1 for a in lst[frm:to] if a == partition])

        ind1 = frm + len(lower)
        ind2 = ind1 + counts

        # Push back into correct place:
        lst[frm:ind1] = lower
        lst[ind1:ind2] = [partition] * counts
        lst[ind2:to] = upper

        # Enqueue other locations
        indices.append((frm, ind1))
        indices.append((ind2, to))
    return lst
    raise NotImplementedError()


# In[14]:


assert(qsort([4,2,1])==[1,2,4])
assert(qsort([0])==[0])

