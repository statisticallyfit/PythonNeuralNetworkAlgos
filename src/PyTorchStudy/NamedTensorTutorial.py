# %% [markdown]
# #### Conda Environment: pymatrix_env 
#
# #### Tutorial Sources:
# * [(experimental) Named Tensors Introduction)](https://pytorch.org/tutorials/intermediate/named_tensor_tutorial.html#annotations:VOh11nKBEeqlHi8b3rPBxg)
# * [Named Tensors (API doc)](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_to)
#
# #### API Documentation Sources:
# * [Named Tensor Operator Coverage](https://pytorch.org/docs/stable/name_inference.html)
# * [PyTorch Tensors (API Doc)](https://pytorch.org/docs/stable/tensors.html)
#
#
# # Tutorial: Named Tensors and Named Inference in PyTorch
# ### Definition: Named Tensor
# Named Tensors aim to make tensors easier to use by allowing users to associate explicit names with tensor dimensions. In most cases, operations that take dimension parameters will accept dimension names, avoiding the need to track dimensions by position. In addition, named tensors use names to automatically check that APIs are being used correctly at runtime, providing extra safety. Names can also be used to rearrange dimensions, for example, to support **“broadcasting by name” rather than “broadcasting by position”.**
#
# ### Name Inference Rules
# 1. [Keeps Input Names](https://pytorch.org/docs/stable/name_inference.html#keeps-input-names)
# 2. [Removes Dimensions](https://pytorch.org/docs/stable/name_inference.html#removes-dimensions)
# 3. [Unifies Names from Inputs](https://pytorch.org/docs/stable/name_inference.html#unifies-names-from-inputs)
# 4. [Permutes Dimensions](https://pytorch.org/docs/stable/name_inference.html#permutes-dimensions)
# 5. [Contracts away Dims](https://pytorch.org/docs/stable/name_inference.html#contracts-away-dims)
# 6. [Factory Functions Take Names](https://pytorch.org/docs/stable/name_inference.html#factory-functions)
# 7. [Out Function and In-Place Variant Rules](https://pytorch.org/docs/stable/name_inference.html#out-function-and-in-place-variants)
#
# 
# #### Workaround for Operations Not Supported by Named Tensors:
# As a workaround, drop names via `tensor = tensor.rename(None)` before using any function that does not yet support named tensors.
#
# 
# ### Currently Supported:
# * [named tensors operator coverage](https://pytorch.org/docs/stable/name_inference.html#name-inference-reference-doc)
#
# 
# ## Goal of Tutorial:
# This tutorial is intended as a guide to the functionality that will be included with the 1.3 launch. By the end of it, you will be able to:
#
# 1. Create Tensors with named dimensions, as well as remove or rename those dimensions.
# 2. Understand the basics of how operations propagate dimension names.
# 3. See how naming dimensions enables clearer code in two key areas:
#       * Broadcasting operations
#       * Flattening and unflattening dimensions
# 4. Put these ideas into practice by writing a multi-head attention module using named tensors.
#
# 
# # Basics
# 
# ## Named Dimensions
# PyTorch allows `Tensor`s to have named dimensions; factory functions take a new *names* argument that associates a name with each dimension. This works with most factory functions such as: `tensor, empty, ones, zeros, randn, rand`. Here we construct a `Tensor` with names:
# %% codecell

import torch
import torch.tensor as Tensor


from typing import *

tensor: Tensor = torch.randn(1, 2, 2, 3, names = ('N', 'C', 'H', 'W'))
assert tensor.names == ('N', 'C', 'H', 'W')

tensor
# %% [markdown]
# Unlike in the [original named tensors blogpost](http://nlp.seas.harvard.edu/NamedTensor), named dimensions are ordered: `tensor.names[i]` is the name of the `i`th dimension of `tensor`.
# %% codecell
assert tensor.names[0] == 'N' and \
       tensor.names[1] == 'C' and \
       tensor.names[2] == 'H' and \
       tensor.names[3] == 'W'

# %% [markdown]
# ## Renaming a `Tensor`'s dimensions:
# **Method 1:** Set the `.names` attribute directly, as equal to a list. This changes the name in-place.
# %% codecell
tensor.names: List[str] = ['batch', 'channel', 'width', 'height']

assert tensor.names == ('batch', 'channel', 'width', 'height')

tensor
# %% [markdown]
# **Method 2:** Specify new names, changing the names out-of-place
# %% codecell

tensor: Tensor = tensor.rename(channel = 'C', width = 'W', height = 'H')

assert tensor.names == ('batch', 'C', 'W', 'H')

tensor
# %% [markdown]
# ## Removing Names
# The preferred way to remove names is to call `tensor.rename(None)`
# %% codecell
tensor: Tensor = tensor.rename(None)
assert tensor.names == (None, None, None, None)

tensor
# %% [markdown]
# ## About Unnamed Tensors
# Unnamed tensors (with no named dimensions) still work normally and do not have names in their `repr`.
# %% codecell
unnamedTensor: Tensor = torch.randn(2, 1, 3)
assert unnamedTensor.names == (None, None, None)

unnamedTensor
# %% [markdown]
# Named tensors (or partially named tensors) do not require that all dimensions are named. Some dimensions can be `None`.
# %% codecell
partiallyNamedTensor: Tensor = torch.randn(3,1,1,2, names = ('B', None, None, None))
assert partiallyNamedTensor.names == ('B', None, None, None)

partiallyNamedTensor

# %% [markdown]
# ## Refining Dimensions
# Because named tensors can co-exist with unnamed tensors, we need a nice way to write named tensor-aware code that **works with both named and unnamed tensors.** The function [`tensor.refine_names(*names)`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.refine_names) works to refine dimensions and lift unnamed dims to named dims. Refining a dimension is like a "rename" but also with the following additional constraints:
#
# * A `None` dimension can be refined to have **any** name.
# * A named dimension can **only** be refined to have the same name (so a dimension named "apples" cannot be renamed to "oranges")
# %% codecell
tensor: Tensor = torch.randn(3,1,1,2)
namedTensor: Tensor = tensor.refine_names('N', 'C', 'H', 'W')

# Refine the last two dimensions to `H` and `W`
partiallyNamedTensor: Tensor = tensor.refine_names(..., 'H', 'W')

assert tensor.names == (None, None, None, None)
assert namedTensor.names == ('N', 'C', 'H', 'W')
assert partiallyNamedTensor.names == (None, None, 'H', 'W')

# %% codecell
# Function to catch the errors from the passed function argument
def catchError(func):
    try:
        func() # execute the function passed as argument
        # assert False # TODO what is the point of this? If the function works, this assertion fails, so it messes up the partiallyNamedTensor test below...
    except RuntimeError as err:
        err: str = str(err) # make the error into string form
        if (len(err) > 180): # then shorten the printout
            err = err[0:180] + " ... (truncated)"
        print(f"ERROR!: {err}")

# %% [markdown]
# Seeing how we cannot "rename" dimensions when refining.
# %% codecell
catchError(lambda: namedTensor.refine_names('N', 'C', 'H', 'width'))
# %% [markdown]
# Seeing how we can refine the unnamed dimensions, which is the purpose of the [`refine_names()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.refine_names) function:
# %% codecell
tensorRefinedTwoDims = partiallyNamedTensor.refine_names('batchSize', 'channelSize', ...)

catchError(lambda: tensorRefinedTwoDims)

assert tensorRefinedTwoDims.names == ('batchSize', 'channelSize', 'H', 'W')

tensorRefinedTwoDims

# %% [markdown]
# ## Accessors and Reduction
# One can use dimension names to refer to dimensions instead of the positional dimension. These operations also propagate names.
# * NOTE: Indexing (basic and advanced) has not yet been implemented.
# %% codecell
assert torch.equal( namedTensor.softmax(dim = 'N'), namedTensor.softmax(dim = 0))
assert torch.equal(namedTensor.sum(dim = 'C'), namedTensor.sum(dim = 1))

# Slicing (get one image)
assert torch.equal(namedTensor.select(dim = 0, index = 0), namedTensor.select(dim = 'N', index = 0))


# %% [markdown]
# Another test to show significance of using `select()` versus simple array accessor:
# %%
X = torch.arange(7*8*2*4*5).reshape(2,8,5,7,4)
X.names = ['two', 'eight', 'five', 'seven', 'four']

assert torch.equal( X[:,:,:,3,:], X.select('seven', 3) )
assert torch.equal( X[:,:,:,:,2], X.select('four', 2) )
assert torch.equal( X[0,:,:,:,:], X.select('two', 0) )
assert torch.equal( X[1,:,:,:,:], X.select('two', 1) )
assert torch.equal( X[:,7,:,:,:], X.select('eight', 7) )

assert torch.equal( X[0,:,3,:,:], X.select('two', 0).select('five', 3) )
assert torch.equal( X[0,6,2,1,3], X.select('two', 0).select('eight', 6).select('five', 2).select('seven', 1).select('four', 3) )


# %% [markdown]
# ## Size Accessing
# Can check the size of the entire tensor and even of a single dimension.
# %%
X = torch.arange(7*8*2*4*5).reshape(2,8,5,7,4)
X.names = ['two', 'eight', 'five', 'seven', 'four']

assert X.size() == X.shape == torch.Size([2, 8, 5, 7, 4])

assert X.size('two') == 2
assert X.size('eight') == 8
assert X.size('five') == 5
assert X.size('seven') == 7
assert X.size('four') == 4





# %% [markdown]
# ## Name Inference
# Names are propagated on operations in a two-step process called **name inference:**
#
# 1. **Check names:** an operator may perform automatic checks at runtime that check that certain dimension names must match.
# 2. **Propagate names:** name inference propagates output names to output tensors.
#
#
# ## Rules of Name Inference
#
# ### 1/ Propagation of Names (Keeps input names)
# Most simple operations propagate names. The ultimate goal for named tensors is for all operations to propagate names in a reasonable, intuitive manner.
# %% codecell
assert namedTensor.abs().names == ('N', 'C', 'H', 'W')

assert namedTensor.transpose(0, 1).names == ('C', 'N', 'H', 'W')
# Transposing dims later on:
assert namedTensor.transpose(2, 3).names == ('N', 'C', 'W', 'H')

assert namedTensor.align_to('W', 'N', 'H', 'C').names == ('W', 'N', 'H', 'C')

assert namedTensor.atan().names == ('N', 'C', 'H', 'W')

assert namedTensor.bool().names == ('N', 'C', 'H', 'W')

assert namedTensor.byte().names == ('N', 'C', 'H', 'W')

# namedTensor.cholesky() # not supported

assert namedTensor.conj().names == ('N', 'C', 'H', 'W')

# Chunk result on dim = 0
# TODO: pytorch library needs to update its methods so they do their operations according to NAMED DIMENSIONS, so we don't have to use the dimension numbers. Here would say dim = 'N' or something.
c1, c2 = namedTensor.chunk(chunks = 2, dim = 0)
assert c1.names == ('N', 'C', 'H', 'W')
assert c2.names == ('N', 'C', 'H', 'W')
assert c1.shape == (2, 1, 1, 2)
assert c2.shape == (1, 1, 1, 2)
assert namedTensor.shape == (3, 1, 1, 2)
assert c1.shape[0] + c2.shape[0] == namedTensor.shape[0]

# Another chunk example on a dim, where numChunks > dimSize
t = namedTensor.chunk(chunks = 2, dim = 1)
assert t[0].shape == (3,1,1,2)
assert t[0].names == ('N', 'C', 'H', 'W')

# Checking names of the .data information
assert namedTensor.data.names == ('N', 'C', 'H', 'W')
# namedTensor.det() # det() not supported with named tensors
# namedTensor.argmin(dim = 1) # argmin not supported with named tensors
# namedTensor.diag(diagonal = 0) # not supported
# namedTensor.grad # does nothing

# Check can refer to named dims instead of the numbers
assert torch.equal(namedTensor.mean('N'), namedTensor.mean(dim = 0))
# Checking mean result shape on all dimensions
assert namedTensor.mean().names == ()
assert namedTensor.mean('N').names == ('C', 'H', 'W')
assert namedTensor.mean('C').names == ('N', 'H', 'W')
assert namedTensor.mean('H').names == ('N', 'C', 'W')
assert namedTensor.mean('W').names == ('N', 'C', 'H')

# Checking min() shape on first dimensions, similar to mean()
assert namedTensor.min('N').values.names == ('C', 'H', 'W')

# namedTensor.permute(0,2,1) # permute() not supported with named tensors

assert namedTensor.pow(exponent = 2).names == ('N', 'C', 'H', 'W')

# Check can refer to named dimensions instead of number dims
assert (namedTensor.softmax('C') == namedTensor.softmax(dim = 1)).all()
# Checking softmax shape on all dimensions
# assert namedTensor.softmax(dim = 0).names == ('N', 'C', 'H', 'W')
assert namedTensor.softmax('N').names == ('N', 'C', 'H', 'W')
assert namedTensor.softmax('C').names == ('N', 'C', 'H', 'W')
assert namedTensor.softmax('H').names == ('N', 'C', 'H', 'W')
assert namedTensor.softmax('W').names == ('N', 'C', 'H', 'W')


# Checking what `squeeze()` does on different dimensions to the names:
assert namedTensor.names == ('N', 'C', 'H', 'W')

# Confirm can refer to named dims instead of numbers for squeeze()
assert torch.equal(namedTensor.squeeze('N'), namedTensor.squeeze(0))

# On dims 0, 3 there is no size 1-dim tensor to squeeze out, so shapes stay the same (however names get renamed to None unfortunately, they shouldn't!!)
assert namedTensor.squeeze('N').names == namedTensor.squeeze('W').names == (None, None, None, None)
assert namedTensor.squeeze('N').shape == namedTensor.squeeze('W').shape == namedTensor.shape == (3,1,1,2)

# Now squeezing on either dim = 1 or dim = 2 we get a different shape because on those dims, the tensor of size 1 so the squeeze() method squeezes it out. The names get changed likewise.
assert namedTensor.squeeze('C').names == ('N', 'H', 'W') and namedTensor.squeeze('C').shape == (3,1,2)
assert namedTensor.squeeze('H').names == ('N', 'C', 'W') and namedTensor.squeeze('H').shape == (3,1,2)

# NOTE: squeeze() just removes the 1-dim tensors everywhere
t1: Tensor = torch.arange(2*5*3).reshape(2,3,5)
t1.names = ['A', 'B', 'C']

# No shape or name was changed for t1 because it has no tensors of dim size == 1
assert t1.shape == t1.squeeze().shape == (2,3,5) and t1.names == t1.squeeze().names == ('A', 'B', 'C')
# But namedTensor has ALL its dim-1 tensors removed after calling squeeze()
assert namedTensor.names == ('N', 'C', 'H', 'W') \
       and namedTensor.shape == (3,1,1,2) \
       and namedTensor.squeeze().shape == (3,2) \
       and namedTensor.squeeze().names == ('N', 'W')

# namedTensor.unsqueeze(dim = 0) # unsqueeze NOT supported with named tensors!

# namedTensor.trace() # not supported with named tensors




# %% [markdown]
# ### 2/ Removes Dimensions
#
# A general rule: Wheneover integer dimensions can be passed as indices to ano operator, one can also pass a dimension name instead of that integer index. Same goes for lists of dimension indices that can be replaced for lists of dimension names.
#
# **How the Remove Dimensions Rule is Obeyed:**
#
# * **Check Names:** if `dim` or `dims` is passed in as a list of names, check that those names exist in `self`.
# * **Propagate names:** if the dimensions of the input tensor specified by `dim` or `dims` are not present in the output tensor, then the corresponding names of those dimensions do not appear in `output.names`.
#
#
# Reduction operations like [`sum()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.sum) remove dimensions by reducing over the desired dimensions. Other operations like [`select()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.select) and [`squeeze()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.squeeze) simply remove dimensions by returning the other relevant parts of the tensor.
# %%
X = torch.arange(7*1*2*4*5).reshape(2,1,5,7,4)
X.names = ['two', 'one', 'five', 'seven', 'four']


assert X.squeeze('one').names == ('two', 'five', 'seven', 'four')
assert 'one' not in X.squeeze('one').names

assert X.sum(['five', 'four']).names == ('two', 'one', 'seven')
assert 'five' not in X.sum(['five', 'four']).names and \
    'four' not in X.sum(['five', 'four']).names
assert X.sum(['five', 'four']).shape != X.shape

# %% [markdown]
# Reduction operations with `keepdim=True` don't actually remove dimensions:
# %%
X = torch.arange(7*8*2*4*5).reshape(2,8,5,7,4)
X.names = ['two', 'eight', 'five', 'seven', 'four']

assert X.sum(['eight', 'four'], keepdim=True).names == X.names
# Showing that the shape has tensors of size 1 in place wher ethe summing occurred:
assert X.sum(['eight', 'four'], keepdim=True).shape == torch.Size([2,1,5,7,1])
assert X.sum(['eight', 'four'], keepdim=True).shape != X.shape





# %% [markdown]
# ### 3/ Unifies Names from Inputs
# All binary arithmetic operations follow the rule of "unifying names from inputs".
#
# Operations that instead broadcast will broadcast positionally from the right to preserve compatibility with unnamed tensors.
#
# **How the Unify Names Rule is Obeyed:**
#
# * **Check names:** 
#   1. for names to be unified, the names of the tensors pre-operation must match positionally from the right. For instance: in `tensor + other`, the condition `match(tensor.names[i], other.names[i])` must be true for all `i` in `(-min(tensor.dim(), other.dim()) + 1,   -1]`.
# 
# $\color{red}{\text{TODO: how to test this, below tries are NOT working ...}}$
# %%
# Small example of how names are checked:
X = torch.arange(12*7*8*2*4*5).reshape(12,2,8,5,7,4)
X.names = ['twelve', 'two', 'eight', 'five', 'seven', 'four']

Y = torch.arange(7*8*2*4*5*3*6*1).reshape(3,6,1,2,8,5,7,4)
Y.names = ['three', 'six', 'one', 'two', 'eight', 'five', 'seven', 'four']

getIndicesRange = lambda A, B: list(range(-min(A.dim(), B.dim()) + 1, -1))
rs = getIndicesRange(X, Y)
assert rs == [-5, -4, -3, -2]

# Getting the dimensions that correspond to the indices in the range rs
xrs = tuple([X.names[i] for i in rs] )
yrs = tuple([Y.names[i] for i in rs] )

assert xrs == yrs == ('two', 'eight', 'five', 'seven')

assert xrs != X.names
assert ('twelve', ) + xrs + ('four', ) == X.names

assert yrs != Y.names
assert ('three', 'six', 'one') + yrs + ('four', ) == Y.names




# %%
# The above indices show how to fix X and Y so they can be summed:
#Xs = torch.arange(12*7*8*2*4*5).reshape(12,2,8,5,7,4)
Xs = torch.arange(12*7*8*2*5).reshape(12,2,8,5,7)
Xs.names = ['twelve', 'two', 'eight', 'five', 'seven']

Ys = torch.arange(7*8*2*5*3*6).reshape(3,6,2,8,5,7)
Ys.names = ['three', 'six', 'two', 'eight', 'five', 'seven']

rs = getIndicesRange(Xs, Ys)

# TODO why is the last dimension always missing? What does that mean???
xrs = tuple([Xs.names[i] for i in rs] )
yrs = tuple([Ys.names[i] for i in rs] )

# TODO now I want to find a way to add X and Y because things should be alright / legal by rules 1) and 2) but for some reason it doesn't work: why??
# Xs + Ys
# %% [markdown]
# * **Check names:**
#   2. Also, all named dimensions must be aligned from the right. Durin gmatching, if we match a named dimension `A` with an unnamed dimension `None` then `A` must not appear in the tensor with the unnamed dimension. 
# 
# 
# * **Propagate names:** unify pairs of names from the right from both tensors to produce output names. 
# 
# 
# **Example: Of Dimensions Matching Positionally from the Right:** in the below example, since we matched `None` in `tensor` with `C` in `other`, then `C` should not be present in `tensor`, and since we matched `other`'s `N` against `tensor`'s `None`, then `N` should not be present in `other`. 
# %%
tensor = torch.randn(3, 3, names=('N', None))
other = torch.randn(3, 3, names=(None, 'C'))

rs = getIndicesRange(tensor, other)
assert rs == []

# So it is safe to add them:
assert (tensor + other).names == ('N', 'C')


# %% [markdown]
# **Example 1: How Dimensions do not Match Positionally from the Right:**
# %%
tensor = torch.randn(3, 3, names=('N', 'C'))
other = torch.randn(3, names=('N',))

rs = getIndicesRange(tensor, other)
assert rs == []

catchError(lambda: (tensor + other).names )
#RuntimeError: Error when attempting to broadcast dims ['N', 'C'] and dims ['N']: dim 'C' and dim 'N' are at the same position from the right but do not match.

# %% [markdown]
# **Example 1: Of How Dimensions Aren't Aligned When Matching from the Right:**
# %%
# Dimensions aren't aligned when matching tensor.names[-1] and other.names[-1]:
# tensor: Tensor[N, None]
# other:  Tensor[      N]
tensor = torch.randn(3, 3, names=('N', None))
other = torch.randn(3, names=('N',))

catchError(lambda:  (tensor + other).names )
# RuntimeError: Misaligned dims when attempting to broadcast dims ['N'] and dims ['N', None]: dim 'N' appears in a different position from the right across both lists.

# %% [markdown]
# **Example 2: How Dimensions do not Match Positionally from the Right:**
# 
# * **Check names:** Two names match if and only if they are equal (by string equality) or at least one is `None`.
# %% codecell
x: Tensor = torch.randn(3, names = ('X', ))
y: Tensor = torch.randn(3)
z: Tensor = torch.randn(3, names = ('Z',))

catchError(lambda: x + z)

# %% [markdown]
# **Propagate names:** *unify* the two names by returning the most refined name of the two. With `x + y`, the name `X` is more refined than `None` and addition works while above it does not because `X` and `Z` have different names on the same axis while the names of `X` and `Y` do not conflict.
# %% codecell
assert (x + y).names == ('X',)






# %% [markdown]
# ### 4/ Contracting Away Dims (Name Inference for Matrix Multiplication)
# 
# #### Case 1: Matrix Multiplication ([`torch.mm()`](https://pytorch.org/docs/stable/generated/torch.mm.html#torch.mm))
# 
# The function [`torch.mm(A, B)`](https://pytorch.org/docs/stable/generated/torch.mm.html#torch.mm) performs matrix multiplication of two given matrices `A` and `B`, and so the outer dimension of `A` must equal the inner dimension of `B`: `A.shape[-2] == B.shape[-1]`. The result is a two-dimensional tensor (matrix) which has shape `torch.Size([A.shape[0], B.shape[1])`. 
# 
# * **Key point:** matrix multiplication does NOT check if the contracted dimensions (in this case `D` and `in`) have the same name.
# * **NOTE THE DIFFERENCE:** the function [`torch.mm()`](https://pytorch.org/docs/stable/generated/torch.mm.html#torch.mm) for matrices does NOT broadcast while [`torch.matmul()`](https://pytorch.org/docs/stable/generated/torch.matmul.html#torch.matmul) for higher-order tensors does broadcast. 
# 
# 
# For [`torch.mm(tensor, other)`](https://pytorch.org/docs/stable/generated/torch.mm.html#torch.mm), here are the name inference checks that occur: 
# * **Check names:** None
# * **Propagate names:** resulting tensor names are (`tensor.names[0], other.names[1]`)
# %% codecell
markovStates: Tensor = torch.randn(128, 5, names = ('batch', 'D'))
transitionMatrix: Tensor = torch.randn(5, 7, names = ('in', 'out'))

# Apply one transition
newState: Tensor = markovStates.mm(transitionMatrix)

# Asserting multiplication still allowed on `D` and `in` even though they are not the same name.
assert newState.names == ('batch', 'out')
assert newState.shape == (128, 7)


# %% [markdown]
# #### Case 2: Matrix-Vector Multiplication ([`torch.mv()`](https://pytorch.org/docs/stable/generated/torch.mv.html#torch.mv))
# This function does a matrix-vector product of matrix `input` with vector `vec`, where it must be true that `input.shape[1] == vec.shape[0]`. 
# 
# Any matrix multiplication does a dot product over two dimensions (ignoring any batch dimensions) and collapses the two dimensions it has done dot product over. When two tensors are matrix-multiplied, the contracted dimensions disappear and do not show up in the output tensor. 
# 
# 
# [`torch.mv()`](https://pytorch.org/docs/stable/generated/torch.mv.html#torch.mv)  and [`torch.dot()`](https://pytorch.org/docs/stable/generated/torch.dot.html#torch.dot) work similarly: name inference does not check input names and removes the dimensions that are involved in the dot product. 
# 
# For `torch.mv(input, vec)`, here is how name inference rules are obeyed: 
# * **Check names:** None
# * **Propagate names:** the resulting tensor has name equal to `input.names[0]`. 
# %%
x = torch.randn(4, 3, names = ('N', 'D'))
y = torch.randn(3, names = ('something',))

assert x.mv(y).shape == torch.Size([4])
assert x.mv(y).names == ('N', )



# %% [markdown]
# #### Case 3: Batch Matrix Multiplication ([`torch.matmul()`](https://pytorch.org/docs/stable/generated/torch.matmul.html#torch.matmul))
# In this case, for `torch.matmul(tensor, other)`, we have `tensor.dim() >= 2` and `other.dim() >= 2`. 
# 
# Here is how name inference rules are obeyed: 
# * ** Check names: ** check that the batch dimensions of the inputs are aligned and broadcastable. 
# * **Propagate names:** result names are obtained by unifying the batch dimensions and removing the contracted dimensions: `unify(tensor.names[:-2], other.names[:-2]) + (tensor.names[-2], other.names[-1])`
# %%
# Batch matrix multiply of matrices where the first three dims are batch dims in x and the first two are batch dims in y
x = torch.randn(7,2,1,4,3, names = ('batch_one', 'batch_two', 'batch_three', 'A', 'B'))
y = torch.randn(  1,5,3,2, names = ('batch_two', 'batch_three', 'C', 'D'))

# Showing what names will be UNIFIED: 
assert x.names[:-2] == ('batch_one', 'batch_two', 'batch_three')
assert y.names[:-2] == (             'batch_two', 'batch_three')

# Showing what the new matrix result will take its name from: (note: the non-matrix)
assert x.names[-2] == 'A'
assert y.names[-1] == 'D'


# Calculating the result of the multiplication: 
result = torch.matmul(x, y)


assert result.names == ('batch_one', 'batch_two', 'batch_three', 'A', 'D')
# Showing how the non-matrix dimensions (batch dimensions) were broadcasted: 
assert result.shape == torch.Size([7, 2, 5, 4, 2])







# %% [markdown]
# ## [Broadcasting](https://hyp.is/-9CpUCmCEeuGN98Fny_dTw/pytorch.org/docs/stable/notes/broadcasting.html)
# The rules of broadcasting are described as follows. 
# 
# Two tensors are "broadcastable" if the following rules hold: 
# * Each tensor has at least one dimension
# * When iterating over the dimension sizes, starting at the trailing dimension, 
#   1. the dimension sizes must either be equal, or ..
#   2. one of them is equal `1`, or ..
#   3. one of them does not exist.
# 
# For example: 
# 
# Same shapes are always broadcastable
# %%
x = torch.empty(5, 7, 3)
y = torch.empty(5, 7, 3)
assert (x + y).size() == torch.Size([5,7,3])
# %% [markdown]
# `x` and `y` are NOT broadcastable because `x` does not have at least one dimension:
# %%
x = torch.empty((0),)
y = torch.empty(2, 2)

catchError(lambda: x + y)
# %% [markdown]
# Below, it is clear that `x` and `y` are broadcastable because:
# * 1st trailing dimension: both have size 1
# * 2nd trailing dimension: `y` has size 1
# * 3rd trailing dimension: `x` size == `y` size
# * 4th trailing dimension: `y` dimension doesn't exist
# %%
x = torch.empty(5, 3, 4, 1)
y = torch.empty(   3, 1, 1)

assert (x + y).size() == torch.Size([5, 3, 4, 1])

# %% [markdown]
# ### Broadcasting Rules
# 
# If two tensors `x` and `y` are "broadcastable" the resulting tensor size is calculated as follows: 
# 
# 1. **Step 1:** If the number of dimensions of `x` and `y` are not equal (`x.ndim != y.ndim`), then *prepend* 1 to the dimensions of the tensor with fewer dimensions to make the tensors equal length. 
# 2. **Step 2:** then for each dimension size of `x` and `y`, the resulting dimension size of the broadcasted tensor is the max of the sizes of `x` and `y` along that dimension (`max`($x_{\text{dim}_i}$), $y_{\text{dim}_i}$)
# 
# 
# For example: 
# %%
x = torch.empty(5, 1, 4, 1)
y = torch.empty(   3, 1, 1)

assert (x + y).size() == torch.Size([5, 3, 4, 1])

# %%
x = torch.empty(      1)
y = torch.empty(3, 1, 7)

assert (x + y).size() == torch.Size([3, 1, 7])

# %%
x = torch.empty(5, 2, 4, 1)
y = torch.empty(   3, 1, 1)

catchError(lambda : (x + y).size() )

# %% [markdown]
# More about broadcasting from numpy page: 
# * [https://numpy.org/doc/stable/user/basics.broadcasting.html#module-numpy.doc.broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html#module-numpy.doc.broadcasting)




# %% [markdown]
# ## Broadcasting and Name Inference
# Named tensors do not change broadcasting behavior, they still broadcast by position. But when checking two dimensions if they can be broadcasted, PyTorch also checks that the names of those dimensions match. In other words PyTorch does broadcasting by checking for two things:
#
# 1. Checks if the two dimensions can be broadcasted (structurally)
# 2. Checks the names of those dimensions are equal (else it doesn't broadcast)
#
# This results in named tensors preventing unintended alignment during operations that broadcast.
#
# 
# 
# **Example: Apply a `perBatchScale` to the `tensor`:** Below, without `names` the `perBatchScale` tensor is aligned with the last dimension of `tensor`, which is `W` but an error is thrown since this doesn't match the name of the dimension `N` of the `perBatchScale` tensor. (Later: will talk about explicit broadcasting by names for how to align tensors by name).
# But what we wanted instead was to perform the operation by aligning `perBatchScale` with the batch dimension `N` of `tensor`.
# %% codecell
tensor: Tensor = torch.randn(2,2,2,2, names = ('N', 'C', 'H', 'W'))
perBatchScale: Tensor = torch.rand(2, names = ('N', ))
catchError(lambda : tensor * perBatchScale)




# %% [markdown]
# ## Explicit Broadcasting by Names
# Main complaints about working with multiple dimensions is the need to [`unsqueeze()`](https://pytorch.org/docs/stable/torch.html#torch.unsqueeze) (to introduce / add) dummy dimensions so that operations can occur. For the `perBatchScale` example, to multiply the unnamed versions of the tensors we would [`unsqueeze()`](https://pytorch.org/docs/stable/torch.html#torch.unsqueeze) as follows.
#
# **Old Method: [`unsqueeze()`](https://pytorch.org/docs/stable/torch.html#torch.unsqueeze)**
# %% codecell
tensor_: Tensor = torch.randn(2,2,2,2) # N, C, H, W
perBatchScale_: Tensor = torch.rand(2) # N

assert tensor_.shape == (2,2,2,2)
assert perBatchScale_.view(2,1,1,1).shape == (2,1,1,1)

print(f"perBatchScale = {perBatchScale_}\n\n")
print(f"tensor = {tensor_}")

# %% [markdown]
# * **NOTE:** Recognize as a sidenote that [`view()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.view) and [`expand_as()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.expand_as) are not the same:
# %% codecell
perBatchScale_.view(2,1,1,1)
# %% codecell
perBatchScale_.expand_as(tensor_)
# %% codecell
# Broadcasting so that can multiply along dimension `N`
# NOTE: view is semantically the right choice
correctResult_: Tensor = tensor_ * perBatchScale_.view(2,1,1,1) # N, C, H, W
# NOTE: expand_as is semantically incorrect
incorrectResult_: Tensor = tensor_ * perBatchScale_.expand_as(tensor_)

assert correctResult_.shape == incorrectResult_.shape == (2,2,2,2)
# Even though they have the same shape, they are not the same
assert not torch.allclose(correctResult_, incorrectResult_)

# %% [markdown]
# **New Method: [`align_as()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_as) or [`align_to()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_to)**
#
# We can make the multiplication operations safer (and easily agnostic to the number of dimensions) by using names. The new [`tensor.align_as(other)`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_as) operations permutes the dimensions of `tensor` to match the order specified in `other.names`, adding one-sized dimensions where appropriate (basically doing the work of [`permute()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.permute) and [`view()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.view)).
#
# * $\color{orange}{\text{WARNING:}}$ [`align_to()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_to) and [`align_as()`]((https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_as)) are not necessarily doing the same work as [`view()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.view). In the below example when some dimensions are missing and we need to fill them in with 1-dim tensors, then using [`view()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.view) to fill them in results in the same tensor as using [`align_to()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_to) or [`align_as()`]((https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_as)). But see below in `Manipulation Dimensions` that when permuting (not adding more) dimensions, [`view()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.view) does not give the same result tensor as [`align_to()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_to).
# %% codecell
tensor: Tensor = tensor_.refine_names('N', 'C', 'H', 'W')
perBatchScale: Tensor = perBatchScale_.refine_names('N')

assert tensor.names == ('N', 'C', 'H', 'W')
assert perBatchScale.names == ('N',)

# Check that view()'s effect on the tensor is the same as align_as()
assert torch.equal(perBatchScale.align_as(tensor).rename(None), perBatchScale_.view(2,1,1,1))

# Check that align_as() gives the resulting tensor the entire dimension names of the `tensor` we want to align as.
assert perBatchScale.align_as(tensor).names == ('N', 'C', 'H', 'W')

perBatchScale.align_as(tensor)

# %% [markdown]
# Now do the calculation with [`align_as()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_as) instead of [`view()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.view):
# %% codecell
scaledResult: Tensor = tensor * perBatchScale.align_as(tensor)

# Check scaled result gets the names:
assert scaledResult.names == ('N', 'C', 'H', 'W')
# Check the previous unnamed result is equal to the named one here:
assert torch.equal(scaledResult.rename(None), correctResult_)
# Another way to check:
assert torch.equal(scaledResult, correctResult_.refine_names('N', 'C', 'H', 'W'))


# %% [markdown]
# ## [Explicit Alignment by Names](https://pytorch.org/docs/stable/named_tensor.html#explicit-alignment-by-names)
# Use [`align_as()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_as) or [`align_to()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_to) to align tensor dimensions by name to a specified ordering. Useful for doing broadcasting by names.
# %% codecell
# This function is agnostic to dimension ordering of input, so long as it has a `C` dimension SOMEWHERE
def scaleChannels(input: Tensor, scale: Tensor) -> Tensor:
    scaleNamed: Tensor = scale.refine_names('C')
    return input * scaleNamed.align_as(input)

# %% codecell
# Initializing the variables:
B, H, C, W, D = 5, 4, 3, 2, 7 # C = num channels
scale: Tensor = torch.randn(C, names = ('C',))
scale_: Tensor = scale.rename(None)
imgs: Tensor = torch.rand(B, H, W, C, names = ('B', 'H', 'W', 'C'))
imgs_: Tensor = imgs.rename(None)
moreImgs: Tensor = torch.rand(B, C, H, W, names = ('B', 'C', 'H', 'W'))
moreImgs_: Tensor = moreImgs.rename(None)
videos: Tensor = torch.randn(B, C, H, W, D, names = ('B', 'C', 'H', 'W', 'D'))
videos_: Tensor = videos.rename(None)

assert scale.shape == (C,) and scale.names == ('C',)

# NOTE: when writing view_as result is not same as align_as when the tensors added are not each 1-dim
assert scale.align_as(imgs).names == imgs.names
assert scale.align_as(imgs).shape == (1,1,1,C)
# scale_.view(imgs.shape) # assertion error
# scale_.view_as(imgs).shape == (1,1,1,C) #RuntimeError: shape '[5, 4, 2, 3]' is invalid for input of size 3

assert scale.align_as(moreImgs).shape == (1,C,1,1)
assert scale.align_as(moreImgs).names == moreImgs.names

assert scale.align_as(videos).shape == (1,C,1,1, 1)
assert scale.align_as(videos).names == videos.names


# %% codecell
resImgs: Tensor = scaleChannels(input = imgs, scale = scale)
assert resImgs.shape == (B, H, W, C)
assert resImgs.names == imgs.names

resMore: Tensor = scaleChannels(input = moreImgs, scale = scale)
assert resMore.shape == (B, C, H, W)
assert resMore.names == moreImgs.names

resVideos: Tensor = scaleChannels(input = videos, scale = scale)
assert resVideos.shape == (B, C, H, W, D)
assert resVideos.names == videos.names
# %% [markdown]
# ## Flattening and Unflattening Dimensions by Names
#
# **Old Method: [`view()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.view), [`reshape()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.reshape), [`flatten()`](https://hyp.is/P03oZHQMEeqVWnehE0Axew/pytorch.org/docs/stable/named_tensor.html):**
#
# One common operation is flattening and unflattening dimensions. Right now, users perform this using either [`view()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.view), [`reshape()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.reshape), or [`flatten()`](https://hyp.is/P03oZHQMEeqVWnehE0Axew/pytorch.org/docs/stable/named_tensor.html). Use cases include flattening batch dimensions to send tensors into operators that are forced to take inputs with a certain number of dimensions (for instance `Conv2D` takes 4D input)
# %% codecell

# %% [markdown]
# **New Method 1: [`flatten()`](https://hyp.is/P03oZHQMEeqVWnehE0Axew/pytorch.org/docs/stable/named_tensor.html):**
#
# To make the operations more semantically meaningful  than [`view()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.view) and [`reshape()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.reshape), we must introduce new [`tensor.unflatten(dim, namedshape)`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.unflatten) method and update [`flatten()`](https://hyp.is/P03oZHQMEeqVWnehE0Axew/pytorch.org/docs/stable/named_tensor.html) to work with names: [`tensor.flatten(dims, new_dim)`](https://hyp.is/P03oZHQMEeqVWnehE0Axew/pytorch.org/docs/stable/named_tensor.html)
#
# [`flatten()`](https://hyp.is/P03oZHQMEeqVWnehE0Axew/pytorch.org/docs/stable/named_tensor.html) can only flatten adjacent dimensions but also works on non-contiguous dimensions (in memory).
# %% codecell
tensor: Tensor = torch.arange(2*3*4*1).reshape(1,3,4,2) # N, C, H, W
tensor.names = ('N', 'C', 'H', 'W')

tensor
# %% codecell
# NOTE: the dimensions to be flattened must be consecutive

# Flattening C, H, W into one dimension titled 'features'
flatTensor: Tensor = tensor.flatten(dims = ['C', 'H', 'W'], out_dim = 'features')
assert flatTensor.shape == (1, 24)
assert flatTensor.names == ('N', 'features')


flatTensor2: Tensor = tensor.flatten(dims = ['C', 'H'], out_dim = 'CH')
assert flatTensor2.shape == (1, 12, 2)
assert flatTensor2.names == ('N', 'CH', 'W')

# %% [markdown]
# **New Method 2: [`unflatten()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.unflatten)**
#
# Unflattens the named dimension `dim`, viewing it in the shape specified by `namedshape`.
#
#  One must pass into [`unflatten()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.unflatten) a **named shape**, which is a list of `(dim, size)` tuples, to specify how to unflatten the dim.
# * NOTE: work in progress for pytorch to save the sizes during a [`flatten()`](https://hyp.is/P03oZHQMEeqVWnehE0Axew/pytorch.org/docs/stable/named_tensor.html) for [`unflatten()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.unflatten)
# %% codecell

tensorRemade: Tensor = flatTensor.unflatten(dim='features', namedshape=(('C', 3), ('H', 4), ('W', 2)))
assert torch.equal(tensor, tensorRemade)
assert tensorRemade.names == ('N', 'C', 'H', 'W')

tensorRemade2: Tensor = flatTensor2.unflatten(dim = 'CH', namedshape=(('C', 3), ('H', 4)))
assert torch.equal(tensor, tensorRemade2)
assert tensorRemade2.names == ('N', 'C', 'H', 'W')






# %% [markdown]
# ## [Manipulating Dimensions](https://pytorch.org/docs/stable/named_tensor.html#explicit-alignment-by-names)
#
# # $\color{red}{\text{TODO: compare the effects of } \texttt{align_as, view, unflatten, flatten} \text{ to verify if  they are the same, and then compare the effects of } \texttt{align_to, permute} \text{to see if they are the same} }$
#
# **CASE: Permuting (unnamed) vs. Aligning (named)**
#
# Use [`align_to()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_to) to permute large amounts of dimensions without menionting all of them as in required by [`permute()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.permute).
# %% codecell
A, B, C, D, E, F = 0, 1, 2, 3, 4, 5
tensor_: Tensor = torch.randn(A, B, C, D, E, F)
tensor: Tensor = tensor_.refine_names('A', 'B', 'C', 'D', 'E', 'F')

assert tensor.shape == tensor_.shape == (A, B, C, D, E, F)

# Move F (5th dim) and dimension E (4th dim) to the front while keeping the rest in the same order.
# Old way: (non-named)
assert tensor_.permute(5,4,0,1,2,3).shape == (F, E, A, B, C, D)
# Better way: (named)
assert tensor.align_to('F', 'E', ...).names == ('F', 'E', 'A', 'B', 'C', 'D')
# Sanity check: permute == align results:
assert (tensor_.permute(5,4,0,1,2,3) == tensor.align_to('F', 'E', ...)).all()

# %% [markdown]
# **CASE: Flattening (named) vs. View (unnamed)**
#
# Use [`flatten()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.flatten) and [`unflatten()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.unflatten) to flatten and unflatten dimensions, respectively. These have more semantic meaning than [`view()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.view) and [`reshape()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.reshape).
# %% codecell
N, C, H, W = 32, 3, 128, 128
imgs_: Tensor = torch.randn(N, C, H, W)
imgs: Tensor = imgs_.refine_names('N', 'C', 'H', 'W')

# Flattening C, H, W into one dimension of size C*H*W
flatImgs_: Tensor = imgs_.view(N, -1)
assert flatImgs_.shape == (N, C*H*W)

# Flattening via named dimensions
flatImgs: Tensor = imgs.flatten(dims = ['C', 'H', 'W'], out_dim = 'features')
assert flatImgs.names == ('N', 'features')
assert flatImgs.shape == (N, C*H*W)

# Unflattening  the non-named tensor
unflattenedImgs_: Tensor = flatImgs_.view(N, C, H, W)
assert unflattenedImgs_.shape == imgs.shape

# Unflattening the named tensor
unflattenedImgs: Tensor = flatImgs.unflatten(dim = 'features', namedshape = [('C', 3), ('H', 128), ('W', 128)])
assert unflattenedImgs.shape == imgs.shape
assert unflattenedImgs.names == imgs.names


# %% [markdown]
# **COMPARISON: Permute, Align, Reshape, Transpose, View:**
# %% codecell
s, p, b = 2, 3, 4
x = torch.arange(s*(p+s+1)*b).reshape(s, p+s+1, b).refine_names('S', 'P_plus_S', 'B')
x_ = x.rename(None)

# Sanity basic check:
assert (x_.view(s, p+s+1, b) == x_).all() # sanity check
assert (x.align_as(x) == x).all() # sanity check

x
# %% codecell
### View
tensorView_ = x_.view(p+s+1,s,b)
tensorView_
# %% codecell
### Reshape
tensorReshape_ = x_.reshape(p+s+1, s, b)
tensorReshape_

assert (tensorReshape_ == tensorView_).all()
# %% codecell
### Transpose
tensorTranspose = x.transpose('S', 'P_plus_S')
tensorTranspose
assert not (tensorTranspose == tensorView_).all()
assert not (tensorTranspose == tensorReshape_).all()
# NOTE: confirms that view() and transpose() are not necessarily the same, as in the below link:
# https://pytorch.org/docs/stable/tensors.html#torch.Tensor.view

# %% codecell
### Align To:
tensorAlign = x.align_to('P_plus_S', 'S', ...) # 6,2,4
tensorAlign

assert (tensorAlign == tensorTranspose).all()

# %% codecell
### Permute
tensorPermute_ = x_.permute(1,0,2)
tensorPermute_
assert (tensorPermute_ == tensorAlign).all()

# %% codecell
# Checking relations between align_to(), permute(), and transpose()
assert (tensorAlign == tensorTranspose).all()
assert (tensorAlign == tensorPermute_).all()
assert (tensorPermute_ == tensorTranspose).all()

assert not (tensorAlign == tensorReshape_).all()
# THEREFORE: align_to() == permute() == transpose()


# %% [markdown]
# ## Autograd (Not yet supported)
# Autograd currently ignores names on all tensors and treats them like regular tensors. Gradient computation is correct but we lose the safety that names give us.
# * NOTE: this is a work in progress to handle names in autograd
# %% codecell
x: Tensor = torch.randn(3, names = ('D',))
weight: Tensor = torch.randn(3, names = ('D', ), requires_grad = True)

# Checking that weight gradient is empty
assert str(weight.grad) == 'None'

loss: Tensor = (x - weight).abs()
assert str(loss.grad) == 'None'

# Create a random value for grad loss as argument to loss backward()
gradLoss: Tensor = torch.randn(3)

# %% codecell
loss.backward(gradLoss)

assert str(loss.grad) == 'None' # remains the same

assert str(weight.grad) != 'None' # not empty anymore after backward()
assert weight.grad.shape == (3,) # see, tensor exists in grad
assert weight.grad.names == (None,) # note not yet named, will be named in future

# Record the correct gradient
# NOTE: this is not yet named, will be named in the future
correctGrad: Tensor = weight.grad.clone()
correctGrad

weight.grad.zero_() #set to zero
assert torch.equal(weight.grad, Tensor([0,0,0],dtype=torch.float))

# %% codecell
gradLoss: Tensor = gradLoss.refine_names('C') # set the only dimension as name C
loss: Tensor = (x - weight).abs()
loss.backward(gradLoss)

# Stil unnamed even though the gradLoss was named
assert weight.grad.names == (None, )
assert torch.allclose(weight.grad, correctGrad)


# %% [markdown]
# ## Application Example: [Multi-Head Attention](https://synergo.atlassian.net/wiki/spaces/KnowRes/pages/1446445463/multi-head+attention+mechanism)
# Going through a complete example of implementing a common PyTorch `nn.Module`: [multi-head attention](https://synergo.atlassian.net/wiki/spaces/KnowRes/pages/1446445463/multi-head+attention+mechanism).
#
# Adapting implementation: We adapt the implementation of [multi-head attention](https://synergo.atlassian.net/wiki/spaces/KnowRes/pages/1446445463/multi-head+attention+mechanism) in [this code resource at ParlAI. ](https://github.com/facebookresearch/ParlAI/blob/f7db35cba3f3faf6097b3e6b208442cd564783d9/parlai/agents/transformer/modules.py#L907). Note there are four places labeled (I), (II), (III), and (IV) where using named tensors enables more readable code, and we will dive into each of these after the code block.
#
# * (I) **Refining the input tensor dims: ** the [`query = query.refine_names(..., 'T', 'D')`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.refine_names) serves as enforcable documentation and lifts input dimensions to being named. Checks that the last two dimensions can be refined to `['T', 'D']`, preventing potentially silent or confusing size mismatch errors later down the line.
# * (II) **Manipulating dimensions in `_prepareHead()`: **CLEARLY state sth einput and output dimensions. The input tensor must end with the `T` and `D` dims and the output tensor ends in `H`, `T`, and `D_head` dims. Secondly, it is clear to see what is going on: `_prepareHead()` takes the key, query and value and splits the embedding dimension `D` into multiple heads, finally rearranging embedding dim `D` order to be `[..., 'H', 'T', 'D_head']`. To contrast, the [original implementation](https://github.com/facebookresearch/ParlAI/blob/f7db35cba3f3faf6097b3e6b208442cd564783d9/parlai/agents/transformer/modules.py#L947-L957) uses the non-semantically clear [`view()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.view) and [`transpose()`](https://pytorch.org/docs/stable/torch.html#torch.transpose) operations.
# * (III) **Explicit Broadcasting by names:** To make `mask` broadcast correctly with `dotProd`, we would usually [`unsqueeze()`](https://pytorch.org/docs/stable/torch.html#torch.unsqueeze) dims 1 (for `H`) and `-1` (for `T_key`) in the case of self attention or [`unsqueeze()`](https://pytorch.org/docs/stable/torch.html#torch.unsqueeze) dim `1` in the case of encoder attention (to stand in for the dimension called `H`). But using named tensors, we simply align the `attnMask` to the shape and names of `dotProd` using [`align_as()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_as) so no need to worry about where to [`unsqueeze()`](https://pytorch.org/docs/stable/torch.html#torch.unsqueeze) dims.
# * (IV) **More Dimension manipulation using [`align_to()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_to) and [`flatten()`](https://hyp.is/P03oZHQMEeqVWnehE0Axew/pytorch.org/docs/stable/named_tensor.html):** Here as in (II), the [`align_to()`](https://pytorch.org/docs/stable/named_tensor.html#torch.Tensor.align_to) and [`flatten()`](https://hyp.is/P03oZHQMEeqVWnehE0Axew/pytorch.org/docs/stable/named_tensor.html) are more semantically meaningful than [`view()`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor.view) and [`transpose()`](https://pytorch.org/docs/stable/torch.html#torch.transpose) despite being more verbose.
# %% codecell
import torch.tensor as Tensor
import torch.nn as nn
from torch.nn import Dropout, Linear, LayerNorm
import torch.nn.functional as F
import math


class MultiHeadAttention(nn.Module):

    def __init__(self, numHeads: int, dim: int, dropout = 0):
        super(MultiHeadAttention, self).__init__()
        self.numHeads: int = numHeads
        self.dim: int = dim

        self.attnDropout: Dropout = Dropout(p = dropout)

        # The linear layers through which we pass the word embedding matrix in order to create the query (Q),
        # key (K) and value (V) matrices.
        self.linearQ: Linear = Linear(in_features=dim, out_features=dim)
        self.linearK: Linear = Linear(in_features=dim, out_features=dim)
        self.linearV: Linear = Linear(in_features=dim, out_features=dim)

        # Initializing the weight matrices of these linear layers
        nn.init.xavier_normal_(self.linearQ.weight)
        nn.init.xavier_normal_(self.linearK.weight)
        nn.init.xavier_normal_(self.linearV.weight)

        # The linear layer for the output
        self.linearOut: Linear = Linear(in_features=dim, out_features=dim)

        # Initializing the weight matrix in the linear output layer
        nn.init.xavier_normal_(self.linearOut.weight)




    def forward(self, queryNamed: Tensor, key: Tensor = None, value: Tensor = None,
                mask: Tensor = None) -> Tensor:

        # (I) ------------------------------------------------------------------------------------

        # Renaming the tensor's last two dimensions from None to T and D
        queryNamed: Tensor = queryNamed.refine_names(..., 'T', 'D')
        # queryNamed shape == (B, T, D)
        # NOTE: this marks whether the attention to calculate is of the type 1) self attention, or 2) encoder  attention.
        isSelfAttnType: Tensor = key is None and value is None
        # It is self attention if both key, value are None
        if isSelfAttnType: # then last dim has dim T
            mask: Tensor = mask.refine_names(..., 'T')
            # mask shape == (B, T)
        else: # if attention is of type encoder attention, last dims are T, T_key
            mask: Tensor = mask.refine_names(..., 'T', 'T_key')
            # make shape == (B, T, T_key)


        dim: int = queryNamed.size('D')
        assert dim == self.dim, f"Dimensions do not match: {dim} query vs {self.dim} configured"
        assert mask is not None, "Mask is None, please specify a mask"

        numHeads: int = self.numHeads
        dimPerHead: int = dim // numHeads
        scale: float = math.sqrt(dimPerHead)


        # (II) ------------------------------------------------------------------------------------
        # Manipulating dimensions in prepareHead
        def _prepareHead(tensor: Tensor) -> Tensor:
            tensorNamed: Tensor = tensor.refine_names(..., 'T', 'D')
            return (tensorNamed # shape == (B, T, H, D_head)
                    .unflatten(dim = 'D', namedshape = (('H', numHeads), ('D_head', dimPerHead)))
                    .align_to(..., 'H', 'T', 'D_head')) # shape == (B, H, T, D_head)


        assert value is None # TODO why?

        if isSelfAttnType:
            key = value = queryNamed # this places query's value into both key and value matrices.
            # key shape == value shape == (B, T, D)
        elif value is None:
            # Then key and value are the same, but query differs
            key: Tensor = key.refine_names(..., 'T', 'D')
            # key shape == TODO
            value: Tensor = key
            # value shape == TODO

        #dim: int = key.size('D')


        ### Distinguish between queryLen (T) and keyLen (T_key) dims.

        # if self attention: weightsKey (D (None),D (None)) * key (B, T, D) ---> (B, T, None)
        # if encoder attention: TODO weightsKey (D (None),D (None)) * key () ---> ()
        K: Tensor = _prepareHead(self.linearK(key)).rename(T = 'T_key') # key shape == (B, T, D)
        # K shape == (B, H, T_key, D_head)

        # if self attention: weightsValue (D (None),D (None)) * value (B, T, D) ---> (B, T, None)
        # if encoder attention: TODO # weightsValue (D (None),D (None)) * value (B, T, D) ---> (B, T, None)
        V: Tensor = _prepareHead(self.linearV(value)).rename(T = 'T_key')
        # V shape == (B, H, T_key, D_head)

        # if self attention: weightsQuery (D (None),D (None)) * query (B, T, D) --> (B, T, None)
        # if encoder attention: TODO weightsQuery (D (None),D (None)) * query (B, T, D) --> (B, T, None)
        Q: Tensor = _prepareHead(self.linearQ(queryNamed)) # the T dim stays the same
        # Q shape == (B, H, T, D_head)


        # if self attention: Q matrix (B, H, T, D_head) * K.aligned (B, H, D_head, T_key) ---> (B, H, T, T_key)
        # TODO if encoder attention: Q matrix (B, H, T, D_head) * K.aligned (B, H, D_head, T_key) ---> (B, H, T, T_key)
        dotProd: Tensor = Q.div_(scale).matmul(K.align_to(..., 'D_head', 'T_key'))
        # for self attention: dotProd shape == (B, H, T, T_key)
        # for encoder attention: TODO dotProd shape == (B, H, T, T_key)

        dotProd.refine_names(..., 'H', 'T', 'T_key') # just a check
        # for self attention: dotProd shape == (B, H, T, T_key)
        # for encoder attention: TODO

        # (III) ------------------------------------------------------------------------------------

        # mask: shape == (B, T) for self attention or (B, T, T_key) for encoder attention
        attnMask: Tensor = (mask == 0).align_as(dotProd)
        # attnMask shape == (B, H, T, T_key)

        # Mask dot product according to the attention mask
        dotProd.masked_fill_(mask = attnMask, value = -float(1e20))
        # dotProd shape == (B, H, T, T_key)

        attnWeights: Tensor = self.attnDropout(F.softmax(dotProd / scale, dim = 'T_key'))
        # attnWeights shape == (B, H, T, T_key)

        # (IV) ------------------------------------------------------------------------------------
        # Step: multiplying the softmaxed results with the value matrix V, as in the attention formula. Then reshaping the result.
        attentioned: Tensor = (
            # attnWeights (B, H, T, T_key) * VALUES V (B, H, T_key, D_head) ---> (B, H, T, D_head)
            attnWeights
                .matmul(V).refine_names(..., 'H', 'T', 'D_head') # shape == (B, H, T, D_head)
                .align_to(..., 'T', 'H', 'D_head') # shape == (B, T, H, D_head)
                .flatten(dims = ['H', 'D_head'], out_dim = 'D') # shape == (B, T, D)
        )
        # attentioned shape == (B, T, D)

        # Creating output by passing attentions through linear layer, then making sure of the result's name shape.
        # weightsOut (D (None), D (None)) * attentioned (B, T, D) ---> (B, T, None)
        output: Tensor = self.linearOut(attentioned).refine_names(..., 'T', 'D')
        # output shape == (B, T, D)

        return output # output shape == (B, T, D)

# %% codecell
B, T, D, H = 7, 5, 2*3, 3
query: Tensor = torch.randn(B, T, D, names = ('B', 'T', 'D'))
mask: Tensor = torch.ones(B, T, names = ('B', 'T'))
attn = MultiHeadAttention(numHeads = H, dim = D)
attn
# %% codecell
output = attn(query, mask = mask)
assert output.shape == (B, T, D) and output.names == ('B', 'T', 'D')

# %% codecell
# Showing MultiHeadAttention module is agnostic to the existence of batch dimensions.
query = torch.randn(T, D, names=('T', 'D'))
mask = torch.ones(T, names=('T',))
output = attn(query, mask=mask)
assert output.names == ('T', 'D') and output.shape == (T, D)

# %%