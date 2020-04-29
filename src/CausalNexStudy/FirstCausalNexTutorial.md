```python
import os
from typing import *
```


```python
os.getcwd()
# Setting the baseline:
os.chdir('/development/projects/statisticallyfit/github/learningmathstat/PythonNeuralNetNLP')


curPath: str = os.getcwd() + "/src/CausalNexStudy/"

dataPath: str = curPath + "data/student/"


print("curPath = ", curPath, "\n")
print("dataPath = ", dataPath, "\n")
```

    curPath =  /development/projects/statisticallyfit/github/learningmathstat/PythonNeuralNetNLP/src/CausalNexStudy/ 
    
    dataPath =  /development/projects/statisticallyfit/github/learningmathstat/PythonNeuralNetNLP/src/CausalNexStudy/data/student/ 
    



```python
import sys
# Making files in utils folder visible here: to import my local print functions for nn.Module objects
sys.path.append(os.getcwd() + "/src/utils/")
# For being able to import files within CausalNex folder
sys.path.append(curPath)

sys.path
```




    ['/development/projects/statisticallyfit/github/learningmathstat/PythonNeuralNetNLP/src/CausalNexStudy',
     '/development/bin/python/conda3_ana/envs/pybayesian_env/lib/python37.zip',
     '/development/bin/python/conda3_ana/envs/pybayesian_env/lib/python3.7',
     '/development/bin/python/conda3_ana/envs/pybayesian_env/lib/python3.7/lib-dynload',
     '',
     '/development/bin/python/conda3_ana/envs/pybayesian_env/lib/python3.7/site-packages',
     '/development/bin/python/conda3_ana/envs/pybayesian_env/lib/python3.7/site-packages/IPython/extensions',
     '/home/statisticallyfit/.ipython',
     '/development/projects/statisticallyfit/github/learningmathstat/PythonNeuralNetNLP/src/utils/',
     '/development/projects/statisticallyfit/github/learningmathstat/PythonNeuralNetNLP/src/CausalNexStudy/']



# 1/ Structure Learning
## Structure from Domain Knowledge
We can manually define a structure model by specifying the relationships between different features.
First we must create an empty structure model.


```python
from causalnex.structure import StructureModel

structureModel: StructureModel = StructureModel()
structureModel
```




    <causalnex.structure.structuremodel.StructureModel at 0x7f6d14067fd0>



Next we can specify the relationships between features. Let us assume that experts tell us the following causal relationships are known (where G1 is grade in semester 1):

* `health` $\longrightarrow$ `absences`
* `health` $\longrightarrow$ `G1`


```python
structureModel.add_edges_from([
    ('health', 'absences'),
    ('health', 'G1')
])
```

## Visualizing the Structure


```python
structureModel.edges
```




    OutEdgeView([('health', 'absences'), ('health', 'G1')])




```python
structureModel.nodes
```




    NodeView(('health', 'absences', 'G1'))




```python
from IPython.display import Image
from causalnex.plots import plot_structure, NODE_STYLE, EDGE_STYLE

viz = plot_structure(
    structureModel,
    graph_attributes={"scale": "0.5"},
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK)
filename_first = curPath + "structure_model_first.png"

viz.draw(filename_first)
Image(filename_first)
```

    /development/bin/python/conda3_ana/envs/pybayesian_env/lib/python3.7/site-packages/pygraphviz/agraph.py:1367: RuntimeWarning: Warning: node 'health', graph '%3' size too small for label
    Warning: node 'absences', graph '%3' size too small for label
    Warning: node 'G1', graph '%3' size too small for label
    
      warnings.warn(b"".join(errors).decode(self.encoding), RuntimeWarning)





![png](FirstCausalNexTutorial_files/FirstCausalNexTutorial_10_1.png)



## Learning the Structure
Can use CausalNex to learn structure model from data, when number of variables grows or domain knowledge does not exist. (Algorithm used is the [NOTEARS algorithm](https://arxiv.org/abs/1803.01422)).
* NOTE: not always necessary to train / test split because structure learning should be a joint effort between machine learning and domain experts.

First must pre-process the data so the [NOTEARS algorithm](https://arxiv.org/abs/1803.01422) can be used.

## Preparing the Data for Structure Learning


```python
import pandas as pd
from pandas.core.frame import DataFrame

fileName: str = dataPath + 'student-por.csv'
data: DataFrame = pd.read_csv(fileName, delimiter = ';')

data.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school</th>
      <th>sex</th>
      <th>age</th>
      <th>address</th>
      <th>famsize</th>
      <th>Pstatus</th>
      <th>Medu</th>
      <th>Fedu</th>
      <th>Mjob</th>
      <th>Fjob</th>
      <th>...</th>
      <th>famrel</th>
      <th>freetime</th>
      <th>goout</th>
      <th>Dalc</th>
      <th>Walc</th>
      <th>health</th>
      <th>absences</th>
      <th>G1</th>
      <th>G2</th>
      <th>G3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GP</td>
      <td>F</td>
      <td>18</td>
      <td>U</td>
      <td>GT3</td>
      <td>A</td>
      <td>4</td>
      <td>4</td>
      <td>at_home</td>
      <td>teacher</td>
      <td>...</td>
      <td>4</td>
      <td>3</td>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>4</td>
      <td>0</td>
      <td>11</td>
      <td>11</td>
    </tr>
    <tr>
      <th>1</th>
      <td>GP</td>
      <td>F</td>
      <td>17</td>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>1</td>
      <td>1</td>
      <td>at_home</td>
      <td>other</td>
      <td>...</td>
      <td>5</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>2</td>
      <td>9</td>
      <td>11</td>
      <td>11</td>
    </tr>
    <tr>
      <th>2</th>
      <td>GP</td>
      <td>F</td>
      <td>15</td>
      <td>U</td>
      <td>LE3</td>
      <td>T</td>
      <td>1</td>
      <td>1</td>
      <td>at_home</td>
      <td>other</td>
      <td>...</td>
      <td>4</td>
      <td>3</td>
      <td>2</td>
      <td>2</td>
      <td>3</td>
      <td>3</td>
      <td>6</td>
      <td>12</td>
      <td>13</td>
      <td>12</td>
    </tr>
    <tr>
      <th>3</th>
      <td>GP</td>
      <td>F</td>
      <td>15</td>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>4</td>
      <td>2</td>
      <td>health</td>
      <td>services</td>
      <td>...</td>
      <td>3</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>5</td>
      <td>0</td>
      <td>14</td>
      <td>14</td>
      <td>14</td>
    </tr>
    <tr>
      <th>4</th>
      <td>GP</td>
      <td>F</td>
      <td>16</td>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>3</td>
      <td>3</td>
      <td>other</td>
      <td>other</td>
      <td>...</td>
      <td>4</td>
      <td>3</td>
      <td>2</td>
      <td>1</td>
      <td>2</td>
      <td>5</td>
      <td>0</td>
      <td>11</td>
      <td>13</td>
      <td>13</td>
    </tr>
    <tr>
      <th>5</th>
      <td>GP</td>
      <td>M</td>
      <td>16</td>
      <td>U</td>
      <td>LE3</td>
      <td>T</td>
      <td>4</td>
      <td>3</td>
      <td>services</td>
      <td>other</td>
      <td>...</td>
      <td>5</td>
      <td>4</td>
      <td>2</td>
      <td>1</td>
      <td>2</td>
      <td>5</td>
      <td>6</td>
      <td>12</td>
      <td>12</td>
      <td>13</td>
    </tr>
    <tr>
      <th>6</th>
      <td>GP</td>
      <td>M</td>
      <td>16</td>
      <td>U</td>
      <td>LE3</td>
      <td>T</td>
      <td>2</td>
      <td>2</td>
      <td>other</td>
      <td>other</td>
      <td>...</td>
      <td>4</td>
      <td>4</td>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>0</td>
      <td>13</td>
      <td>12</td>
      <td>13</td>
    </tr>
    <tr>
      <th>7</th>
      <td>GP</td>
      <td>F</td>
      <td>17</td>
      <td>U</td>
      <td>GT3</td>
      <td>A</td>
      <td>4</td>
      <td>4</td>
      <td>other</td>
      <td>teacher</td>
      <td>...</td>
      <td>4</td>
      <td>1</td>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>2</td>
      <td>10</td>
      <td>13</td>
      <td>13</td>
    </tr>
    <tr>
      <th>8</th>
      <td>GP</td>
      <td>M</td>
      <td>15</td>
      <td>U</td>
      <td>LE3</td>
      <td>A</td>
      <td>3</td>
      <td>2</td>
      <td>services</td>
      <td>other</td>
      <td>...</td>
      <td>4</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>15</td>
      <td>16</td>
      <td>17</td>
    </tr>
    <tr>
      <th>9</th>
      <td>GP</td>
      <td>M</td>
      <td>15</td>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>3</td>
      <td>4</td>
      <td>other</td>
      <td>other</td>
      <td>...</td>
      <td>5</td>
      <td>5</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>5</td>
      <td>0</td>
      <td>12</td>
      <td>12</td>
      <td>13</td>
    </tr>
  </tbody>
</table>
<p>10 rows × 33 columns</p>
</div>



Can see the features are numeric and non-numeric. Can drop sensitive features like gender that we do not want to include in our model.


```python
iDropCol: List[int] = ['school','sex','age','Mjob', 'Fjob','reason','guardian']

data = data.drop(columns = iDropCol)
data.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>address</th>
      <th>famsize</th>
      <th>Pstatus</th>
      <th>Medu</th>
      <th>Fedu</th>
      <th>traveltime</th>
      <th>studytime</th>
      <th>failures</th>
      <th>schoolsup</th>
      <th>famsup</th>
      <th>...</th>
      <th>famrel</th>
      <th>freetime</th>
      <th>goout</th>
      <th>Dalc</th>
      <th>Walc</th>
      <th>health</th>
      <th>absences</th>
      <th>G1</th>
      <th>G2</th>
      <th>G3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>U</td>
      <td>GT3</td>
      <td>A</td>
      <td>4</td>
      <td>4</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
      <td>yes</td>
      <td>no</td>
      <td>...</td>
      <td>4</td>
      <td>3</td>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>4</td>
      <td>0</td>
      <td>11</td>
      <td>11</td>
    </tr>
    <tr>
      <th>1</th>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>no</td>
      <td>yes</td>
      <td>...</td>
      <td>5</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>2</td>
      <td>9</td>
      <td>11</td>
      <td>11</td>
    </tr>
    <tr>
      <th>2</th>
      <td>U</td>
      <td>LE3</td>
      <td>T</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>yes</td>
      <td>no</td>
      <td>...</td>
      <td>4</td>
      <td>3</td>
      <td>2</td>
      <td>2</td>
      <td>3</td>
      <td>3</td>
      <td>6</td>
      <td>12</td>
      <td>13</td>
      <td>12</td>
    </tr>
    <tr>
      <th>3</th>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>4</td>
      <td>2</td>
      <td>1</td>
      <td>3</td>
      <td>0</td>
      <td>no</td>
      <td>yes</td>
      <td>...</td>
      <td>3</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>5</td>
      <td>0</td>
      <td>14</td>
      <td>14</td>
      <td>14</td>
    </tr>
    <tr>
      <th>4</th>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>no</td>
      <td>yes</td>
      <td>...</td>
      <td>4</td>
      <td>3</td>
      <td>2</td>
      <td>1</td>
      <td>2</td>
      <td>5</td>
      <td>0</td>
      <td>11</td>
      <td>13</td>
      <td>13</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 26 columns</p>
</div>



Next we want tomake our data numeric since this is what the NOTEARS algorithm expects. We can do this by label-encoding the non-numeric variables (to make them also numeric, like the current numeric variables).


```python
import numpy as np


structData: DataFrame = data.copy()

# This operation below excludes all column variables that are number variables (so keeping only categorical variables)
structData.select_dtypes(exclude=[np.number]).head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>address</th>
      <th>famsize</th>
      <th>Pstatus</th>
      <th>schoolsup</th>
      <th>famsup</th>
      <th>paid</th>
      <th>activities</th>
      <th>nursery</th>
      <th>higher</th>
      <th>internet</th>
      <th>romantic</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>U</td>
      <td>GT3</td>
      <td>A</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
    </tr>
    <tr>
      <th>1</th>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>no</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>no</td>
    </tr>
    <tr>
      <th>2</th>
      <td>U</td>
      <td>LE3</td>
      <td>T</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>yes</td>
      <td>no</td>
    </tr>
    <tr>
      <th>3</th>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>no</td>
      <td>yes</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>yes</td>
      <td>yes</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>4</th>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>no</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Getting the names of the categorical variables (columns)
structData.select_dtypes(exclude=[np.number]).columns
```




    Index(['address', 'famsize', 'Pstatus', 'schoolsup', 'famsup', 'paid',
           'activities', 'nursery', 'higher', 'internet', 'romantic'],
          dtype='object')




```python
namesOfCategoricalVars: List[str] = list(structData.select_dtypes(exclude=[np.number]).columns)
namesOfCategoricalVars
```




    ['address',
     'famsize',
     'Pstatus',
     'schoolsup',
     'famsup',
     'paid',
     'activities',
     'nursery',
     'higher',
     'internet',
     'romantic']




```python
from sklearn.preprocessing import LabelEncoder

labelEncoder: LabelEncoder = LabelEncoder()

# NOTE: structData keeps also the numeric columns, doesn't exclude them! just updates the non-numeric cols.
for varName in namesOfCategoricalVars:
    structData[varName] = labelEncoder.fit_transform(y = structData[varName])
```


```python
structData.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>address</th>
      <th>famsize</th>
      <th>Pstatus</th>
      <th>Medu</th>
      <th>Fedu</th>
      <th>traveltime</th>
      <th>studytime</th>
      <th>failures</th>
      <th>schoolsup</th>
      <th>famsup</th>
      <th>...</th>
      <th>famrel</th>
      <th>freetime</th>
      <th>goout</th>
      <th>Dalc</th>
      <th>Walc</th>
      <th>health</th>
      <th>absences</th>
      <th>G1</th>
      <th>G2</th>
      <th>G3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>4</td>
      <td>4</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>...</td>
      <td>4</td>
      <td>3</td>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>4</td>
      <td>0</td>
      <td>11</td>
      <td>11</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>...</td>
      <td>5</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>2</td>
      <td>9</td>
      <td>11</td>
      <td>11</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>...</td>
      <td>4</td>
      <td>3</td>
      <td>2</td>
      <td>2</td>
      <td>3</td>
      <td>3</td>
      <td>6</td>
      <td>12</td>
      <td>13</td>
      <td>12</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>4</td>
      <td>2</td>
      <td>1</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>...</td>
      <td>3</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>5</td>
      <td>0</td>
      <td>14</td>
      <td>14</td>
      <td>14</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>...</td>
      <td>4</td>
      <td>3</td>
      <td>2</td>
      <td>1</td>
      <td>2</td>
      <td>5</td>
      <td>0</td>
      <td>11</td>
      <td>13</td>
      <td>13</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 26 columns</p>
</div>




```python
# Going to compare the converted numeric values to their previous categorical values:
namesOfCategoricalVars
```




    ['address',
     'famsize',
     'Pstatus',
     'schoolsup',
     'famsup',
     'paid',
     'activities',
     'nursery',
     'higher',
     'internet',
     'romantic']




```python
categData: DataFrame = data.select_dtypes(exclude=[np.number])
```


```python
# The different values of Address variable (R and U)
np.unique(categData['address'])
```




    array(['R', 'U'], dtype=object)




```python
np.unique(categData['famsize'])
```




    array(['GT3', 'LE3'], dtype=object)




```python
np.unique(categData['Pstatus'])
```




    array(['A', 'T'], dtype=object)




```python
np.unique(categData['schoolsup'])
```




    array(['no', 'yes'], dtype=object)




```python
np.unique(categData['famsup'])
```




    array(['no', 'yes'], dtype=object)




```python
np.unique(categData['paid'])
```




    array(['no', 'yes'], dtype=object)




```python
np.unique(categData['activities'])
```




    array(['no', 'yes'], dtype=object)




```python
np.unique(categData['nursery'])
```




    array(['no', 'yes'], dtype=object)




```python
np.unique(categData['higher'])
```




    array(['no', 'yes'], dtype=object)




```python
np.unique(categData['internet'])
```




    array(['no', 'yes'], dtype=object)




```python
np.unique(categData['romantic'])
```




    array(['no', 'yes'], dtype=object)




```python
# A numeric column:
np.unique(data['Medu'])


```




    array([0, 1, 2, 3, 4])




```python
# All the values we convert in structData are binary, so testing how a non-binary one gets converted here:
testMultivals: List[str] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

assert list(labelEncoder.fit_transform(y = testMultivals)) == [0, 1, 2, 3, 4, 5, 6, 7]
```

Now apply the NOTEARS algo to learn the structure:




```python

#from src.utils.Clock import *

def clock(startTime, endTime):
    elapsedTime = endTime - startTime
    elapsedMins = int(elapsedTime / 60)
    elapsedSecs = int(elapsedTime - (elapsedMins * 60))
    return elapsedMins, elapsedSecs
```


```python
from causalnex.structure.notears import from_pandas
import time

startTime: float = time.time()

structureModelLearned = from_pandas(X = structData)

print(f"Time taken = {clock(startTime = startTime, endTime = time.time())}")
```

    Time taken = (6, 1)



```python
# Now visualize it:
viz = plot_structure(
    structureModelLearned,
    graph_attributes={"scale": "0.5"},
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK)
filename_learned = curPath + "structure_model_learnedStructure.png"

viz.draw(filename_learned)
Image(filename_learned)




```

    /development/bin/python/conda3_ana/envs/pybayesian_env/lib/python3.7/site-packages/pygraphviz/agraph.py:1367: RuntimeWarning: Warning: node 'address', graph '%3' size too small for label
    Warning: node 'famsize', graph '%3' size too small for label
    Warning: node 'Pstatus', graph '%3' size too small for label
    Warning: node 'Medu', graph '%3' size too small for label
    Warning: node 'Fedu', graph '%3' size too small for label
    Warning: node 'traveltime', graph '%3' size too small for label
    Warning: node 'studytime', graph '%3' size too small for label
    Warning: node 'failures', graph '%3' size too small for label
    Warning: node 'schoolsup', graph '%3' size too small for label
    Warning: node 'famsup', graph '%3' size too small for label
    Warning: node 'paid', graph '%3' size too small for label
    Warning: node 'activities', graph '%3' size too small for label
    Warning: node 'nursery', graph '%3' size too small for label
    Warning: node 'higher', graph '%3' size too small for label
    Warning: node 'internet', graph '%3' size too small for label
    Warning: node 'romantic', graph '%3' size too small for label
    Warning: node 'famrel', graph '%3' size too small for label
    Warning: node 'freetime', graph '%3' size too small for label
    Warning: node 'goout', graph '%3' size too small for label
    Warning: node 'Dalc', graph '%3' size too small for label
    Warning: node 'Walc', graph '%3' size too small for label
    Warning: node 'health', graph '%3' size too small for label
    Warning: node 'absences', graph '%3' size too small for label
    Warning: node 'G1', graph '%3' size too small for label
    Warning: node 'G2', graph '%3' size too small for label
    Warning: node 'G3', graph '%3' size too small for label
    
      warnings.warn(b"".join(errors).decode(self.encoding), RuntimeWarning)





![png](FirstCausalNexTutorial_files/FirstCausalNexTutorial_39_1.png)



Can apply thresholding here to prune the algorithm's resulting fully connected graph. Thresholding can be applied either by specifying the value for the parameter `w_threshold` in `from_pandas` or we can remove the edges by calling the structure model function `remove_edges_below_threshold`.


```python
structureModelPruned = structureModelLearned.copy()
structureModelPruned.remove_edges_below_threshold(threshold = 0.8)
```


```python
# Now visualize it:
viz = plot_structure(
    structureModelPruned,
    graph_attributes={"scale": "0.5"},
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK)
filename_pruned = curPath + "structure_model_pruned.png"
viz.draw(filename_pruned)
Image(filename_pruned)
```

    /development/bin/python/conda3_ana/envs/pybayesian_env/lib/python3.7/site-packages/pygraphviz/agraph.py:1367: RuntimeWarning: Warning: node 'address', graph '%3' size too small for label
    Warning: node 'absences', graph '%3' size too small for label
    Warning: node 'G1', graph '%3' size too small for label
    Warning: node 'famsize', graph '%3' size too small for label
    Warning: node 'Pstatus', graph '%3' size too small for label
    Warning: node 'famrel', graph '%3' size too small for label
    Warning: node 'Medu', graph '%3' size too small for label
    Warning: node 'Fedu', graph '%3' size too small for label
    Warning: node 'traveltime', graph '%3' size too small for label
    Warning: node 'studytime', graph '%3' size too small for label
    Warning: node 'failures', graph '%3' size too small for label
    Warning: node 'schoolsup', graph '%3' size too small for label
    Warning: node 'famsup', graph '%3' size too small for label
    Warning: node 'paid', graph '%3' size too small for label
    Warning: node 'activities', graph '%3' size too small for label
    Warning: node 'nursery', graph '%3' size too small for label
    Warning: node 'higher', graph '%3' size too small for label
    Warning: node 'internet', graph '%3' size too small for label
    Warning: node 'romantic', graph '%3' size too small for label
    Warning: node 'freetime', graph '%3' size too small for label
    Warning: node 'goout', graph '%3' size too small for label
    Warning: node 'Dalc', graph '%3' size too small for label
    Warning: node 'Walc', graph '%3' size too small for label
    Warning: node 'health', graph '%3' size too small for label
    Warning: node 'G2', graph '%3' size too small for label
    Warning: node 'G3', graph '%3' size too small for label
    
      warnings.warn(b"".join(errors).decode(self.encoding), RuntimeWarning)
    /development/bin/python/conda3_ana/envs/pybayesian_env/lib/python3.7/site-packages/pygraphviz/agraph.py:1367: RuntimeWarning: Warning: node 'address', graph '%3' size too small for label
    Warning: node 'absences', graph '%3' size too small for label
    Warning: node 'G1', graph '%3' size too small for label
    Warning: node 'G2', graph '%3' size too small for label
    Warning: node 'G3', graph '%3' size too small for label
    Warning: node 'famsize', graph '%3' size too small for label
    Warning: node 'Pstatus', graph '%3' size too small for label
    Warning: node 'famrel', graph '%3' size too small for label
    Warning: node 'Medu', graph '%3' size too small for label
    Warning: node 'Fedu', graph '%3' size too small for label
    Warning: node 'traveltime', graph '%3' size too small for label
    Warning: node 'studytime', graph '%3' size too small for label
    Warning: node 'failures', graph '%3' size too small for label
    Warning: node 'schoolsup', graph '%3' size too small for label
    Warning: node 'famsup', graph '%3' size too small for label
    Warning: node 'paid', graph '%3' size too small for label
    Warning: node 'activities', graph '%3' size too small for label
    Warning: node 'nursery', graph '%3' size too small for label
    Warning: node 'higher', graph '%3' size too small for label
    Warning: node 'internet', graph '%3' size too small for label
    Warning: node 'romantic', graph '%3' size too small for label
    Warning: node 'freetime', graph '%3' size too small for label
    Warning: node 'goout', graph '%3' size too small for label
    Warning: node 'Dalc', graph '%3' size too small for label
    Warning: node 'Walc', graph '%3' size too small for label
    Warning: node 'health', graph '%3' size too small for label
    
      warnings.warn(b"".join(errors).decode(self.encoding), RuntimeWarning)





![png](FirstCausalNexTutorial_files/FirstCausalNexTutorial_42_1.png)



Comparing the freshly learned model with the pruned model:


```python
structureModelLearned.adj
```




    AdjacencyView({'address': {'famsize': {'origin': 'learned', 'weight': 0.07172400411745194}, 'Pstatus': {'origin': 'learned', 'weight': 0.027500652131841753}, 'Medu': {'origin': 'learned', 'weight': 0.4329609981782503}, 'Fedu': {'origin': 'learned', 'weight': 0.10940724573937048}, 'traveltime': {'origin': 'learned', 'weight': -0.3080468648891065}, 'studytime': {'origin': 'learned', 'weight': 0.22858517407180592}, 'failures': {'origin': 'learned', 'weight': 0.06633709792506814}, 'schoolsup': {'origin': 'learned', 'weight': 2.265558640319601e-06}, 'famsup': {'origin': 'learned', 'weight': 4.164128335492464e-06}, 'paid': {'origin': 'learned', 'weight': 2.6188325902813357e-06}, 'activities': {'origin': 'learned', 'weight': 8.921883360997223e-06}, 'nursery': {'origin': 'learned', 'weight': 1.0431757754516237e-06}, 'higher': {'origin': 'learned', 'weight': 0.2175470691398659}, 'internet': {'origin': 'learned', 'weight': 4.631899217412905e-07}, 'romantic': {'origin': 'learned', 'weight': 2.1163994047249527e-05}, 'famrel': {'origin': 'learned', 'weight': 0.2713375883408355}, 'freetime': {'origin': 'learned', 'weight': 0.11768720419459214}, 'goout': {'origin': 'learned', 'weight': 0.16392393831724242}, 'Dalc': {'origin': 'learned', 'weight': 0.11663243893798651}, 'Walc': {'origin': 'learned', 'weight': 0.16559963300289912}, 'health': {'origin': 'learned', 'weight': 0.20294893185551394}, 'absences': {'origin': 'learned', 'weight': 1.0400949529066366}, 'G1': {'origin': 'learned', 'weight': 1.006295091882122}, 'G2': {'origin': 'learned', 'weight': 0.15007496882413057}, 'G3': {'origin': 'learned', 'weight': 0.223096391377955}}, 'famsize': {'address': {'origin': 'learned', 'weight': 2.57364988344861e-06}, 'Pstatus': {'origin': 'learned', 'weight': -5.39386360384519e-07}, 'Medu': {'origin': 'learned', 'weight': -0.0016220902698672792}, 'Fedu': {'origin': 'learned', 'weight': -0.024651044459558742}, 'traveltime': {'origin': 'learned', 'weight': 0.25181986913147913}, 'studytime': {'origin': 'learned', 'weight': 0.07404468489673609}, 'failures': {'origin': 'learned', 'weight': -0.00011631802985936184}, 'schoolsup': {'origin': 'learned', 'weight': 7.582265421368856e-07}, 'famsup': {'origin': 'learned', 'weight': 8.083571741711851e-06}, 'paid': {'origin': 'learned', 'weight': 5.982031984826393e-07}, 'activities': {'origin': 'learned', 'weight': 1.1369901568939202e-05}, 'nursery': {'origin': 'learned', 'weight': 1.3604190036451818e-06}, 'higher': {'origin': 'learned', 'weight': 3.4544721166046257e-07}, 'internet': {'origin': 'learned', 'weight': 1.985563914894138e-06}, 'romantic': {'origin': 'learned', 'weight': 2.9757663553056567e-05}, 'famrel': {'origin': 'learned', 'weight': 0.23128615865426996}, 'freetime': {'origin': 'learned', 'weight': 0.023554521782170514}, 'goout': {'origin': 'learned', 'weight': -0.089444259197238}, 'Dalc': {'origin': 'learned', 'weight': 0.272822548840043}, 'Walc': {'origin': 'learned', 'weight': 0.21200668687560334}, 'health': {'origin': 'learned', 'weight': 0.07702410821801904}, 'absences': {'origin': 'learned', 'weight': -0.1488343695903593}, 'G1': {'origin': 'learned', 'weight': 0.5361350969644317}, 'G2': {'origin': 'learned', 'weight': 0.032840481295506055}, 'G3': {'origin': 'learned', 'weight': 0.03510912683115285}}, 'Pstatus': {'address': {'origin': 'learned', 'weight': 4.034341252476512e-06}, 'famsize': {'origin': 'learned', 'weight': -0.17295794814902476}, 'Medu': {'origin': 'learned', 'weight': 0.1384140623478854}, 'Fedu': {'origin': 'learned', 'weight': 0.14975863405325376}, 'traveltime': {'origin': 'learned', 'weight': 0.714734047306784}, 'studytime': {'origin': 'learned', 'weight': 0.29230404950042704}, 'failures': {'origin': 'learned', 'weight': 0.27245193062493933}, 'schoolsup': {'origin': 'learned', 'weight': 6.161919403615951e-06}, 'famsup': {'origin': 'learned', 'weight': 8.134891913687072e-06}, 'paid': {'origin': 'learned', 'weight': 7.550818083392646e-06}, 'activities': {'origin': 'learned', 'weight': 9.167216054392334e-06}, 'nursery': {'origin': 'learned', 'weight': 2.2293990599005983e-06}, 'higher': {'origin': 'learned', 'weight': 2.567768712230681e-07}, 'internet': {'origin': 'learned', 'weight': 1.2495739741261968e-06}, 'romantic': {'origin': 'learned', 'weight': 3.606586324263287e-05}, 'famrel': {'origin': 'learned', 'weight': 0.8402877660070628}, 'freetime': {'origin': 'learned', 'weight': 0.3076339104564842}, 'goout': {'origin': 'learned', 'weight': -0.006601878891263519}, 'Dalc': {'origin': 'learned', 'weight': 0.451312158903729}, 'Walc': {'origin': 'learned', 'weight': 0.4005429332616751}, 'health': {'origin': 'learned', 'weight': 0.2873495054103081}, 'absences': {'origin': 'learned', 'weight': -1.0538754156321408}, 'G1': {'origin': 'learned', 'weight': 1.261362346111696}, 'G2': {'origin': 'learned', 'weight': 0.18088756091335226}, 'G3': {'origin': 'learned', 'weight': -0.08860028396266117}}, 'Medu': {'address': {'origin': 'learned', 'weight': 5.282843496249485e-07}, 'famsize': {'origin': 'learned', 'weight': -8.376171747006237e-05}, 'Pstatus': {'origin': 'learned', 'weight': 7.664857242148944e-07}, 'Fedu': {'origin': 'learned', 'weight': 0.6253625161000721}, 'traveltime': {'origin': 'learned', 'weight': -1.4976973044455327e-05}, 'studytime': {'origin': 'learned', 'weight': 0.07663461056844137}, 'failures': {'origin': 'learned', 'weight': -8.47848862991425e-06}, 'schoolsup': {'origin': 'learned', 'weight': 1.4871605630041722e-06}, 'famsup': {'origin': 'learned', 'weight': 2.768426487726607e-06}, 'paid': {'origin': 'learned', 'weight': 4.306941634359122e-07}, 'activities': {'origin': 'learned', 'weight': 4.839327739872298e-06}, 'nursery': {'origin': 'learned', 'weight': 9.859417699637172e-07}, 'higher': {'origin': 'learned', 'weight': 1.2090653015743418e-07}, 'internet': {'origin': 'learned', 'weight': 3.826610819737762e-07}, 'romantic': {'origin': 'learned', 'weight': 1.7041739225182675e-05}, 'famrel': {'origin': 'learned', 'weight': 0.06395750625321515}, 'freetime': {'origin': 'learned', 'weight': 0.005298006953244488}, 'goout': {'origin': 'learned', 'weight': 0.017833992490542724}, 'Dalc': {'origin': 'learned', 'weight': 0.05639212133201029}, 'Walc': {'origin': 'learned', 'weight': -0.05655177993703371}, 'health': {'origin': 'learned', 'weight': -0.0017836759484594275}, 'absences': {'origin': 'learned', 'weight': -0.10963221670789629}, 'G1': {'origin': 'learned', 'weight': 0.3731879464225919}, 'G2': {'origin': 'learned', 'weight': 0.048587816372934696}, 'G3': {'origin': 'learned', 'weight': -0.04977786757469074}}, 'Fedu': {'address': {'origin': 'learned', 'weight': 1.815837863695999e-06}, 'famsize': {'origin': 'learned', 'weight': -5.875240692181356e-06}, 'Pstatus': {'origin': 'learned', 'weight': 1.0862756113952355e-06}, 'Medu': {'origin': 'learned', 'weight': 1.3815353478780808e-06}, 'traveltime': {'origin': 'learned', 'weight': 2.3458092007222387e-06}, 'studytime': {'origin': 'learned', 'weight': -0.002267727436488319}, 'failures': {'origin': 'learned', 'weight': -4.4896874864671566e-06}, 'schoolsup': {'origin': 'learned', 'weight': 3.5966507196187998e-06}, 'famsup': {'origin': 'learned', 'weight': 8.380912481855755e-06}, 'paid': {'origin': 'learned', 'weight': 1.5972940923620563e-06}, 'activities': {'origin': 'learned', 'weight': 2.2202292453444777e-05}, 'nursery': {'origin': 'learned', 'weight': 3.836377734813915e-06}, 'higher': {'origin': 'learned', 'weight': 4.6588574867353284e-07}, 'internet': {'origin': 'learned', 'weight': 1.6062126461530145e-06}, 'romantic': {'origin': 'learned', 'weight': 6.776538544245963e-05}, 'famrel': {'origin': 'learned', 'weight': 0.09036740104688158}, 'freetime': {'origin': 'learned', 'weight': 0.07269279661945031}, 'goout': {'origin': 'learned', 'weight': 0.001521336398273317}, 'Dalc': {'origin': 'learned', 'weight': 0.06540063043992946}, 'Walc': {'origin': 'learned', 'weight': 0.12603842388100064}, 'health': {'origin': 'learned', 'weight': 0.09655752353619704}, 'absences': {'origin': 'learned', 'weight': 0.34662147120177766}, 'G1': {'origin': 'learned', 'weight': 0.2457622670411357}, 'G2': {'origin': 'learned', 'weight': 0.06740156244799099}, 'G3': {'origin': 'learned', 'weight': 0.04209668187865408}}, 'traveltime': {'address': {'origin': 'learned', 'weight': -3.2083752911421134e-08}, 'famsize': {'origin': 'learned', 'weight': 5.681875851702312e-07}, 'Pstatus': {'origin': 'learned', 'weight': 1.5254924959846107e-07}, 'Medu': {'origin': 'learned', 'weight': -0.05682679496770537}, 'Fedu': {'origin': 'learned', 'weight': 0.04369105682484006}, 'studytime': {'origin': 'learned', 'weight': 0.14665592285551024}, 'failures': {'origin': 'learned', 'weight': 8.390113681439373e-07}, 'schoolsup': {'origin': 'learned', 'weight': 3.572657993912356e-06}, 'famsup': {'origin': 'learned', 'weight': 6.7280883915310845e-06}, 'paid': {'origin': 'learned', 'weight': 1.1047233320614985e-06}, 'activities': {'origin': 'learned', 'weight': 1.5182162182595177e-05}, 'nursery': {'origin': 'learned', 'weight': 1.4616510424530478e-06}, 'higher': {'origin': 'learned', 'weight': 2.1338297753062791e-07}, 'internet': {'origin': 'learned', 'weight': 1.6460904743183209e-06}, 'romantic': {'origin': 'learned', 'weight': 1.3548531245438947e-05}, 'famrel': {'origin': 'learned', 'weight': 0.3652619258538022}, 'freetime': {'origin': 'learned', 'weight': 0.1386601673406505}, 'goout': {'origin': 'learned', 'weight': 0.14543707996940677}, 'Dalc': {'origin': 'learned', 'weight': 0.2640464432914783}, 'Walc': {'origin': 'learned', 'weight': 0.1054311976437596}, 'health': {'origin': 'learned', 'weight': 0.05946039269548516}, 'absences': {'origin': 'learned', 'weight': 0.31742677251596246}, 'G1': {'origin': 'learned', 'weight': 0.4258522757563797}, 'G2': {'origin': 'learned', 'weight': 0.0452125282264167}, 'G3': {'origin': 'learned', 'weight': 0.1472529805083419}}, 'studytime': {'address': {'origin': 'learned', 'weight': 1.2094798742837836e-06}, 'famsize': {'origin': 'learned', 'weight': 2.2938931309765494e-06}, 'Pstatus': {'origin': 'learned', 'weight': 4.5152482925329287e-07}, 'Medu': {'origin': 'learned', 'weight': 1.0099464281901412e-05}, 'Fedu': {'origin': 'learned', 'weight': -0.000495670140147531}, 'traveltime': {'origin': 'learned', 'weight': 2.7298276113987395e-06}, 'failures': {'origin': 'learned', 'weight': -4.52614007711886e-07}, 'schoolsup': {'origin': 'learned', 'weight': 1.3187597528677218e-06}, 'famsup': {'origin': 'learned', 'weight': 3.733353224457675e-06}, 'paid': {'origin': 'learned', 'weight': 3.7336184729781297e-06}, 'activities': {'origin': 'learned', 'weight': 1.1962348457785248e-05}, 'nursery': {'origin': 'learned', 'weight': 3.5500670023818374e-06}, 'higher': {'origin': 'learned', 'weight': 2.3561892859955156e-07}, 'internet': {'origin': 'learned', 'weight': 2.96354399751265e-06}, 'romantic': {'origin': 'learned', 'weight': 1.3775916562081774e-05}, 'famrel': {'origin': 'learned', 'weight': 0.15816240290931505}, 'freetime': {'origin': 'learned', 'weight': 0.061672808424480724}, 'goout': {'origin': 'learned', 'weight': 0.050063594468249706}, 'Dalc': {'origin': 'learned', 'weight': -1.7407881648513562e-05}, 'Walc': {'origin': 'learned', 'weight': -0.13225283210928684}, 'health': {'origin': 'learned', 'weight': 0.044435607273602996}, 'absences': {'origin': 'learned', 'weight': -0.24449913460462702}, 'G1': {'origin': 'learned', 'weight': 0.8636139137063454}, 'G2': {'origin': 'learned', 'weight': 0.05362052988133593}, 'G3': {'origin': 'learned', 'weight': 0.07325427221999745}}, 'failures': {'address': {'origin': 'learned', 'weight': 1.0270730806788747e-06}, 'famsize': {'origin': 'learned', 'weight': 0.007199670534529419}, 'Pstatus': {'origin': 'learned', 'weight': 3.7113144071898173e-07}, 'Medu': {'origin': 'learned', 'weight': -0.05554902196378678}, 'Fedu': {'origin': 'learned', 'weight': -0.03634104972539488}, 'traveltime': {'origin': 'learned', 'weight': 0.28893299557926194}, 'studytime': {'origin': 'learned', 'weight': -0.036925581153895784}, 'schoolsup': {'origin': 'learned', 'weight': 1.2442168943478484e-06}, 'famsup': {'origin': 'learned', 'weight': 2.7970697872618514e-06}, 'paid': {'origin': 'learned', 'weight': 3.2799055993158386e-07}, 'activities': {'origin': 'learned', 'weight': 5.462903893005342e-06}, 'nursery': {'origin': 'learned', 'weight': 1.115736579162668e-06}, 'higher': {'origin': 'learned', 'weight': -1.583102592694493e-07}, 'internet': {'origin': 'learned', 'weight': -4.150375359058897e-08}, 'romantic': {'origin': 'learned', 'weight': 5.644847741993733e-06}, 'famrel': {'origin': 'learned', 'weight': 0.1668232709293059}, 'freetime': {'origin': 'learned', 'weight': 0.2757287584822249}, 'goout': {'origin': 'learned', 'weight': -0.00253721944936783}, 'Dalc': {'origin': 'learned', 'weight': 0.19852244938589078}, 'Walc': {'origin': 'learned', 'weight': 0.1110213039605426}, 'health': {'origin': 'learned', 'weight': 0.17934136094011674}, 'absences': {'origin': 'learned', 'weight': 0.9395791571697139}, 'G1': {'origin': 'learned', 'weight': -0.7734093106877317}, 'G2': {'origin': 'learned', 'weight': -0.17877938791798662}, 'G3': {'origin': 'learned', 'weight': -0.15972379098765793}}, 'schoolsup': {'address': {'origin': 'learned', 'weight': 0.09016610695015827}, 'famsize': {'origin': 'learned', 'weight': -0.07969030328801704}, 'Pstatus': {'origin': 'learned', 'weight': 0.0031060892594583374}, 'Medu': {'origin': 'learned', 'weight': -0.14973724028142785}, 'Fedu': {'origin': 'learned', 'weight': 0.111206285588392}, 'traveltime': {'origin': 'learned', 'weight': -0.05461326354951528}, 'studytime': {'origin': 'learned', 'weight': 0.2323474711325423}, 'failures': {'origin': 'learned', 'weight': 0.05344254788762017}, 'famsup': {'origin': 'learned', 'weight': 0.43115271308130015}, 'paid': {'origin': 'learned', 'weight': 4.393230469914194e-07}, 'activities': {'origin': 'learned', 'weight': 3.3289576319408384e-06}, 'nursery': {'origin': 'learned', 'weight': 0.21898204604390092}, 'higher': {'origin': 'learned', 'weight': 0.15113701551678627}, 'internet': {'origin': 'learned', 'weight': 0.04153209516996423}, 'romantic': {'origin': 'learned', 'weight': 1.741729645205567e-05}, 'famrel': {'origin': 'learned', 'weight': 0.013400176227771085}, 'freetime': {'origin': 'learned', 'weight': 0.08146892483723561}, 'goout': {'origin': 'learned', 'weight': -0.054048281147243506}, 'Dalc': {'origin': 'learned', 'weight': 0.030431446056897765}, 'Walc': {'origin': 'learned', 'weight': -0.28625533228773004}, 'health': {'origin': 'learned', 'weight': 0.16814364990171213}, 'absences': {'origin': 'learned', 'weight': -0.44169320558277186}, 'G1': {'origin': 'learned', 'weight': -0.8015184747758134}, 'G2': {'origin': 'learned', 'weight': 0.01756848085425741}, 'G3': {'origin': 'learned', 'weight': -0.16017431148807354}}, 'famsup': {'address': {'origin': 'learned', 'weight': 0.10427386381413724}, 'famsize': {'origin': 'learned', 'weight': 0.0016122619388671963}, 'Pstatus': {'origin': 'learned', 'weight': 0.08467752097138515}, 'Medu': {'origin': 'learned', 'weight': 0.2712033095860632}, 'Fedu': {'origin': 'learned', 'weight': 0.14573161333959725}, 'traveltime': {'origin': 'learned', 'weight': 0.09728374298715864}, 'studytime': {'origin': 'learned', 'weight': 0.266362204840018}, 'failures': {'origin': 'learned', 'weight': 0.08031678051890989}, 'schoolsup': {'origin': 'learned', 'weight': 1.633685547630518e-07}, 'paid': {'origin': 'learned', 'weight': 1.7014085331477617e-07}, 'activities': {'origin': 'learned', 'weight': 7.251013741149529e-07}, 'nursery': {'origin': 'learned', 'weight': 0.49493689368622484}, 'higher': {'origin': 'learned', 'weight': 0.17814403224742134}, 'internet': {'origin': 'learned', 'weight': 0.27715008710483463}, 'romantic': {'origin': 'learned', 'weight': 1.212623696766134e-06}, 'famrel': {'origin': 'learned', 'weight': 0.09564586270588174}, 'freetime': {'origin': 'learned', 'weight': 0.08487609151687552}, 'goout': {'origin': 'learned', 'weight': 0.09664059894202708}, 'Dalc': {'origin': 'learned', 'weight': 0.01911615512884646}, 'Walc': {'origin': 'learned', 'weight': -0.08227553368062841}, 'health': {'origin': 'learned', 'weight': 0.1009039626224132}, 'absences': {'origin': 'learned', 'weight': 0.6753957856896687}, 'G1': {'origin': 'learned', 'weight': 0.013792402912843525}, 'G2': {'origin': 'learned', 'weight': -0.008335288023269384}, 'G3': {'origin': 'learned', 'weight': 0.11012660720124419}}, 'paid': {'address': {'origin': 'learned', 'weight': -0.06226780216318523}, 'famsize': {'origin': 'learned', 'weight': -0.08662176398113904}, 'Pstatus': {'origin': 'learned', 'weight': 0.01940453653643334}, 'Medu': {'origin': 'learned', 'weight': 0.45092087317544877}, 'Fedu': {'origin': 'learned', 'weight': 0.07819729062203296}, 'traveltime': {'origin': 'learned', 'weight': -0.1751929065462438}, 'studytime': {'origin': 'learned', 'weight': -0.06792582697060526}, 'failures': {'origin': 'learned', 'weight': 0.19488310269441256}, 'schoolsup': {'origin': 'learned', 'weight': 0.10971256665441963}, 'famsup': {'origin': 'learned', 'weight': 0.3711694184171664}, 'activities': {'origin': 'learned', 'weight': 0.42980667486373997}, 'nursery': {'origin': 'learned', 'weight': 0.10713624144249709}, 'higher': {'origin': 'learned', 'weight': 0.0651615011059292}, 'internet': {'origin': 'learned', 'weight': 0.06155932087550792}, 'romantic': {'origin': 'learned', 'weight': 6.219147593514768e-06}, 'famrel': {'origin': 'learned', 'weight': 0.07276395951434235}, 'freetime': {'origin': 'learned', 'weight': -0.397084583455957}, 'goout': {'origin': 'learned', 'weight': -0.05554731045279839}, 'Dalc': {'origin': 'learned', 'weight': 0.18947644768941185}, 'Walc': {'origin': 'learned', 'weight': 0.03286301430594966}, 'health': {'origin': 'learned', 'weight': 0.2884379850406954}, 'absences': {'origin': 'learned', 'weight': -1.0534625350951718}, 'G1': {'origin': 'learned', 'weight': -0.7476665468841639}, 'G2': {'origin': 'learned', 'weight': 0.215077113364691}, 'G3': {'origin': 'learned', 'weight': -0.19159897136433737}}, 'activities': {'address': {'origin': 'learned', 'weight': 0.05553758017558176}, 'famsize': {'origin': 'learned', 'weight': 0.020024417715390045}, 'Pstatus': {'origin': 'learned', 'weight': 0.1186650900039901}, 'Medu': {'origin': 'learned', 'weight': 0.24111978808014004}, 'Fedu': {'origin': 'learned', 'weight': 0.022242975459254674}, 'traveltime': {'origin': 'learned', 'weight': 0.008463822567962324}, 'studytime': {'origin': 'learned', 'weight': 0.12516307931862}, 'failures': {'origin': 'learned', 'weight': 0.045406510982519854}, 'schoolsup': {'origin': 'learned', 'weight': 0.07942221196339495}, 'famsup': {'origin': 'learned', 'weight': 0.40747787530276136}, 'paid': {'origin': 'learned', 'weight': 1.0579930515164717e-07}, 'nursery': {'origin': 'learned', 'weight': 0.3870752878517111}, 'higher': {'origin': 'learned', 'weight': 0.10140915280647488}, 'internet': {'origin': 'learned', 'weight': 0.22115620514055448}, 'romantic': {'origin': 'learned', 'weight': 5.062885962223394e-07}, 'famrel': {'origin': 'learned', 'weight': 0.1060097717426425}, 'freetime': {'origin': 'learned', 'weight': 0.29025194859764786}, 'goout': {'origin': 'learned', 'weight': 0.053016213518201454}, 'Dalc': {'origin': 'learned', 'weight': 0.03508084451564856}, 'Walc': {'origin': 'learned', 'weight': 0.05822411086046015}, 'health': {'origin': 'learned', 'weight': -0.04472072932931432}, 'absences': {'origin': 'learned', 'weight': -0.011557604864954631}, 'G1': {'origin': 'learned', 'weight': 0.13356290095617598}, 'G2': {'origin': 'learned', 'weight': -0.02719253860768766}, 'G3': {'origin': 'learned', 'weight': 0.008521962648982792}}, 'nursery': {'address': {'origin': 'learned', 'weight': 0.2776178205344719}, 'famsize': {'origin': 'learned', 'weight': 0.20181916953441106}, 'Pstatus': {'origin': 'learned', 'weight': 0.18458724734437718}, 'Medu': {'origin': 'learned', 'weight': 0.5239103813400171}, 'Fedu': {'origin': 'learned', 'weight': 0.0576652012939855}, 'traveltime': {'origin': 'learned', 'weight': 0.3359494704671782}, 'studytime': {'origin': 'learned', 'weight': 0.18535635699631886}, 'failures': {'origin': 'learned', 'weight': 0.0750746154121407}, 'schoolsup': {'origin': 'learned', 'weight': 4.4501014882221276e-07}, 'famsup': {'origin': 'learned', 'weight': 5.245322452922104e-07}, 'paid': {'origin': 'learned', 'weight': 5.830128592885166e-07}, 'activities': {'origin': 'learned', 'weight': 8.75089591986338e-07}, 'higher': {'origin': 'learned', 'weight': 0.33856473446106944}, 'internet': {'origin': 'learned', 'weight': 0.4242928819958667}, 'romantic': {'origin': 'learned', 'weight': 2.139012622741077e-06}, 'famrel': {'origin': 'learned', 'weight': 0.432569121650298}, 'freetime': {'origin': 'learned', 'weight': 0.18200415195307637}, 'goout': {'origin': 'learned', 'weight': 0.17017617661645093}, 'Dalc': {'origin': 'learned', 'weight': -0.05664828517064359}, 'Walc': {'origin': 'learned', 'weight': 0.017727713239038333}, 'health': {'origin': 'learned', 'weight': 0.1833351895084601}, 'absences': {'origin': 'learned', 'weight': 0.19424952439476387}, 'G1': {'origin': 'learned', 'weight': 0.26458992819928057}, 'G2': {'origin': 'learned', 'weight': 0.07008782622305502}, 'G3': {'origin': 'learned', 'weight': -0.04178769441684207}}, 'higher': {'address': {'origin': 'learned', 'weight': 7.851783367975633e-07}, 'famsize': {'origin': 'learned', 'weight': 0.17370961720916422}, 'Pstatus': {'origin': 'learned', 'weight': 0.42470020866871444}, 'Medu': {'origin': 'learned', 'weight': 0.9842407795725915}, 'Fedu': {'origin': 'learned', 'weight': 0.28719837310478313}, 'traveltime': {'origin': 'learned', 'weight': 0.6652075929820775}, 'studytime': {'origin': 'learned', 'weight': 0.6614250646852067}, 'failures': {'origin': 'learned', 'weight': -0.30470801802731773}, 'schoolsup': {'origin': 'learned', 'weight': 1.2479890798999761e-06}, 'famsup': {'origin': 'learned', 'weight': 2.9132190513716887e-06}, 'paid': {'origin': 'learned', 'weight': 2.7674708199764802e-06}, 'activities': {'origin': 'learned', 'weight': 7.063695630694698e-06}, 'nursery': {'origin': 'learned', 'weight': 9.369537748463454e-07}, 'internet': {'origin': 'learned', 'weight': 7.463964327612281e-07}, 'romantic': {'origin': 'learned', 'weight': 2.268046145982143e-05}, 'famrel': {'origin': 'learned', 'weight': 0.749421075800239}, 'freetime': {'origin': 'learned', 'weight': 0.05992191532028243}, 'goout': {'origin': 'learned', 'weight': -0.02944249552655697}, 'Dalc': {'origin': 'learned', 'weight': -0.06561934921537634}, 'Walc': {'origin': 'learned', 'weight': 0.2709113403707566}, 'health': {'origin': 'learned', 'weight': 0.460475844352154}, 'absences': {'origin': 'learned', 'weight': -0.4644399619110806}, 'G1': {'origin': 'learned', 'weight': 2.6906165356962597}, 'G2': {'origin': 'learned', 'weight': 0.21293172852077402}, 'G3': {'origin': 'learned', 'weight': 0.161696919211617}}, 'internet': {'address': {'origin': 'learned', 'weight': 0.40328532019811464}, 'famsize': {'origin': 'learned', 'weight': 0.08161029156084386}, 'Pstatus': {'origin': 'learned', 'weight': 0.20073374119007015}, 'Medu': {'origin': 'learned', 'weight': 0.6875462651121823}, 'Fedu': {'origin': 'learned', 'weight': 0.06454075511391491}, 'traveltime': {'origin': 'learned', 'weight': -0.021094282505113388}, 'studytime': {'origin': 'learned', 'weight': 0.09306481319152346}, 'failures': {'origin': 'learned', 'weight': -0.015305344026746737}, 'schoolsup': {'origin': 'learned', 'weight': 1.7593655699762522e-06}, 'famsup': {'origin': 'learned', 'weight': 1.2448178984658832e-06}, 'paid': {'origin': 'learned', 'weight': 1.4622746367588082e-06}, 'activities': {'origin': 'learned', 'weight': 2.270135281570907e-06}, 'nursery': {'origin': 'learned', 'weight': 4.823286857399146e-07}, 'higher': {'origin': 'learned', 'weight': 0.27561946030947526}, 'romantic': {'origin': 'learned', 'weight': 5.241075220842723e-06}, 'famrel': {'origin': 'learned', 'weight': 0.40830632335954425}, 'freetime': {'origin': 'learned', 'weight': 0.19475274397573786}, 'goout': {'origin': 'learned', 'weight': 0.1408710805149382}, 'Dalc': {'origin': 'learned', 'weight': 0.2086038568514957}, 'Walc': {'origin': 'learned', 'weight': 0.1663542314573771}, 'health': {'origin': 'learned', 'weight': -0.12331190291514839}, 'absences': {'origin': 'learned', 'weight': 0.8369080746968736}, 'G1': {'origin': 'learned', 'weight': 0.4693377785294991}, 'G2': {'origin': 'learned', 'weight': 0.10416797222379809}, 'G3': {'origin': 'learned', 'weight': 0.12476082994216223}}, 'romantic': {'address': {'origin': 'learned', 'weight': 0.03449641423060724}, 'famsize': {'origin': 'learned', 'weight': 0.0001242279611122574}, 'Pstatus': {'origin': 'learned', 'weight': 0.03882760026404552}, 'Medu': {'origin': 'learned', 'weight': 0.057553976531306665}, 'Fedu': {'origin': 'learned', 'weight': -0.038502546594630475}, 'traveltime': {'origin': 'learned', 'weight': 0.14329667201511975}, 'studytime': {'origin': 'learned', 'weight': 0.15562427843420687}, 'failures': {'origin': 'learned', 'weight': 0.10425856564537055}, 'schoolsup': {'origin': 'learned', 'weight': 0.014368894340047815}, 'famsup': {'origin': 'learned', 'weight': 0.3147106400752427}, 'paid': {'origin': 'learned', 'weight': 0.04724004434882376}, 'activities': {'origin': 'learned', 'weight': 0.4895721690598813}, 'nursery': {'origin': 'learned', 'weight': 0.2448302568893097}, 'higher': {'origin': 'learned', 'weight': 0.013855780556472706}, 'internet': {'origin': 'learned', 'weight': 0.14405028246426685}, 'famrel': {'origin': 'learned', 'weight': 0.09273389200751765}, 'freetime': {'origin': 'learned', 'weight': 0.12148123441125036}, 'goout': {'origin': 'learned', 'weight': 0.011833625417886233}, 'Dalc': {'origin': 'learned', 'weight': 0.17526816121879552}, 'Walc': {'origin': 'learned', 'weight': -0.08849224803371417}, 'health': {'origin': 'learned', 'weight': 0.09235839989213118}, 'absences': {'origin': 'learned', 'weight': 0.7593034494873926}, 'G1': {'origin': 'learned', 'weight': 0.04875311772928067}, 'G2': {'origin': 'learned', 'weight': -0.039529109530973716}, 'G3': {'origin': 'learned', 'weight': -0.0005487024932422538}}, 'famrel': {'address': {'origin': 'learned', 'weight': 1.320897881340788e-06}, 'famsize': {'origin': 'learned', 'weight': 8.77451264318084e-07}, 'Pstatus': {'origin': 'learned', 'weight': 1.846478796364456e-07}, 'Medu': {'origin': 'learned', 'weight': 1.966155554661421e-05}, 'Fedu': {'origin': 'learned', 'weight': 5.614649983118622e-06}, 'traveltime': {'origin': 'learned', 'weight': 1.2821620220563868e-06}, 'studytime': {'origin': 'learned', 'weight': 2.7325071082731085e-06}, 'failures': {'origin': 'learned', 'weight': 1.8774318511130135e-06}, 'schoolsup': {'origin': 'learned', 'weight': 7.748541219982958e-06}, 'famsup': {'origin': 'learned', 'weight': 1.0392942107720905e-05}, 'paid': {'origin': 'learned', 'weight': 6.725986004009021e-06}, 'activities': {'origin': 'learned', 'weight': 1.7103940193342104e-05}, 'nursery': {'origin': 'learned', 'weight': 1.8503775845644034e-06}, 'higher': {'origin': 'learned', 'weight': 3.11903271403777e-07}, 'internet': {'origin': 'learned', 'weight': 1.1560838230536603e-06}, 'romantic': {'origin': 'learned', 'weight': 3.644736374916043e-05}, 'freetime': {'origin': 'learned', 'weight': 0.31156532861814135}, 'goout': {'origin': 'learned', 'weight': 0.13688329678438912}, 'Dalc': {'origin': 'learned', 'weight': 8.974158916716448e-06}, 'Walc': {'origin': 'learned', 'weight': 0.012488501523243383}, 'health': {'origin': 'learned', 'weight': 0.32535235552165176}, 'absences': {'origin': 'learned', 'weight': 0.029534730152577033}, 'G1': {'origin': 'learned', 'weight': 0.46833609431305073}, 'G2': {'origin': 'learned', 'weight': 0.20116104297386833}, 'G3': {'origin': 'learned', 'weight': -0.024238569511162412}}, 'freetime': {'address': {'origin': 'learned', 'weight': 4.999315254151007e-06}, 'famsize': {'origin': 'learned', 'weight': 7.565108486278707e-06}, 'Pstatus': {'origin': 'learned', 'weight': 9.210757723189831e-07}, 'Medu': {'origin': 'learned', 'weight': 5.3045604346644666e-05}, 'Fedu': {'origin': 'learned', 'weight': 1.0989037361421973e-05}, 'traveltime': {'origin': 'learned', 'weight': 5.4929092719122535e-06}, 'studytime': {'origin': 'learned', 'weight': 5.999391678181635e-06}, 'failures': {'origin': 'learned', 'weight': 1.454765326837019e-06}, 'schoolsup': {'origin': 'learned', 'weight': 1.083118372234952e-05}, 'famsup': {'origin': 'learned', 'weight': 2.9264384487782554e-05}, 'paid': {'origin': 'learned', 'weight': 4.7266131590172746e-07}, 'activities': {'origin': 'learned', 'weight': 7.199372883872205e-06}, 'nursery': {'origin': 'learned', 'weight': 7.151725171424487e-06}, 'higher': {'origin': 'learned', 'weight': 2.4368058171397756e-06}, 'internet': {'origin': 'learned', 'weight': 3.6712820497747034e-06}, 'romantic': {'origin': 'learned', 'weight': 2.6581035887039415e-05}, 'famrel': {'origin': 'learned', 'weight': 2.6864503278375758e-06}, 'goout': {'origin': 'learned', 'weight': 0.3402337019417903}, 'Dalc': {'origin': 'learned', 'weight': 9.033290147904766e-06}, 'Walc': {'origin': 'learned', 'weight': 5.723497269328464e-06}, 'health': {'origin': 'learned', 'weight': 0.20359128011716196}, 'absences': {'origin': 'learned', 'weight': -0.13258912399887035}, 'G1': {'origin': 'learned', 'weight': 0.15893694608957573}, 'G2': {'origin': 'learned', 'weight': -0.021466939129440744}, 'G3': {'origin': 'learned', 'weight': -0.035291910715639876}}, 'goout': {'address': {'origin': 'learned', 'weight': 3.2035805298097187e-06}, 'famsize': {'origin': 'learned', 'weight': 2.860011965556905e-06}, 'Pstatus': {'origin': 'learned', 'weight': 3.2360205696198744e-06}, 'Medu': {'origin': 'learned', 'weight': 0.00013893787430084464}, 'Fedu': {'origin': 'learned', 'weight': 3.500255190181704e-05}, 'traveltime': {'origin': 'learned', 'weight': 7.206819224813103e-06}, 'studytime': {'origin': 'learned', 'weight': 5.392816587318543e-06}, 'failures': {'origin': 'learned', 'weight': 1.2758953810800162e-05}, 'schoolsup': {'origin': 'learned', 'weight': 9.292721765645084e-06}, 'famsup': {'origin': 'learned', 'weight': 3.142034075725276e-05}, 'paid': {'origin': 'learned', 'weight': 6.015041527997529e-06}, 'activities': {'origin': 'learned', 'weight': 4.984497634306652e-05}, 'nursery': {'origin': 'learned', 'weight': 1.0622247426374497e-05}, 'higher': {'origin': 'learned', 'weight': 6.733122212252568e-06}, 'internet': {'origin': 'learned', 'weight': 6.996845346414707e-06}, 'romantic': {'origin': 'learned', 'weight': 0.00014000699129624396}, 'famrel': {'origin': 'learned', 'weight': 8.279250568554317e-06}, 'freetime': {'origin': 'learned', 'weight': 2.2300812352732997e-06}, 'Dalc': {'origin': 'learned', 'weight': 4.8560363036115805e-06}, 'Walc': {'origin': 'learned', 'weight': 2.1472173559096028e-06}, 'health': {'origin': 'learned', 'weight': -0.12015368066308832}, 'absences': {'origin': 'learned', 'weight': 0.22748994743278778}, 'G1': {'origin': 'learned', 'weight': 0.0725254040091578}, 'G2': {'origin': 'learned', 'weight': -0.008887013971329476}, 'G3': {'origin': 'learned', 'weight': -0.005467748034587408}}, 'Dalc': {'address': {'origin': 'learned', 'weight': 2.443914771173288e-06}, 'famsize': {'origin': 'learned', 'weight': 6.124775682118712e-07}, 'Pstatus': {'origin': 'learned', 'weight': 3.3480538042122376e-07}, 'Medu': {'origin': 'learned', 'weight': 1.8941343308167783e-05}, 'Fedu': {'origin': 'learned', 'weight': 6.684651844691612e-06}, 'traveltime': {'origin': 'learned', 'weight': 1.6720888589429364e-06}, 'studytime': {'origin': 'learned', 'weight': -0.04079588249535337}, 'failures': {'origin': 'learned', 'weight': 1.5180401053457686e-06}, 'schoolsup': {'origin': 'learned', 'weight': 2.6577884822509986e-05}, 'famsup': {'origin': 'learned', 'weight': 3.898305342873185e-05}, 'paid': {'origin': 'learned', 'weight': 1.3187861051116028e-06}, 'activities': {'origin': 'learned', 'weight': 4.86850586028225e-05}, 'nursery': {'origin': 'learned', 'weight': 9.098998339948322e-06}, 'higher': {'origin': 'learned', 'weight': 1.3772195017901158e-06}, 'internet': {'origin': 'learned', 'weight': 1.9892730666634255e-06}, 'romantic': {'origin': 'learned', 'weight': 1.1085710188018912e-05}, 'famrel': {'origin': 'learned', 'weight': 0.061860074406191755}, 'freetime': {'origin': 'learned', 'weight': 0.08959510517136154}, 'goout': {'origin': 'learned', 'weight': -0.0024505554268309045}, 'Walc': {'origin': 'learned', 'weight': 0.8623769618608512}, 'health': {'origin': 'learned', 'weight': 0.0062315200782290985}, 'absences': {'origin': 'learned', 'weight': 0.6285293747934196}, 'G1': {'origin': 'learned', 'weight': -0.1679903202090344}, 'G2': {'origin': 'learned', 'weight': 0.01828514198351367}, 'G3': {'origin': 'learned', 'weight': -0.06069763850187142}}, 'Walc': {'address': {'origin': 'learned', 'weight': 2.3235931090372038e-06}, 'famsize': {'origin': 'learned', 'weight': 9.661335752092414e-07}, 'Pstatus': {'origin': 'learned', 'weight': 4.580593050516383e-07}, 'Medu': {'origin': 'learned', 'weight': 1.0234019307479275e-05}, 'Fedu': {'origin': 'learned', 'weight': 5.230869729896622e-06}, 'traveltime': {'origin': 'learned', 'weight': 3.823707461640614e-06}, 'studytime': {'origin': 'learned', 'weight': -3.7312092819954272e-06}, 'failures': {'origin': 'learned', 'weight': 3.1858816041837672e-06}, 'schoolsup': {'origin': 'learned', 'weight': 6.602704056446805e-07}, 'famsup': {'origin': 'learned', 'weight': 2.462099835786531e-05}, 'paid': {'origin': 'learned', 'weight': 4.096182615608204e-06}, 'activities': {'origin': 'learned', 'weight': 4.679631804837704e-05}, 'nursery': {'origin': 'learned', 'weight': 1.4819511531044937e-05}, 'higher': {'origin': 'learned', 'weight': 1.0224844526732827e-06}, 'internet': {'origin': 'learned', 'weight': 3.2089637875986894e-06}, 'romantic': {'origin': 'learned', 'weight': 2.529025287342515e-05}, 'famrel': {'origin': 'learned', 'weight': -2.572005415955528e-05}, 'freetime': {'origin': 'learned', 'weight': 0.1213001152355078}, 'goout': {'origin': 'learned', 'weight': 0.3524600102352628}, 'Dalc': {'origin': 'learned', 'weight': 6.927723939556109e-07}, 'health': {'origin': 'learned', 'weight': 0.22910017223115414}, 'absences': {'origin': 'learned', 'weight': 0.28212912867979606}, 'G1': {'origin': 'learned', 'weight': 0.01628754240663206}, 'G2': {'origin': 'learned', 'weight': -0.028336314998879123}, 'G3': {'origin': 'learned', 'weight': -0.017052027248871705}}, 'health': {'address': {'origin': 'learned', 'weight': 2.495006069707716e-06}, 'famsize': {'origin': 'learned', 'weight': 4.5809455483301075e-06}, 'Pstatus': {'origin': 'learned', 'weight': 9.494811331021372e-07}, 'Medu': {'origin': 'learned', 'weight': 5.323859031710839e-05}, 'Fedu': {'origin': 'learned', 'weight': 8.728697764773375e-06}, 'traveltime': {'origin': 'learned', 'weight': 1.0242635060847743e-05}, 'studytime': {'origin': 'learned', 'weight': 8.714528708551217e-06}, 'failures': {'origin': 'learned', 'weight': 2.806745787568456e-06}, 'schoolsup': {'origin': 'learned', 'weight': 3.8134498853512872e-06}, 'famsup': {'origin': 'learned', 'weight': 2.320637753493311e-05}, 'paid': {'origin': 'learned', 'weight': 1.3045542586857709e-06}, 'activities': {'origin': 'learned', 'weight': 5.101290264386016e-05}, 'nursery': {'origin': 'learned', 'weight': 7.240116351111648e-06}, 'higher': {'origin': 'learned', 'weight': 6.676523819363924e-07}, 'internet': {'origin': 'learned', 'weight': 4.782931502866295e-06}, 'romantic': {'origin': 'learned', 'weight': 6.18192581736639e-05}, 'famrel': {'origin': 'learned', 'weight': 2.7931909257193434e-06}, 'freetime': {'origin': 'learned', 'weight': 2.8779314964966107e-06}, 'goout': {'origin': 'learned', 'weight': -5.738929894237622e-06}, 'Dalc': {'origin': 'learned', 'weight': 6.5806594432733315e-06}, 'Walc': {'origin': 'learned', 'weight': 2.5242442268968173e-06}, 'absences': {'origin': 'learned', 'weight': 0.013270440047704299}, 'G1': {'origin': 'learned', 'weight': 0.09831680087724673}, 'G2': {'origin': 'learned', 'weight': -0.0655360822154847}, 'G3': {'origin': 'learned', 'weight': -0.03549672945498936}}, 'absences': {'address': {'origin': 'learned', 'weight': 2.1954756979199574e-07}, 'famsize': {'origin': 'learned', 'weight': 8.597580220229035e-07}, 'Pstatus': {'origin': 'learned', 'weight': 3.110979370027898e-08}, 'Medu': {'origin': 'learned', 'weight': 3.818433288195618e-06}, 'Fedu': {'origin': 'learned', 'weight': 1.8252677120908404e-06}, 'traveltime': {'origin': 'learned', 'weight': 2.2660262196440774e-06}, 'studytime': {'origin': 'learned', 'weight': -1.6241967207249302e-06}, 'failures': {'origin': 'learned', 'weight': 3.1040475703698455e-07}, 'schoolsup': {'origin': 'learned', 'weight': 3.2795583819598026e-07}, 'famsup': {'origin': 'learned', 'weight': 1.2319092982466107e-06}, 'paid': {'origin': 'learned', 'weight': 6.232694334298974e-08}, 'activities': {'origin': 'learned', 'weight': 6.813282419837235e-06}, 'nursery': {'origin': 'learned', 'weight': 1.783222076390664e-06}, 'higher': {'origin': 'learned', 'weight': 5.590376239583715e-08}, 'internet': {'origin': 'learned', 'weight': 3.687447609686423e-07}, 'romantic': {'origin': 'learned', 'weight': 1.6291233178806432e-06}, 'famrel': {'origin': 'learned', 'weight': 6.761395164008487e-06}, 'freetime': {'origin': 'learned', 'weight': -2.8147000352287287e-06}, 'goout': {'origin': 'learned', 'weight': 2.98875965846704e-06}, 'Dalc': {'origin': 'learned', 'weight': 1.2537933032705393e-06}, 'Walc': {'origin': 'learned', 'weight': 2.9049481240489784e-06}, 'health': {'origin': 'learned', 'weight': -2.3873787462029974e-05}, 'G1': {'origin': 'learned', 'weight': -1.5031127212036804e-06}, 'G2': {'origin': 'learned', 'weight': 3.886996614933009e-06}, 'G3': {'origin': 'learned', 'weight': 3.987948656636059e-06}}, 'G1': {'address': {'origin': 'learned', 'weight': 4.145635565322556e-07}, 'famsize': {'origin': 'learned', 'weight': 4.231758239400621e-07}, 'Pstatus': {'origin': 'learned', 'weight': 1.2192523374411585e-07}, 'Medu': {'origin': 'learned', 'weight': 3.524468719738307e-06}, 'Fedu': {'origin': 'learned', 'weight': 2.655572153653365e-06}, 'traveltime': {'origin': 'learned', 'weight': 1.6493706472793821e-06}, 'studytime': {'origin': 'learned', 'weight': 5.880507684560454e-07}, 'failures': {'origin': 'learned', 'weight': -1.7871574230049647e-07}, 'schoolsup': {'origin': 'learned', 'weight': 4.865957647916266e-07}, 'famsup': {'origin': 'learned', 'weight': 7.719161908753132e-06}, 'paid': {'origin': 'learned', 'weight': 4.879860760979429e-07}, 'activities': {'origin': 'learned', 'weight': 1.573168543985265e-05}, 'nursery': {'origin': 'learned', 'weight': 2.2310985066482208e-06}, 'higher': {'origin': 'learned', 'weight': 1.1238345971304325e-07}, 'internet': {'origin': 'learned', 'weight': 1.1594765224713857e-06}, 'romantic': {'origin': 'learned', 'weight': 4.5568396125773596e-05}, 'famrel': {'origin': 'learned', 'weight': 2.1548227065399565e-06}, 'freetime': {'origin': 'learned', 'weight': 5.557825534741226e-06}, 'goout': {'origin': 'learned', 'weight': 9.449183937356098e-06}, 'Dalc': {'origin': 'learned', 'weight': -1.5501567349024007e-06}, 'Walc': {'origin': 'learned', 'weight': 5.0681509628027555e-05}, 'health': {'origin': 'learned', 'weight': 1.4456180749546806e-05}, 'absences': {'origin': 'learned', 'weight': -0.16519243826107544}, 'G2': {'origin': 'learned', 'weight': 0.8893123602483163}, 'G3': {'origin': 'learned', 'weight': 0.1314622702860853}}, 'G2': {'address': {'origin': 'learned', 'weight': 1.0808731900149392e-06}, 'famsize': {'origin': 'learned', 'weight': 1.018204545261268e-06}, 'Pstatus': {'origin': 'learned', 'weight': 4.0197743788316634e-07}, 'Medu': {'origin': 'learned', 'weight': 9.147904181797066e-06}, 'Fedu': {'origin': 'learned', 'weight': 6.073498805912339e-06}, 'traveltime': {'origin': 'learned', 'weight': 4.277353370007445e-06}, 'studytime': {'origin': 'learned', 'weight': 1.4113913670578505e-06}, 'failures': {'origin': 'learned', 'weight': -5.18613014617815e-07}, 'schoolsup': {'origin': 'learned', 'weight': 1.3800602422165208e-06}, 'famsup': {'origin': 'learned', 'weight': 3.0220831125406032e-05}, 'paid': {'origin': 'learned', 'weight': 1.1816940754479807e-06}, 'activities': {'origin': 'learned', 'weight': 5.669885412547309e-05}, 'nursery': {'origin': 'learned', 'weight': 7.608200291011169e-06}, 'higher': {'origin': 'learned', 'weight': 1.9509765374517475e-07}, 'internet': {'origin': 'learned', 'weight': 3.3812595236012536e-06}, 'romantic': {'origin': 'learned', 'weight': 0.000163890714845625}, 'famrel': {'origin': 'learned', 'weight': 4.421633581782909e-06}, 'freetime': {'origin': 'learned', 'weight': 9.63198572344712e-06}, 'goout': {'origin': 'learned', 'weight': 2.416742610715618e-05}, 'Dalc': {'origin': 'learned', 'weight': -4.049949010417597e-06}, 'Walc': {'origin': 'learned', 'weight': 4.391655782041878e-06}, 'health': {'origin': 'learned', 'weight': 3.863184393270905e-06}, 'absences': {'origin': 'learned', 'weight': -0.12083364187284075}, 'G1': {'origin': 'learned', 'weight': 4.852215936739337e-06}, 'G3': {'origin': 'learned', 'weight': 0.884705682463779}}, 'G3': {'address': {'origin': 'learned', 'weight': 2.8997294244065144e-06}, 'famsize': {'origin': 'learned', 'weight': 3.6447543713365855e-06}, 'Pstatus': {'origin': 'learned', 'weight': 1.2383169619592981e-06}, 'Medu': {'origin': 'learned', 'weight': 2.7181742380645266e-05}, 'Fedu': {'origin': 'learned', 'weight': 1.7927492482726562e-05}, 'traveltime': {'origin': 'learned', 'weight': 8.956896659868888e-06}, 'studytime': {'origin': 'learned', 'weight': 5.052203280123686e-06}, 'failures': {'origin': 'learned', 'weight': -1.621351356540549e-06}, 'schoolsup': {'origin': 'learned', 'weight': 3.7300833122935385e-06}, 'famsup': {'origin': 'learned', 'weight': 6.9595740834268e-05}, 'paid': {'origin': 'learned', 'weight': 2.618791872592911e-06}, 'activities': {'origin': 'learned', 'weight': 0.00019957011213946537}, 'nursery': {'origin': 'learned', 'weight': 2.8136654487595504e-05}, 'higher': {'origin': 'learned', 'weight': 7.976562142570407e-07}, 'internet': {'origin': 'learned', 'weight': 1.1023378253076663e-05}, 'romantic': {'origin': 'learned', 'weight': 0.0005007381639334503}, 'famrel': {'origin': 'learned', 'weight': 1.2436281655857373e-05}, 'freetime': {'origin': 'learned', 'weight': 1.4630621123820853e-05}, 'goout': {'origin': 'learned', 'weight': 8.885235654394119e-05}, 'Dalc': {'origin': 'learned', 'weight': -1.519052520577944e-05}, 'Walc': {'origin': 'learned', 'weight': -5.154448682834879e-06}, 'health': {'origin': 'learned', 'weight': -8.85746266481034e-07}, 'absences': {'origin': 'learned', 'weight': 0.2799693506960016}, 'G1': {'origin': 'learned', 'weight': 1.2269310076312509e-05}, 'G2': {'origin': 'learned', 'weight': 1.6073761334772817e-06}}})




```python
structureModelPruned.adj
```




    AdjacencyView({'address': {'absences': {'origin': 'learned', 'weight': 1.0400949529066366}, 'G1': {'origin': 'learned', 'weight': 1.006295091882122}}, 'famsize': {}, 'Pstatus': {'famrel': {'origin': 'learned', 'weight': 0.8402877660070628}, 'absences': {'origin': 'learned', 'weight': -1.0538754156321408}, 'G1': {'origin': 'learned', 'weight': 1.261362346111696}}, 'Medu': {}, 'Fedu': {}, 'traveltime': {}, 'studytime': {'G1': {'origin': 'learned', 'weight': 0.8636139137063454}}, 'failures': {'absences': {'origin': 'learned', 'weight': 0.9395791571697139}}, 'schoolsup': {'G1': {'origin': 'learned', 'weight': -0.8015184747758134}}, 'famsup': {}, 'paid': {'absences': {'origin': 'learned', 'weight': -1.0534625350951718}}, 'activities': {}, 'nursery': {}, 'higher': {'Medu': {'origin': 'learned', 'weight': 0.9842407795725915}, 'G1': {'origin': 'learned', 'weight': 2.6906165356962597}}, 'internet': {'absences': {'origin': 'learned', 'weight': 0.8369080746968736}}, 'romantic': {}, 'famrel': {}, 'freetime': {}, 'goout': {}, 'Dalc': {'Walc': {'origin': 'learned', 'weight': 0.8623769618608512}}, 'Walc': {}, 'health': {}, 'absences': {}, 'G1': {'G2': {'origin': 'learned', 'weight': 0.8893123602483163}}, 'G2': {'G3': {'origin': 'learned', 'weight': 0.884705682463779}}, 'G3': {}})




```python
structureModelLearned.degree
```




    DiDegreeView({'address': 50, 'famsize': 50, 'Pstatus': 50, 'Medu': 50, 'Fedu': 50, 'traveltime': 50, 'studytime': 50, 'failures': 50, 'schoolsup': 50, 'famsup': 50, 'paid': 50, 'activities': 50, 'nursery': 50, 'higher': 50, 'internet': 50, 'romantic': 50, 'famrel': 50, 'freetime': 50, 'goout': 50, 'Dalc': 50, 'Walc': 50, 'health': 50, 'absences': 50, 'G1': 50, 'G2': 50, 'G3': 50})




```python
structureModelPruned.degree
```




    DiDegreeView({'address': 2, 'famsize': 0, 'Pstatus': 3, 'Medu': 1, 'Fedu': 0, 'traveltime': 0, 'studytime': 1, 'failures': 1, 'schoolsup': 1, 'famsup': 0, 'paid': 1, 'activities': 0, 'nursery': 0, 'higher': 2, 'internet': 1, 'romantic': 0, 'famrel': 1, 'freetime': 0, 'goout': 0, 'Dalc': 1, 'Walc': 1, 'health': 0, 'absences': 5, 'G1': 6, 'G2': 2, 'G3': 1})




```python
structureModelLearned.edges
```




    OutEdgeView([('address', 'famsize'), ('address', 'Pstatus'), ('address', 'Medu'), ('address', 'Fedu'), ('address', 'traveltime'), ('address', 'studytime'), ('address', 'failures'), ('address', 'schoolsup'), ('address', 'famsup'), ('address', 'paid'), ('address', 'activities'), ('address', 'nursery'), ('address', 'higher'), ('address', 'internet'), ('address', 'romantic'), ('address', 'famrel'), ('address', 'freetime'), ('address', 'goout'), ('address', 'Dalc'), ('address', 'Walc'), ('address', 'health'), ('address', 'absences'), ('address', 'G1'), ('address', 'G2'), ('address', 'G3'), ('famsize', 'address'), ('famsize', 'Pstatus'), ('famsize', 'Medu'), ('famsize', 'Fedu'), ('famsize', 'traveltime'), ('famsize', 'studytime'), ('famsize', 'failures'), ('famsize', 'schoolsup'), ('famsize', 'famsup'), ('famsize', 'paid'), ('famsize', 'activities'), ('famsize', 'nursery'), ('famsize', 'higher'), ('famsize', 'internet'), ('famsize', 'romantic'), ('famsize', 'famrel'), ('famsize', 'freetime'), ('famsize', 'goout'), ('famsize', 'Dalc'), ('famsize', 'Walc'), ('famsize', 'health'), ('famsize', 'absences'), ('famsize', 'G1'), ('famsize', 'G2'), ('famsize', 'G3'), ('Pstatus', 'address'), ('Pstatus', 'famsize'), ('Pstatus', 'Medu'), ('Pstatus', 'Fedu'), ('Pstatus', 'traveltime'), ('Pstatus', 'studytime'), ('Pstatus', 'failures'), ('Pstatus', 'schoolsup'), ('Pstatus', 'famsup'), ('Pstatus', 'paid'), ('Pstatus', 'activities'), ('Pstatus', 'nursery'), ('Pstatus', 'higher'), ('Pstatus', 'internet'), ('Pstatus', 'romantic'), ('Pstatus', 'famrel'), ('Pstatus', 'freetime'), ('Pstatus', 'goout'), ('Pstatus', 'Dalc'), ('Pstatus', 'Walc'), ('Pstatus', 'health'), ('Pstatus', 'absences'), ('Pstatus', 'G1'), ('Pstatus', 'G2'), ('Pstatus', 'G3'), ('Medu', 'address'), ('Medu', 'famsize'), ('Medu', 'Pstatus'), ('Medu', 'Fedu'), ('Medu', 'traveltime'), ('Medu', 'studytime'), ('Medu', 'failures'), ('Medu', 'schoolsup'), ('Medu', 'famsup'), ('Medu', 'paid'), ('Medu', 'activities'), ('Medu', 'nursery'), ('Medu', 'higher'), ('Medu', 'internet'), ('Medu', 'romantic'), ('Medu', 'famrel'), ('Medu', 'freetime'), ('Medu', 'goout'), ('Medu', 'Dalc'), ('Medu', 'Walc'), ('Medu', 'health'), ('Medu', 'absences'), ('Medu', 'G1'), ('Medu', 'G2'), ('Medu', 'G3'), ('Fedu', 'address'), ('Fedu', 'famsize'), ('Fedu', 'Pstatus'), ('Fedu', 'Medu'), ('Fedu', 'traveltime'), ('Fedu', 'studytime'), ('Fedu', 'failures'), ('Fedu', 'schoolsup'), ('Fedu', 'famsup'), ('Fedu', 'paid'), ('Fedu', 'activities'), ('Fedu', 'nursery'), ('Fedu', 'higher'), ('Fedu', 'internet'), ('Fedu', 'romantic'), ('Fedu', 'famrel'), ('Fedu', 'freetime'), ('Fedu', 'goout'), ('Fedu', 'Dalc'), ('Fedu', 'Walc'), ('Fedu', 'health'), ('Fedu', 'absences'), ('Fedu', 'G1'), ('Fedu', 'G2'), ('Fedu', 'G3'), ('traveltime', 'address'), ('traveltime', 'famsize'), ('traveltime', 'Pstatus'), ('traveltime', 'Medu'), ('traveltime', 'Fedu'), ('traveltime', 'studytime'), ('traveltime', 'failures'), ('traveltime', 'schoolsup'), ('traveltime', 'famsup'), ('traveltime', 'paid'), ('traveltime', 'activities'), ('traveltime', 'nursery'), ('traveltime', 'higher'), ('traveltime', 'internet'), ('traveltime', 'romantic'), ('traveltime', 'famrel'), ('traveltime', 'freetime'), ('traveltime', 'goout'), ('traveltime', 'Dalc'), ('traveltime', 'Walc'), ('traveltime', 'health'), ('traveltime', 'absences'), ('traveltime', 'G1'), ('traveltime', 'G2'), ('traveltime', 'G3'), ('studytime', 'address'), ('studytime', 'famsize'), ('studytime', 'Pstatus'), ('studytime', 'Medu'), ('studytime', 'Fedu'), ('studytime', 'traveltime'), ('studytime', 'failures'), ('studytime', 'schoolsup'), ('studytime', 'famsup'), ('studytime', 'paid'), ('studytime', 'activities'), ('studytime', 'nursery'), ('studytime', 'higher'), ('studytime', 'internet'), ('studytime', 'romantic'), ('studytime', 'famrel'), ('studytime', 'freetime'), ('studytime', 'goout'), ('studytime', 'Dalc'), ('studytime', 'Walc'), ('studytime', 'health'), ('studytime', 'absences'), ('studytime', 'G1'), ('studytime', 'G2'), ('studytime', 'G3'), ('failures', 'address'), ('failures', 'famsize'), ('failures', 'Pstatus'), ('failures', 'Medu'), ('failures', 'Fedu'), ('failures', 'traveltime'), ('failures', 'studytime'), ('failures', 'schoolsup'), ('failures', 'famsup'), ('failures', 'paid'), ('failures', 'activities'), ('failures', 'nursery'), ('failures', 'higher'), ('failures', 'internet'), ('failures', 'romantic'), ('failures', 'famrel'), ('failures', 'freetime'), ('failures', 'goout'), ('failures', 'Dalc'), ('failures', 'Walc'), ('failures', 'health'), ('failures', 'absences'), ('failures', 'G1'), ('failures', 'G2'), ('failures', 'G3'), ('schoolsup', 'address'), ('schoolsup', 'famsize'), ('schoolsup', 'Pstatus'), ('schoolsup', 'Medu'), ('schoolsup', 'Fedu'), ('schoolsup', 'traveltime'), ('schoolsup', 'studytime'), ('schoolsup', 'failures'), ('schoolsup', 'famsup'), ('schoolsup', 'paid'), ('schoolsup', 'activities'), ('schoolsup', 'nursery'), ('schoolsup', 'higher'), ('schoolsup', 'internet'), ('schoolsup', 'romantic'), ('schoolsup', 'famrel'), ('schoolsup', 'freetime'), ('schoolsup', 'goout'), ('schoolsup', 'Dalc'), ('schoolsup', 'Walc'), ('schoolsup', 'health'), ('schoolsup', 'absences'), ('schoolsup', 'G1'), ('schoolsup', 'G2'), ('schoolsup', 'G3'), ('famsup', 'address'), ('famsup', 'famsize'), ('famsup', 'Pstatus'), ('famsup', 'Medu'), ('famsup', 'Fedu'), ('famsup', 'traveltime'), ('famsup', 'studytime'), ('famsup', 'failures'), ('famsup', 'schoolsup'), ('famsup', 'paid'), ('famsup', 'activities'), ('famsup', 'nursery'), ('famsup', 'higher'), ('famsup', 'internet'), ('famsup', 'romantic'), ('famsup', 'famrel'), ('famsup', 'freetime'), ('famsup', 'goout'), ('famsup', 'Dalc'), ('famsup', 'Walc'), ('famsup', 'health'), ('famsup', 'absences'), ('famsup', 'G1'), ('famsup', 'G2'), ('famsup', 'G3'), ('paid', 'address'), ('paid', 'famsize'), ('paid', 'Pstatus'), ('paid', 'Medu'), ('paid', 'Fedu'), ('paid', 'traveltime'), ('paid', 'studytime'), ('paid', 'failures'), ('paid', 'schoolsup'), ('paid', 'famsup'), ('paid', 'activities'), ('paid', 'nursery'), ('paid', 'higher'), ('paid', 'internet'), ('paid', 'romantic'), ('paid', 'famrel'), ('paid', 'freetime'), ('paid', 'goout'), ('paid', 'Dalc'), ('paid', 'Walc'), ('paid', 'health'), ('paid', 'absences'), ('paid', 'G1'), ('paid', 'G2'), ('paid', 'G3'), ('activities', 'address'), ('activities', 'famsize'), ('activities', 'Pstatus'), ('activities', 'Medu'), ('activities', 'Fedu'), ('activities', 'traveltime'), ('activities', 'studytime'), ('activities', 'failures'), ('activities', 'schoolsup'), ('activities', 'famsup'), ('activities', 'paid'), ('activities', 'nursery'), ('activities', 'higher'), ('activities', 'internet'), ('activities', 'romantic'), ('activities', 'famrel'), ('activities', 'freetime'), ('activities', 'goout'), ('activities', 'Dalc'), ('activities', 'Walc'), ('activities', 'health'), ('activities', 'absences'), ('activities', 'G1'), ('activities', 'G2'), ('activities', 'G3'), ('nursery', 'address'), ('nursery', 'famsize'), ('nursery', 'Pstatus'), ('nursery', 'Medu'), ('nursery', 'Fedu'), ('nursery', 'traveltime'), ('nursery', 'studytime'), ('nursery', 'failures'), ('nursery', 'schoolsup'), ('nursery', 'famsup'), ('nursery', 'paid'), ('nursery', 'activities'), ('nursery', 'higher'), ('nursery', 'internet'), ('nursery', 'romantic'), ('nursery', 'famrel'), ('nursery', 'freetime'), ('nursery', 'goout'), ('nursery', 'Dalc'), ('nursery', 'Walc'), ('nursery', 'health'), ('nursery', 'absences'), ('nursery', 'G1'), ('nursery', 'G2'), ('nursery', 'G3'), ('higher', 'address'), ('higher', 'famsize'), ('higher', 'Pstatus'), ('higher', 'Medu'), ('higher', 'Fedu'), ('higher', 'traveltime'), ('higher', 'studytime'), ('higher', 'failures'), ('higher', 'schoolsup'), ('higher', 'famsup'), ('higher', 'paid'), ('higher', 'activities'), ('higher', 'nursery'), ('higher', 'internet'), ('higher', 'romantic'), ('higher', 'famrel'), ('higher', 'freetime'), ('higher', 'goout'), ('higher', 'Dalc'), ('higher', 'Walc'), ('higher', 'health'), ('higher', 'absences'), ('higher', 'G1'), ('higher', 'G2'), ('higher', 'G3'), ('internet', 'address'), ('internet', 'famsize'), ('internet', 'Pstatus'), ('internet', 'Medu'), ('internet', 'Fedu'), ('internet', 'traveltime'), ('internet', 'studytime'), ('internet', 'failures'), ('internet', 'schoolsup'), ('internet', 'famsup'), ('internet', 'paid'), ('internet', 'activities'), ('internet', 'nursery'), ('internet', 'higher'), ('internet', 'romantic'), ('internet', 'famrel'), ('internet', 'freetime'), ('internet', 'goout'), ('internet', 'Dalc'), ('internet', 'Walc'), ('internet', 'health'), ('internet', 'absences'), ('internet', 'G1'), ('internet', 'G2'), ('internet', 'G3'), ('romantic', 'address'), ('romantic', 'famsize'), ('romantic', 'Pstatus'), ('romantic', 'Medu'), ('romantic', 'Fedu'), ('romantic', 'traveltime'), ('romantic', 'studytime'), ('romantic', 'failures'), ('romantic', 'schoolsup'), ('romantic', 'famsup'), ('romantic', 'paid'), ('romantic', 'activities'), ('romantic', 'nursery'), ('romantic', 'higher'), ('romantic', 'internet'), ('romantic', 'famrel'), ('romantic', 'freetime'), ('romantic', 'goout'), ('romantic', 'Dalc'), ('romantic', 'Walc'), ('romantic', 'health'), ('romantic', 'absences'), ('romantic', 'G1'), ('romantic', 'G2'), ('romantic', 'G3'), ('famrel', 'address'), ('famrel', 'famsize'), ('famrel', 'Pstatus'), ('famrel', 'Medu'), ('famrel', 'Fedu'), ('famrel', 'traveltime'), ('famrel', 'studytime'), ('famrel', 'failures'), ('famrel', 'schoolsup'), ('famrel', 'famsup'), ('famrel', 'paid'), ('famrel', 'activities'), ('famrel', 'nursery'), ('famrel', 'higher'), ('famrel', 'internet'), ('famrel', 'romantic'), ('famrel', 'freetime'), ('famrel', 'goout'), ('famrel', 'Dalc'), ('famrel', 'Walc'), ('famrel', 'health'), ('famrel', 'absences'), ('famrel', 'G1'), ('famrel', 'G2'), ('famrel', 'G3'), ('freetime', 'address'), ('freetime', 'famsize'), ('freetime', 'Pstatus'), ('freetime', 'Medu'), ('freetime', 'Fedu'), ('freetime', 'traveltime'), ('freetime', 'studytime'), ('freetime', 'failures'), ('freetime', 'schoolsup'), ('freetime', 'famsup'), ('freetime', 'paid'), ('freetime', 'activities'), ('freetime', 'nursery'), ('freetime', 'higher'), ('freetime', 'internet'), ('freetime', 'romantic'), ('freetime', 'famrel'), ('freetime', 'goout'), ('freetime', 'Dalc'), ('freetime', 'Walc'), ('freetime', 'health'), ('freetime', 'absences'), ('freetime', 'G1'), ('freetime', 'G2'), ('freetime', 'G3'), ('goout', 'address'), ('goout', 'famsize'), ('goout', 'Pstatus'), ('goout', 'Medu'), ('goout', 'Fedu'), ('goout', 'traveltime'), ('goout', 'studytime'), ('goout', 'failures'), ('goout', 'schoolsup'), ('goout', 'famsup'), ('goout', 'paid'), ('goout', 'activities'), ('goout', 'nursery'), ('goout', 'higher'), ('goout', 'internet'), ('goout', 'romantic'), ('goout', 'famrel'), ('goout', 'freetime'), ('goout', 'Dalc'), ('goout', 'Walc'), ('goout', 'health'), ('goout', 'absences'), ('goout', 'G1'), ('goout', 'G2'), ('goout', 'G3'), ('Dalc', 'address'), ('Dalc', 'famsize'), ('Dalc', 'Pstatus'), ('Dalc', 'Medu'), ('Dalc', 'Fedu'), ('Dalc', 'traveltime'), ('Dalc', 'studytime'), ('Dalc', 'failures'), ('Dalc', 'schoolsup'), ('Dalc', 'famsup'), ('Dalc', 'paid'), ('Dalc', 'activities'), ('Dalc', 'nursery'), ('Dalc', 'higher'), ('Dalc', 'internet'), ('Dalc', 'romantic'), ('Dalc', 'famrel'), ('Dalc', 'freetime'), ('Dalc', 'goout'), ('Dalc', 'Walc'), ('Dalc', 'health'), ('Dalc', 'absences'), ('Dalc', 'G1'), ('Dalc', 'G2'), ('Dalc', 'G3'), ('Walc', 'address'), ('Walc', 'famsize'), ('Walc', 'Pstatus'), ('Walc', 'Medu'), ('Walc', 'Fedu'), ('Walc', 'traveltime'), ('Walc', 'studytime'), ('Walc', 'failures'), ('Walc', 'schoolsup'), ('Walc', 'famsup'), ('Walc', 'paid'), ('Walc', 'activities'), ('Walc', 'nursery'), ('Walc', 'higher'), ('Walc', 'internet'), ('Walc', 'romantic'), ('Walc', 'famrel'), ('Walc', 'freetime'), ('Walc', 'goout'), ('Walc', 'Dalc'), ('Walc', 'health'), ('Walc', 'absences'), ('Walc', 'G1'), ('Walc', 'G2'), ('Walc', 'G3'), ('health', 'address'), ('health', 'famsize'), ('health', 'Pstatus'), ('health', 'Medu'), ('health', 'Fedu'), ('health', 'traveltime'), ('health', 'studytime'), ('health', 'failures'), ('health', 'schoolsup'), ('health', 'famsup'), ('health', 'paid'), ('health', 'activities'), ('health', 'nursery'), ('health', 'higher'), ('health', 'internet'), ('health', 'romantic'), ('health', 'famrel'), ('health', 'freetime'), ('health', 'goout'), ('health', 'Dalc'), ('health', 'Walc'), ('health', 'absences'), ('health', 'G1'), ('health', 'G2'), ('health', 'G3'), ('absences', 'address'), ('absences', 'famsize'), ('absences', 'Pstatus'), ('absences', 'Medu'), ('absences', 'Fedu'), ('absences', 'traveltime'), ('absences', 'studytime'), ('absences', 'failures'), ('absences', 'schoolsup'), ('absences', 'famsup'), ('absences', 'paid'), ('absences', 'activities'), ('absences', 'nursery'), ('absences', 'higher'), ('absences', 'internet'), ('absences', 'romantic'), ('absences', 'famrel'), ('absences', 'freetime'), ('absences', 'goout'), ('absences', 'Dalc'), ('absences', 'Walc'), ('absences', 'health'), ('absences', 'G1'), ('absences', 'G2'), ('absences', 'G3'), ('G1', 'address'), ('G1', 'famsize'), ('G1', 'Pstatus'), ('G1', 'Medu'), ('G1', 'Fedu'), ('G1', 'traveltime'), ('G1', 'studytime'), ('G1', 'failures'), ('G1', 'schoolsup'), ('G1', 'famsup'), ('G1', 'paid'), ('G1', 'activities'), ('G1', 'nursery'), ('G1', 'higher'), ('G1', 'internet'), ('G1', 'romantic'), ('G1', 'famrel'), ('G1', 'freetime'), ('G1', 'goout'), ('G1', 'Dalc'), ('G1', 'Walc'), ('G1', 'health'), ('G1', 'absences'), ('G1', 'G2'), ('G1', 'G3'), ('G2', 'address'), ('G2', 'famsize'), ('G2', 'Pstatus'), ('G2', 'Medu'), ('G2', 'Fedu'), ('G2', 'traveltime'), ('G2', 'studytime'), ('G2', 'failures'), ('G2', 'schoolsup'), ('G2', 'famsup'), ('G2', 'paid'), ('G2', 'activities'), ('G2', 'nursery'), ('G2', 'higher'), ('G2', 'internet'), ('G2', 'romantic'), ('G2', 'famrel'), ('G2', 'freetime'), ('G2', 'goout'), ('G2', 'Dalc'), ('G2', 'Walc'), ('G2', 'health'), ('G2', 'absences'), ('G2', 'G1'), ('G2', 'G3'), ('G3', 'address'), ('G3', 'famsize'), ('G3', 'Pstatus'), ('G3', 'Medu'), ('G3', 'Fedu'), ('G3', 'traveltime'), ('G3', 'studytime'), ('G3', 'failures'), ('G3', 'schoolsup'), ('G3', 'famsup'), ('G3', 'paid'), ('G3', 'activities'), ('G3', 'nursery'), ('G3', 'higher'), ('G3', 'internet'), ('G3', 'romantic'), ('G3', 'famrel'), ('G3', 'freetime'), ('G3', 'goout'), ('G3', 'Dalc'), ('G3', 'Walc'), ('G3', 'health'), ('G3', 'absences'), ('G3', 'G1'), ('G3', 'G2')])




```python
structureModelPruned.edges
```




    OutEdgeView([('address', 'absences'), ('address', 'G1'), ('Pstatus', 'famrel'), ('Pstatus', 'absences'), ('Pstatus', 'G1'), ('studytime', 'G1'), ('failures', 'absences'), ('schoolsup', 'G1'), ('paid', 'absences'), ('higher', 'Medu'), ('higher', 'G1'), ('internet', 'absences'), ('Dalc', 'Walc'), ('G1', 'G2'), ('G2', 'G3')])




```python
structureModelLearned.in_degree
```




    InDegreeView({'address': 25, 'famsize': 25, 'Pstatus': 25, 'Medu': 25, 'Fedu': 25, 'traveltime': 25, 'studytime': 25, 'failures': 25, 'schoolsup': 25, 'famsup': 25, 'paid': 25, 'activities': 25, 'nursery': 25, 'higher': 25, 'internet': 25, 'romantic': 25, 'famrel': 25, 'freetime': 25, 'goout': 25, 'Dalc': 25, 'Walc': 25, 'health': 25, 'absences': 25, 'G1': 25, 'G2': 25, 'G3': 25})




```python
structureModelPruned.in_degree
```




    InDegreeView({'address': 0, 'famsize': 0, 'Pstatus': 0, 'Medu': 1, 'Fedu': 0, 'traveltime': 0, 'studytime': 0, 'failures': 0, 'schoolsup': 0, 'famsup': 0, 'paid': 0, 'activities': 0, 'nursery': 0, 'higher': 0, 'internet': 0, 'romantic': 0, 'famrel': 1, 'freetime': 0, 'goout': 0, 'Dalc': 0, 'Walc': 1, 'health': 0, 'absences': 5, 'G1': 5, 'G2': 1, 'G3': 1})




```python
structureModelLearned.in_edges
```




    InEdgeView([('famsize', 'address'), ('Pstatus', 'address'), ('Medu', 'address'), ('Fedu', 'address'), ('traveltime', 'address'), ('studytime', 'address'), ('failures', 'address'), ('schoolsup', 'address'), ('famsup', 'address'), ('paid', 'address'), ('activities', 'address'), ('nursery', 'address'), ('higher', 'address'), ('internet', 'address'), ('romantic', 'address'), ('famrel', 'address'), ('freetime', 'address'), ('goout', 'address'), ('Dalc', 'address'), ('Walc', 'address'), ('health', 'address'), ('absences', 'address'), ('G1', 'address'), ('G2', 'address'), ('G3', 'address'), ('address', 'famsize'), ('Pstatus', 'famsize'), ('Medu', 'famsize'), ('Fedu', 'famsize'), ('traveltime', 'famsize'), ('studytime', 'famsize'), ('failures', 'famsize'), ('schoolsup', 'famsize'), ('famsup', 'famsize'), ('paid', 'famsize'), ('activities', 'famsize'), ('nursery', 'famsize'), ('higher', 'famsize'), ('internet', 'famsize'), ('romantic', 'famsize'), ('famrel', 'famsize'), ('freetime', 'famsize'), ('goout', 'famsize'), ('Dalc', 'famsize'), ('Walc', 'famsize'), ('health', 'famsize'), ('absences', 'famsize'), ('G1', 'famsize'), ('G2', 'famsize'), ('G3', 'famsize'), ('address', 'Pstatus'), ('famsize', 'Pstatus'), ('Medu', 'Pstatus'), ('Fedu', 'Pstatus'), ('traveltime', 'Pstatus'), ('studytime', 'Pstatus'), ('failures', 'Pstatus'), ('schoolsup', 'Pstatus'), ('famsup', 'Pstatus'), ('paid', 'Pstatus'), ('activities', 'Pstatus'), ('nursery', 'Pstatus'), ('higher', 'Pstatus'), ('internet', 'Pstatus'), ('romantic', 'Pstatus'), ('famrel', 'Pstatus'), ('freetime', 'Pstatus'), ('goout', 'Pstatus'), ('Dalc', 'Pstatus'), ('Walc', 'Pstatus'), ('health', 'Pstatus'), ('absences', 'Pstatus'), ('G1', 'Pstatus'), ('G2', 'Pstatus'), ('G3', 'Pstatus'), ('address', 'Medu'), ('famsize', 'Medu'), ('Pstatus', 'Medu'), ('Fedu', 'Medu'), ('traveltime', 'Medu'), ('studytime', 'Medu'), ('failures', 'Medu'), ('schoolsup', 'Medu'), ('famsup', 'Medu'), ('paid', 'Medu'), ('activities', 'Medu'), ('nursery', 'Medu'), ('higher', 'Medu'), ('internet', 'Medu'), ('romantic', 'Medu'), ('famrel', 'Medu'), ('freetime', 'Medu'), ('goout', 'Medu'), ('Dalc', 'Medu'), ('Walc', 'Medu'), ('health', 'Medu'), ('absences', 'Medu'), ('G1', 'Medu'), ('G2', 'Medu'), ('G3', 'Medu'), ('address', 'Fedu'), ('famsize', 'Fedu'), ('Pstatus', 'Fedu'), ('Medu', 'Fedu'), ('traveltime', 'Fedu'), ('studytime', 'Fedu'), ('failures', 'Fedu'), ('schoolsup', 'Fedu'), ('famsup', 'Fedu'), ('paid', 'Fedu'), ('activities', 'Fedu'), ('nursery', 'Fedu'), ('higher', 'Fedu'), ('internet', 'Fedu'), ('romantic', 'Fedu'), ('famrel', 'Fedu'), ('freetime', 'Fedu'), ('goout', 'Fedu'), ('Dalc', 'Fedu'), ('Walc', 'Fedu'), ('health', 'Fedu'), ('absences', 'Fedu'), ('G1', 'Fedu'), ('G2', 'Fedu'), ('G3', 'Fedu'), ('address', 'traveltime'), ('famsize', 'traveltime'), ('Pstatus', 'traveltime'), ('Medu', 'traveltime'), ('Fedu', 'traveltime'), ('studytime', 'traveltime'), ('failures', 'traveltime'), ('schoolsup', 'traveltime'), ('famsup', 'traveltime'), ('paid', 'traveltime'), ('activities', 'traveltime'), ('nursery', 'traveltime'), ('higher', 'traveltime'), ('internet', 'traveltime'), ('romantic', 'traveltime'), ('famrel', 'traveltime'), ('freetime', 'traveltime'), ('goout', 'traveltime'), ('Dalc', 'traveltime'), ('Walc', 'traveltime'), ('health', 'traveltime'), ('absences', 'traveltime'), ('G1', 'traveltime'), ('G2', 'traveltime'), ('G3', 'traveltime'), ('address', 'studytime'), ('famsize', 'studytime'), ('Pstatus', 'studytime'), ('Medu', 'studytime'), ('Fedu', 'studytime'), ('traveltime', 'studytime'), ('failures', 'studytime'), ('schoolsup', 'studytime'), ('famsup', 'studytime'), ('paid', 'studytime'), ('activities', 'studytime'), ('nursery', 'studytime'), ('higher', 'studytime'), ('internet', 'studytime'), ('romantic', 'studytime'), ('famrel', 'studytime'), ('freetime', 'studytime'), ('goout', 'studytime'), ('Dalc', 'studytime'), ('Walc', 'studytime'), ('health', 'studytime'), ('absences', 'studytime'), ('G1', 'studytime'), ('G2', 'studytime'), ('G3', 'studytime'), ('address', 'failures'), ('famsize', 'failures'), ('Pstatus', 'failures'), ('Medu', 'failures'), ('Fedu', 'failures'), ('traveltime', 'failures'), ('studytime', 'failures'), ('schoolsup', 'failures'), ('famsup', 'failures'), ('paid', 'failures'), ('activities', 'failures'), ('nursery', 'failures'), ('higher', 'failures'), ('internet', 'failures'), ('romantic', 'failures'), ('famrel', 'failures'), ('freetime', 'failures'), ('goout', 'failures'), ('Dalc', 'failures'), ('Walc', 'failures'), ('health', 'failures'), ('absences', 'failures'), ('G1', 'failures'), ('G2', 'failures'), ('G3', 'failures'), ('address', 'schoolsup'), ('famsize', 'schoolsup'), ('Pstatus', 'schoolsup'), ('Medu', 'schoolsup'), ('Fedu', 'schoolsup'), ('traveltime', 'schoolsup'), ('studytime', 'schoolsup'), ('failures', 'schoolsup'), ('famsup', 'schoolsup'), ('paid', 'schoolsup'), ('activities', 'schoolsup'), ('nursery', 'schoolsup'), ('higher', 'schoolsup'), ('internet', 'schoolsup'), ('romantic', 'schoolsup'), ('famrel', 'schoolsup'), ('freetime', 'schoolsup'), ('goout', 'schoolsup'), ('Dalc', 'schoolsup'), ('Walc', 'schoolsup'), ('health', 'schoolsup'), ('absences', 'schoolsup'), ('G1', 'schoolsup'), ('G2', 'schoolsup'), ('G3', 'schoolsup'), ('address', 'famsup'), ('famsize', 'famsup'), ('Pstatus', 'famsup'), ('Medu', 'famsup'), ('Fedu', 'famsup'), ('traveltime', 'famsup'), ('studytime', 'famsup'), ('failures', 'famsup'), ('schoolsup', 'famsup'), ('paid', 'famsup'), ('activities', 'famsup'), ('nursery', 'famsup'), ('higher', 'famsup'), ('internet', 'famsup'), ('romantic', 'famsup'), ('famrel', 'famsup'), ('freetime', 'famsup'), ('goout', 'famsup'), ('Dalc', 'famsup'), ('Walc', 'famsup'), ('health', 'famsup'), ('absences', 'famsup'), ('G1', 'famsup'), ('G2', 'famsup'), ('G3', 'famsup'), ('address', 'paid'), ('famsize', 'paid'), ('Pstatus', 'paid'), ('Medu', 'paid'), ('Fedu', 'paid'), ('traveltime', 'paid'), ('studytime', 'paid'), ('failures', 'paid'), ('schoolsup', 'paid'), ('famsup', 'paid'), ('activities', 'paid'), ('nursery', 'paid'), ('higher', 'paid'), ('internet', 'paid'), ('romantic', 'paid'), ('famrel', 'paid'), ('freetime', 'paid'), ('goout', 'paid'), ('Dalc', 'paid'), ('Walc', 'paid'), ('health', 'paid'), ('absences', 'paid'), ('G1', 'paid'), ('G2', 'paid'), ('G3', 'paid'), ('address', 'activities'), ('famsize', 'activities'), ('Pstatus', 'activities'), ('Medu', 'activities'), ('Fedu', 'activities'), ('traveltime', 'activities'), ('studytime', 'activities'), ('failures', 'activities'), ('schoolsup', 'activities'), ('famsup', 'activities'), ('paid', 'activities'), ('nursery', 'activities'), ('higher', 'activities'), ('internet', 'activities'), ('romantic', 'activities'), ('famrel', 'activities'), ('freetime', 'activities'), ('goout', 'activities'), ('Dalc', 'activities'), ('Walc', 'activities'), ('health', 'activities'), ('absences', 'activities'), ('G1', 'activities'), ('G2', 'activities'), ('G3', 'activities'), ('address', 'nursery'), ('famsize', 'nursery'), ('Pstatus', 'nursery'), ('Medu', 'nursery'), ('Fedu', 'nursery'), ('traveltime', 'nursery'), ('studytime', 'nursery'), ('failures', 'nursery'), ('schoolsup', 'nursery'), ('famsup', 'nursery'), ('paid', 'nursery'), ('activities', 'nursery'), ('higher', 'nursery'), ('internet', 'nursery'), ('romantic', 'nursery'), ('famrel', 'nursery'), ('freetime', 'nursery'), ('goout', 'nursery'), ('Dalc', 'nursery'), ('Walc', 'nursery'), ('health', 'nursery'), ('absences', 'nursery'), ('G1', 'nursery'), ('G2', 'nursery'), ('G3', 'nursery'), ('address', 'higher'), ('famsize', 'higher'), ('Pstatus', 'higher'), ('Medu', 'higher'), ('Fedu', 'higher'), ('traveltime', 'higher'), ('studytime', 'higher'), ('failures', 'higher'), ('schoolsup', 'higher'), ('famsup', 'higher'), ('paid', 'higher'), ('activities', 'higher'), ('nursery', 'higher'), ('internet', 'higher'), ('romantic', 'higher'), ('famrel', 'higher'), ('freetime', 'higher'), ('goout', 'higher'), ('Dalc', 'higher'), ('Walc', 'higher'), ('health', 'higher'), ('absences', 'higher'), ('G1', 'higher'), ('G2', 'higher'), ('G3', 'higher'), ('address', 'internet'), ('famsize', 'internet'), ('Pstatus', 'internet'), ('Medu', 'internet'), ('Fedu', 'internet'), ('traveltime', 'internet'), ('studytime', 'internet'), ('failures', 'internet'), ('schoolsup', 'internet'), ('famsup', 'internet'), ('paid', 'internet'), ('activities', 'internet'), ('nursery', 'internet'), ('higher', 'internet'), ('romantic', 'internet'), ('famrel', 'internet'), ('freetime', 'internet'), ('goout', 'internet'), ('Dalc', 'internet'), ('Walc', 'internet'), ('health', 'internet'), ('absences', 'internet'), ('G1', 'internet'), ('G2', 'internet'), ('G3', 'internet'), ('address', 'romantic'), ('famsize', 'romantic'), ('Pstatus', 'romantic'), ('Medu', 'romantic'), ('Fedu', 'romantic'), ('traveltime', 'romantic'), ('studytime', 'romantic'), ('failures', 'romantic'), ('schoolsup', 'romantic'), ('famsup', 'romantic'), ('paid', 'romantic'), ('activities', 'romantic'), ('nursery', 'romantic'), ('higher', 'romantic'), ('internet', 'romantic'), ('famrel', 'romantic'), ('freetime', 'romantic'), ('goout', 'romantic'), ('Dalc', 'romantic'), ('Walc', 'romantic'), ('health', 'romantic'), ('absences', 'romantic'), ('G1', 'romantic'), ('G2', 'romantic'), ('G3', 'romantic'), ('address', 'famrel'), ('famsize', 'famrel'), ('Pstatus', 'famrel'), ('Medu', 'famrel'), ('Fedu', 'famrel'), ('traveltime', 'famrel'), ('studytime', 'famrel'), ('failures', 'famrel'), ('schoolsup', 'famrel'), ('famsup', 'famrel'), ('paid', 'famrel'), ('activities', 'famrel'), ('nursery', 'famrel'), ('higher', 'famrel'), ('internet', 'famrel'), ('romantic', 'famrel'), ('freetime', 'famrel'), ('goout', 'famrel'), ('Dalc', 'famrel'), ('Walc', 'famrel'), ('health', 'famrel'), ('absences', 'famrel'), ('G1', 'famrel'), ('G2', 'famrel'), ('G3', 'famrel'), ('address', 'freetime'), ('famsize', 'freetime'), ('Pstatus', 'freetime'), ('Medu', 'freetime'), ('Fedu', 'freetime'), ('traveltime', 'freetime'), ('studytime', 'freetime'), ('failures', 'freetime'), ('schoolsup', 'freetime'), ('famsup', 'freetime'), ('paid', 'freetime'), ('activities', 'freetime'), ('nursery', 'freetime'), ('higher', 'freetime'), ('internet', 'freetime'), ('romantic', 'freetime'), ('famrel', 'freetime'), ('goout', 'freetime'), ('Dalc', 'freetime'), ('Walc', 'freetime'), ('health', 'freetime'), ('absences', 'freetime'), ('G1', 'freetime'), ('G2', 'freetime'), ('G3', 'freetime'), ('address', 'goout'), ('famsize', 'goout'), ('Pstatus', 'goout'), ('Medu', 'goout'), ('Fedu', 'goout'), ('traveltime', 'goout'), ('studytime', 'goout'), ('failures', 'goout'), ('schoolsup', 'goout'), ('famsup', 'goout'), ('paid', 'goout'), ('activities', 'goout'), ('nursery', 'goout'), ('higher', 'goout'), ('internet', 'goout'), ('romantic', 'goout'), ('famrel', 'goout'), ('freetime', 'goout'), ('Dalc', 'goout'), ('Walc', 'goout'), ('health', 'goout'), ('absences', 'goout'), ('G1', 'goout'), ('G2', 'goout'), ('G3', 'goout'), ('address', 'Dalc'), ('famsize', 'Dalc'), ('Pstatus', 'Dalc'), ('Medu', 'Dalc'), ('Fedu', 'Dalc'), ('traveltime', 'Dalc'), ('studytime', 'Dalc'), ('failures', 'Dalc'), ('schoolsup', 'Dalc'), ('famsup', 'Dalc'), ('paid', 'Dalc'), ('activities', 'Dalc'), ('nursery', 'Dalc'), ('higher', 'Dalc'), ('internet', 'Dalc'), ('romantic', 'Dalc'), ('famrel', 'Dalc'), ('freetime', 'Dalc'), ('goout', 'Dalc'), ('Walc', 'Dalc'), ('health', 'Dalc'), ('absences', 'Dalc'), ('G1', 'Dalc'), ('G2', 'Dalc'), ('G3', 'Dalc'), ('address', 'Walc'), ('famsize', 'Walc'), ('Pstatus', 'Walc'), ('Medu', 'Walc'), ('Fedu', 'Walc'), ('traveltime', 'Walc'), ('studytime', 'Walc'), ('failures', 'Walc'), ('schoolsup', 'Walc'), ('famsup', 'Walc'), ('paid', 'Walc'), ('activities', 'Walc'), ('nursery', 'Walc'), ('higher', 'Walc'), ('internet', 'Walc'), ('romantic', 'Walc'), ('famrel', 'Walc'), ('freetime', 'Walc'), ('goout', 'Walc'), ('Dalc', 'Walc'), ('health', 'Walc'), ('absences', 'Walc'), ('G1', 'Walc'), ('G2', 'Walc'), ('G3', 'Walc'), ('address', 'health'), ('famsize', 'health'), ('Pstatus', 'health'), ('Medu', 'health'), ('Fedu', 'health'), ('traveltime', 'health'), ('studytime', 'health'), ('failures', 'health'), ('schoolsup', 'health'), ('famsup', 'health'), ('paid', 'health'), ('activities', 'health'), ('nursery', 'health'), ('higher', 'health'), ('internet', 'health'), ('romantic', 'health'), ('famrel', 'health'), ('freetime', 'health'), ('goout', 'health'), ('Dalc', 'health'), ('Walc', 'health'), ('absences', 'health'), ('G1', 'health'), ('G2', 'health'), ('G3', 'health'), ('address', 'absences'), ('famsize', 'absences'), ('Pstatus', 'absences'), ('Medu', 'absences'), ('Fedu', 'absences'), ('traveltime', 'absences'), ('studytime', 'absences'), ('failures', 'absences'), ('schoolsup', 'absences'), ('famsup', 'absences'), ('paid', 'absences'), ('activities', 'absences'), ('nursery', 'absences'), ('higher', 'absences'), ('internet', 'absences'), ('romantic', 'absences'), ('famrel', 'absences'), ('freetime', 'absences'), ('goout', 'absences'), ('Dalc', 'absences'), ('Walc', 'absences'), ('health', 'absences'), ('G1', 'absences'), ('G2', 'absences'), ('G3', 'absences'), ('address', 'G1'), ('famsize', 'G1'), ('Pstatus', 'G1'), ('Medu', 'G1'), ('Fedu', 'G1'), ('traveltime', 'G1'), ('studytime', 'G1'), ('failures', 'G1'), ('schoolsup', 'G1'), ('famsup', 'G1'), ('paid', 'G1'), ('activities', 'G1'), ('nursery', 'G1'), ('higher', 'G1'), ('internet', 'G1'), ('romantic', 'G1'), ('famrel', 'G1'), ('freetime', 'G1'), ('goout', 'G1'), ('Dalc', 'G1'), ('Walc', 'G1'), ('health', 'G1'), ('absences', 'G1'), ('G2', 'G1'), ('G3', 'G1'), ('address', 'G2'), ('famsize', 'G2'), ('Pstatus', 'G2'), ('Medu', 'G2'), ('Fedu', 'G2'), ('traveltime', 'G2'), ('studytime', 'G2'), ('failures', 'G2'), ('schoolsup', 'G2'), ('famsup', 'G2'), ('paid', 'G2'), ('activities', 'G2'), ('nursery', 'G2'), ('higher', 'G2'), ('internet', 'G2'), ('romantic', 'G2'), ('famrel', 'G2'), ('freetime', 'G2'), ('goout', 'G2'), ('Dalc', 'G2'), ('Walc', 'G2'), ('health', 'G2'), ('absences', 'G2'), ('G1', 'G2'), ('G3', 'G2'), ('address', 'G3'), ('famsize', 'G3'), ('Pstatus', 'G3'), ('Medu', 'G3'), ('Fedu', 'G3'), ('traveltime', 'G3'), ('studytime', 'G3'), ('failures', 'G3'), ('schoolsup', 'G3'), ('famsup', 'G3'), ('paid', 'G3'), ('activities', 'G3'), ('nursery', 'G3'), ('higher', 'G3'), ('internet', 'G3'), ('romantic', 'G3'), ('famrel', 'G3'), ('freetime', 'G3'), ('goout', 'G3'), ('Dalc', 'G3'), ('Walc', 'G3'), ('health', 'G3'), ('absences', 'G3'), ('G1', 'G3'), ('G2', 'G3')])




```python
structureModelPruned.in_edges
```




    InEdgeView([('higher', 'Medu'), ('Pstatus', 'famrel'), ('Dalc', 'Walc'), ('address', 'absences'), ('Pstatus', 'absences'), ('failures', 'absences'), ('paid', 'absences'), ('internet', 'absences'), ('address', 'G1'), ('Pstatus', 'G1'), ('studytime', 'G1'), ('schoolsup', 'G1'), ('higher', 'G1'), ('G1', 'G2'), ('G2', 'G3')])




```python
structureModelLearned.number_of_nodes()
```




    26




```python
structureModelPruned.number_of_nodes()
```




    26




```python
structureModelLearned.node
```




    NodeView(('address', 'famsize', 'Pstatus', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2', 'G3'))




```python
structureModelPruned.node
```




    NodeView(('address', 'famsize', 'Pstatus', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2', 'G3'))




```python
assert structureModelLearned.node == structureModelLearned.nodes

structureModelLearned.nodes
```




    NodeView(('address', 'famsize', 'Pstatus', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2', 'G3'))




```python
assert structureModelPruned.node == structureModelPruned.nodes

structureModelPruned.nodes
```




    NodeView(('address', 'famsize', 'Pstatus', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2', 'G3'))




```python
structureModelLearned.out_degree
```




    OutDegreeView({'address': 25, 'famsize': 25, 'Pstatus': 25, 'Medu': 25, 'Fedu': 25, 'traveltime': 25, 'studytime': 25, 'failures': 25, 'schoolsup': 25, 'famsup': 25, 'paid': 25, 'activities': 25, 'nursery': 25, 'higher': 25, 'internet': 25, 'romantic': 25, 'famrel': 25, 'freetime': 25, 'goout': 25, 'Dalc': 25, 'Walc': 25, 'health': 25, 'absences': 25, 'G1': 25, 'G2': 25, 'G3': 25})




```python
structureModelPruned.out_degree
```




    OutDegreeView({'address': 2, 'famsize': 0, 'Pstatus': 3, 'Medu': 0, 'Fedu': 0, 'traveltime': 0, 'studytime': 1, 'failures': 1, 'schoolsup': 1, 'famsup': 0, 'paid': 1, 'activities': 0, 'nursery': 0, 'higher': 2, 'internet': 1, 'romantic': 0, 'famrel': 0, 'freetime': 0, 'goout': 0, 'Dalc': 1, 'Walc': 0, 'health': 0, 'absences': 0, 'G1': 1, 'G2': 1, 'G3': 0})




```python
structureModelLearned.out_edges
```




    OutEdgeView([('address', 'famsize'), ('address', 'Pstatus'), ('address', 'Medu'), ('address', 'Fedu'), ('address', 'traveltime'), ('address', 'studytime'), ('address', 'failures'), ('address', 'schoolsup'), ('address', 'famsup'), ('address', 'paid'), ('address', 'activities'), ('address', 'nursery'), ('address', 'higher'), ('address', 'internet'), ('address', 'romantic'), ('address', 'famrel'), ('address', 'freetime'), ('address', 'goout'), ('address', 'Dalc'), ('address', 'Walc'), ('address', 'health'), ('address', 'absences'), ('address', 'G1'), ('address', 'G2'), ('address', 'G3'), ('famsize', 'address'), ('famsize', 'Pstatus'), ('famsize', 'Medu'), ('famsize', 'Fedu'), ('famsize', 'traveltime'), ('famsize', 'studytime'), ('famsize', 'failures'), ('famsize', 'schoolsup'), ('famsize', 'famsup'), ('famsize', 'paid'), ('famsize', 'activities'), ('famsize', 'nursery'), ('famsize', 'higher'), ('famsize', 'internet'), ('famsize', 'romantic'), ('famsize', 'famrel'), ('famsize', 'freetime'), ('famsize', 'goout'), ('famsize', 'Dalc'), ('famsize', 'Walc'), ('famsize', 'health'), ('famsize', 'absences'), ('famsize', 'G1'), ('famsize', 'G2'), ('famsize', 'G3'), ('Pstatus', 'address'), ('Pstatus', 'famsize'), ('Pstatus', 'Medu'), ('Pstatus', 'Fedu'), ('Pstatus', 'traveltime'), ('Pstatus', 'studytime'), ('Pstatus', 'failures'), ('Pstatus', 'schoolsup'), ('Pstatus', 'famsup'), ('Pstatus', 'paid'), ('Pstatus', 'activities'), ('Pstatus', 'nursery'), ('Pstatus', 'higher'), ('Pstatus', 'internet'), ('Pstatus', 'romantic'), ('Pstatus', 'famrel'), ('Pstatus', 'freetime'), ('Pstatus', 'goout'), ('Pstatus', 'Dalc'), ('Pstatus', 'Walc'), ('Pstatus', 'health'), ('Pstatus', 'absences'), ('Pstatus', 'G1'), ('Pstatus', 'G2'), ('Pstatus', 'G3'), ('Medu', 'address'), ('Medu', 'famsize'), ('Medu', 'Pstatus'), ('Medu', 'Fedu'), ('Medu', 'traveltime'), ('Medu', 'studytime'), ('Medu', 'failures'), ('Medu', 'schoolsup'), ('Medu', 'famsup'), ('Medu', 'paid'), ('Medu', 'activities'), ('Medu', 'nursery'), ('Medu', 'higher'), ('Medu', 'internet'), ('Medu', 'romantic'), ('Medu', 'famrel'), ('Medu', 'freetime'), ('Medu', 'goout'), ('Medu', 'Dalc'), ('Medu', 'Walc'), ('Medu', 'health'), ('Medu', 'absences'), ('Medu', 'G1'), ('Medu', 'G2'), ('Medu', 'G3'), ('Fedu', 'address'), ('Fedu', 'famsize'), ('Fedu', 'Pstatus'), ('Fedu', 'Medu'), ('Fedu', 'traveltime'), ('Fedu', 'studytime'), ('Fedu', 'failures'), ('Fedu', 'schoolsup'), ('Fedu', 'famsup'), ('Fedu', 'paid'), ('Fedu', 'activities'), ('Fedu', 'nursery'), ('Fedu', 'higher'), ('Fedu', 'internet'), ('Fedu', 'romantic'), ('Fedu', 'famrel'), ('Fedu', 'freetime'), ('Fedu', 'goout'), ('Fedu', 'Dalc'), ('Fedu', 'Walc'), ('Fedu', 'health'), ('Fedu', 'absences'), ('Fedu', 'G1'), ('Fedu', 'G2'), ('Fedu', 'G3'), ('traveltime', 'address'), ('traveltime', 'famsize'), ('traveltime', 'Pstatus'), ('traveltime', 'Medu'), ('traveltime', 'Fedu'), ('traveltime', 'studytime'), ('traveltime', 'failures'), ('traveltime', 'schoolsup'), ('traveltime', 'famsup'), ('traveltime', 'paid'), ('traveltime', 'activities'), ('traveltime', 'nursery'), ('traveltime', 'higher'), ('traveltime', 'internet'), ('traveltime', 'romantic'), ('traveltime', 'famrel'), ('traveltime', 'freetime'), ('traveltime', 'goout'), ('traveltime', 'Dalc'), ('traveltime', 'Walc'), ('traveltime', 'health'), ('traveltime', 'absences'), ('traveltime', 'G1'), ('traveltime', 'G2'), ('traveltime', 'G3'), ('studytime', 'address'), ('studytime', 'famsize'), ('studytime', 'Pstatus'), ('studytime', 'Medu'), ('studytime', 'Fedu'), ('studytime', 'traveltime'), ('studytime', 'failures'), ('studytime', 'schoolsup'), ('studytime', 'famsup'), ('studytime', 'paid'), ('studytime', 'activities'), ('studytime', 'nursery'), ('studytime', 'higher'), ('studytime', 'internet'), ('studytime', 'romantic'), ('studytime', 'famrel'), ('studytime', 'freetime'), ('studytime', 'goout'), ('studytime', 'Dalc'), ('studytime', 'Walc'), ('studytime', 'health'), ('studytime', 'absences'), ('studytime', 'G1'), ('studytime', 'G2'), ('studytime', 'G3'), ('failures', 'address'), ('failures', 'famsize'), ('failures', 'Pstatus'), ('failures', 'Medu'), ('failures', 'Fedu'), ('failures', 'traveltime'), ('failures', 'studytime'), ('failures', 'schoolsup'), ('failures', 'famsup'), ('failures', 'paid'), ('failures', 'activities'), ('failures', 'nursery'), ('failures', 'higher'), ('failures', 'internet'), ('failures', 'romantic'), ('failures', 'famrel'), ('failures', 'freetime'), ('failures', 'goout'), ('failures', 'Dalc'), ('failures', 'Walc'), ('failures', 'health'), ('failures', 'absences'), ('failures', 'G1'), ('failures', 'G2'), ('failures', 'G3'), ('schoolsup', 'address'), ('schoolsup', 'famsize'), ('schoolsup', 'Pstatus'), ('schoolsup', 'Medu'), ('schoolsup', 'Fedu'), ('schoolsup', 'traveltime'), ('schoolsup', 'studytime'), ('schoolsup', 'failures'), ('schoolsup', 'famsup'), ('schoolsup', 'paid'), ('schoolsup', 'activities'), ('schoolsup', 'nursery'), ('schoolsup', 'higher'), ('schoolsup', 'internet'), ('schoolsup', 'romantic'), ('schoolsup', 'famrel'), ('schoolsup', 'freetime'), ('schoolsup', 'goout'), ('schoolsup', 'Dalc'), ('schoolsup', 'Walc'), ('schoolsup', 'health'), ('schoolsup', 'absences'), ('schoolsup', 'G1'), ('schoolsup', 'G2'), ('schoolsup', 'G3'), ('famsup', 'address'), ('famsup', 'famsize'), ('famsup', 'Pstatus'), ('famsup', 'Medu'), ('famsup', 'Fedu'), ('famsup', 'traveltime'), ('famsup', 'studytime'), ('famsup', 'failures'), ('famsup', 'schoolsup'), ('famsup', 'paid'), ('famsup', 'activities'), ('famsup', 'nursery'), ('famsup', 'higher'), ('famsup', 'internet'), ('famsup', 'romantic'), ('famsup', 'famrel'), ('famsup', 'freetime'), ('famsup', 'goout'), ('famsup', 'Dalc'), ('famsup', 'Walc'), ('famsup', 'health'), ('famsup', 'absences'), ('famsup', 'G1'), ('famsup', 'G2'), ('famsup', 'G3'), ('paid', 'address'), ('paid', 'famsize'), ('paid', 'Pstatus'), ('paid', 'Medu'), ('paid', 'Fedu'), ('paid', 'traveltime'), ('paid', 'studytime'), ('paid', 'failures'), ('paid', 'schoolsup'), ('paid', 'famsup'), ('paid', 'activities'), ('paid', 'nursery'), ('paid', 'higher'), ('paid', 'internet'), ('paid', 'romantic'), ('paid', 'famrel'), ('paid', 'freetime'), ('paid', 'goout'), ('paid', 'Dalc'), ('paid', 'Walc'), ('paid', 'health'), ('paid', 'absences'), ('paid', 'G1'), ('paid', 'G2'), ('paid', 'G3'), ('activities', 'address'), ('activities', 'famsize'), ('activities', 'Pstatus'), ('activities', 'Medu'), ('activities', 'Fedu'), ('activities', 'traveltime'), ('activities', 'studytime'), ('activities', 'failures'), ('activities', 'schoolsup'), ('activities', 'famsup'), ('activities', 'paid'), ('activities', 'nursery'), ('activities', 'higher'), ('activities', 'internet'), ('activities', 'romantic'), ('activities', 'famrel'), ('activities', 'freetime'), ('activities', 'goout'), ('activities', 'Dalc'), ('activities', 'Walc'), ('activities', 'health'), ('activities', 'absences'), ('activities', 'G1'), ('activities', 'G2'), ('activities', 'G3'), ('nursery', 'address'), ('nursery', 'famsize'), ('nursery', 'Pstatus'), ('nursery', 'Medu'), ('nursery', 'Fedu'), ('nursery', 'traveltime'), ('nursery', 'studytime'), ('nursery', 'failures'), ('nursery', 'schoolsup'), ('nursery', 'famsup'), ('nursery', 'paid'), ('nursery', 'activities'), ('nursery', 'higher'), ('nursery', 'internet'), ('nursery', 'romantic'), ('nursery', 'famrel'), ('nursery', 'freetime'), ('nursery', 'goout'), ('nursery', 'Dalc'), ('nursery', 'Walc'), ('nursery', 'health'), ('nursery', 'absences'), ('nursery', 'G1'), ('nursery', 'G2'), ('nursery', 'G3'), ('higher', 'address'), ('higher', 'famsize'), ('higher', 'Pstatus'), ('higher', 'Medu'), ('higher', 'Fedu'), ('higher', 'traveltime'), ('higher', 'studytime'), ('higher', 'failures'), ('higher', 'schoolsup'), ('higher', 'famsup'), ('higher', 'paid'), ('higher', 'activities'), ('higher', 'nursery'), ('higher', 'internet'), ('higher', 'romantic'), ('higher', 'famrel'), ('higher', 'freetime'), ('higher', 'goout'), ('higher', 'Dalc'), ('higher', 'Walc'), ('higher', 'health'), ('higher', 'absences'), ('higher', 'G1'), ('higher', 'G2'), ('higher', 'G3'), ('internet', 'address'), ('internet', 'famsize'), ('internet', 'Pstatus'), ('internet', 'Medu'), ('internet', 'Fedu'), ('internet', 'traveltime'), ('internet', 'studytime'), ('internet', 'failures'), ('internet', 'schoolsup'), ('internet', 'famsup'), ('internet', 'paid'), ('internet', 'activities'), ('internet', 'nursery'), ('internet', 'higher'), ('internet', 'romantic'), ('internet', 'famrel'), ('internet', 'freetime'), ('internet', 'goout'), ('internet', 'Dalc'), ('internet', 'Walc'), ('internet', 'health'), ('internet', 'absences'), ('internet', 'G1'), ('internet', 'G2'), ('internet', 'G3'), ('romantic', 'address'), ('romantic', 'famsize'), ('romantic', 'Pstatus'), ('romantic', 'Medu'), ('romantic', 'Fedu'), ('romantic', 'traveltime'), ('romantic', 'studytime'), ('romantic', 'failures'), ('romantic', 'schoolsup'), ('romantic', 'famsup'), ('romantic', 'paid'), ('romantic', 'activities'), ('romantic', 'nursery'), ('romantic', 'higher'), ('romantic', 'internet'), ('romantic', 'famrel'), ('romantic', 'freetime'), ('romantic', 'goout'), ('romantic', 'Dalc'), ('romantic', 'Walc'), ('romantic', 'health'), ('romantic', 'absences'), ('romantic', 'G1'), ('romantic', 'G2'), ('romantic', 'G3'), ('famrel', 'address'), ('famrel', 'famsize'), ('famrel', 'Pstatus'), ('famrel', 'Medu'), ('famrel', 'Fedu'), ('famrel', 'traveltime'), ('famrel', 'studytime'), ('famrel', 'failures'), ('famrel', 'schoolsup'), ('famrel', 'famsup'), ('famrel', 'paid'), ('famrel', 'activities'), ('famrel', 'nursery'), ('famrel', 'higher'), ('famrel', 'internet'), ('famrel', 'romantic'), ('famrel', 'freetime'), ('famrel', 'goout'), ('famrel', 'Dalc'), ('famrel', 'Walc'), ('famrel', 'health'), ('famrel', 'absences'), ('famrel', 'G1'), ('famrel', 'G2'), ('famrel', 'G3'), ('freetime', 'address'), ('freetime', 'famsize'), ('freetime', 'Pstatus'), ('freetime', 'Medu'), ('freetime', 'Fedu'), ('freetime', 'traveltime'), ('freetime', 'studytime'), ('freetime', 'failures'), ('freetime', 'schoolsup'), ('freetime', 'famsup'), ('freetime', 'paid'), ('freetime', 'activities'), ('freetime', 'nursery'), ('freetime', 'higher'), ('freetime', 'internet'), ('freetime', 'romantic'), ('freetime', 'famrel'), ('freetime', 'goout'), ('freetime', 'Dalc'), ('freetime', 'Walc'), ('freetime', 'health'), ('freetime', 'absences'), ('freetime', 'G1'), ('freetime', 'G2'), ('freetime', 'G3'), ('goout', 'address'), ('goout', 'famsize'), ('goout', 'Pstatus'), ('goout', 'Medu'), ('goout', 'Fedu'), ('goout', 'traveltime'), ('goout', 'studytime'), ('goout', 'failures'), ('goout', 'schoolsup'), ('goout', 'famsup'), ('goout', 'paid'), ('goout', 'activities'), ('goout', 'nursery'), ('goout', 'higher'), ('goout', 'internet'), ('goout', 'romantic'), ('goout', 'famrel'), ('goout', 'freetime'), ('goout', 'Dalc'), ('goout', 'Walc'), ('goout', 'health'), ('goout', 'absences'), ('goout', 'G1'), ('goout', 'G2'), ('goout', 'G3'), ('Dalc', 'address'), ('Dalc', 'famsize'), ('Dalc', 'Pstatus'), ('Dalc', 'Medu'), ('Dalc', 'Fedu'), ('Dalc', 'traveltime'), ('Dalc', 'studytime'), ('Dalc', 'failures'), ('Dalc', 'schoolsup'), ('Dalc', 'famsup'), ('Dalc', 'paid'), ('Dalc', 'activities'), ('Dalc', 'nursery'), ('Dalc', 'higher'), ('Dalc', 'internet'), ('Dalc', 'romantic'), ('Dalc', 'famrel'), ('Dalc', 'freetime'), ('Dalc', 'goout'), ('Dalc', 'Walc'), ('Dalc', 'health'), ('Dalc', 'absences'), ('Dalc', 'G1'), ('Dalc', 'G2'), ('Dalc', 'G3'), ('Walc', 'address'), ('Walc', 'famsize'), ('Walc', 'Pstatus'), ('Walc', 'Medu'), ('Walc', 'Fedu'), ('Walc', 'traveltime'), ('Walc', 'studytime'), ('Walc', 'failures'), ('Walc', 'schoolsup'), ('Walc', 'famsup'), ('Walc', 'paid'), ('Walc', 'activities'), ('Walc', 'nursery'), ('Walc', 'higher'), ('Walc', 'internet'), ('Walc', 'romantic'), ('Walc', 'famrel'), ('Walc', 'freetime'), ('Walc', 'goout'), ('Walc', 'Dalc'), ('Walc', 'health'), ('Walc', 'absences'), ('Walc', 'G1'), ('Walc', 'G2'), ('Walc', 'G3'), ('health', 'address'), ('health', 'famsize'), ('health', 'Pstatus'), ('health', 'Medu'), ('health', 'Fedu'), ('health', 'traveltime'), ('health', 'studytime'), ('health', 'failures'), ('health', 'schoolsup'), ('health', 'famsup'), ('health', 'paid'), ('health', 'activities'), ('health', 'nursery'), ('health', 'higher'), ('health', 'internet'), ('health', 'romantic'), ('health', 'famrel'), ('health', 'freetime'), ('health', 'goout'), ('health', 'Dalc'), ('health', 'Walc'), ('health', 'absences'), ('health', 'G1'), ('health', 'G2'), ('health', 'G3'), ('absences', 'address'), ('absences', 'famsize'), ('absences', 'Pstatus'), ('absences', 'Medu'), ('absences', 'Fedu'), ('absences', 'traveltime'), ('absences', 'studytime'), ('absences', 'failures'), ('absences', 'schoolsup'), ('absences', 'famsup'), ('absences', 'paid'), ('absences', 'activities'), ('absences', 'nursery'), ('absences', 'higher'), ('absences', 'internet'), ('absences', 'romantic'), ('absences', 'famrel'), ('absences', 'freetime'), ('absences', 'goout'), ('absences', 'Dalc'), ('absences', 'Walc'), ('absences', 'health'), ('absences', 'G1'), ('absences', 'G2'), ('absences', 'G3'), ('G1', 'address'), ('G1', 'famsize'), ('G1', 'Pstatus'), ('G1', 'Medu'), ('G1', 'Fedu'), ('G1', 'traveltime'), ('G1', 'studytime'), ('G1', 'failures'), ('G1', 'schoolsup'), ('G1', 'famsup'), ('G1', 'paid'), ('G1', 'activities'), ('G1', 'nursery'), ('G1', 'higher'), ('G1', 'internet'), ('G1', 'romantic'), ('G1', 'famrel'), ('G1', 'freetime'), ('G1', 'goout'), ('G1', 'Dalc'), ('G1', 'Walc'), ('G1', 'health'), ('G1', 'absences'), ('G1', 'G2'), ('G1', 'G3'), ('G2', 'address'), ('G2', 'famsize'), ('G2', 'Pstatus'), ('G2', 'Medu'), ('G2', 'Fedu'), ('G2', 'traveltime'), ('G2', 'studytime'), ('G2', 'failures'), ('G2', 'schoolsup'), ('G2', 'famsup'), ('G2', 'paid'), ('G2', 'activities'), ('G2', 'nursery'), ('G2', 'higher'), ('G2', 'internet'), ('G2', 'romantic'), ('G2', 'famrel'), ('G2', 'freetime'), ('G2', 'goout'), ('G2', 'Dalc'), ('G2', 'Walc'), ('G2', 'health'), ('G2', 'absences'), ('G2', 'G1'), ('G2', 'G3'), ('G3', 'address'), ('G3', 'famsize'), ('G3', 'Pstatus'), ('G3', 'Medu'), ('G3', 'Fedu'), ('G3', 'traveltime'), ('G3', 'studytime'), ('G3', 'failures'), ('G3', 'schoolsup'), ('G3', 'famsup'), ('G3', 'paid'), ('G3', 'activities'), ('G3', 'nursery'), ('G3', 'higher'), ('G3', 'internet'), ('G3', 'romantic'), ('G3', 'famrel'), ('G3', 'freetime'), ('G3', 'goout'), ('G3', 'Dalc'), ('G3', 'Walc'), ('G3', 'health'), ('G3', 'absences'), ('G3', 'G1'), ('G3', 'G2')])




```python
structureModelPruned.out_edges
```




    OutEdgeView([('address', 'absences'), ('address', 'G1'), ('Pstatus', 'famrel'), ('Pstatus', 'absences'), ('Pstatus', 'G1'), ('studytime', 'G1'), ('failures', 'absences'), ('schoolsup', 'G1'), ('paid', 'absences'), ('higher', 'Medu'), ('higher', 'G1'), ('internet', 'absences'), ('Dalc', 'Walc'), ('G1', 'G2'), ('G2', 'G3')])




```python
# Adjacency object holding predecessors of each node
structureModelLearned.pred
```




    AdjacencyView({'address': {'famsize': {'origin': 'learned', 'weight': 2.57364988344861e-06}, 'Pstatus': {'origin': 'learned', 'weight': 4.034341252476512e-06}, 'Medu': {'origin': 'learned', 'weight': 5.282843496249485e-07}, 'Fedu': {'origin': 'learned', 'weight': 1.815837863695999e-06}, 'traveltime': {'origin': 'learned', 'weight': -3.2083752911421134e-08}, 'studytime': {'origin': 'learned', 'weight': 1.2094798742837836e-06}, 'failures': {'origin': 'learned', 'weight': 1.0270730806788747e-06}, 'schoolsup': {'origin': 'learned', 'weight': 0.09016610695015827}, 'famsup': {'origin': 'learned', 'weight': 0.10427386381413724}, 'paid': {'origin': 'learned', 'weight': -0.06226780216318523}, 'activities': {'origin': 'learned', 'weight': 0.05553758017558176}, 'nursery': {'origin': 'learned', 'weight': 0.2776178205344719}, 'higher': {'origin': 'learned', 'weight': 7.851783367975633e-07}, 'internet': {'origin': 'learned', 'weight': 0.40328532019811464}, 'romantic': {'origin': 'learned', 'weight': 0.03449641423060724}, 'famrel': {'origin': 'learned', 'weight': 1.320897881340788e-06}, 'freetime': {'origin': 'learned', 'weight': 4.999315254151007e-06}, 'goout': {'origin': 'learned', 'weight': 3.2035805298097187e-06}, 'Dalc': {'origin': 'learned', 'weight': 2.443914771173288e-06}, 'Walc': {'origin': 'learned', 'weight': 2.3235931090372038e-06}, 'health': {'origin': 'learned', 'weight': 2.495006069707716e-06}, 'absences': {'origin': 'learned', 'weight': 2.1954756979199574e-07}, 'G1': {'origin': 'learned', 'weight': 4.145635565322556e-07}, 'G2': {'origin': 'learned', 'weight': 1.0808731900149392e-06}, 'G3': {'origin': 'learned', 'weight': 2.8997294244065144e-06}}, 'famsize': {'address': {'origin': 'learned', 'weight': 0.07172400411745194}, 'Pstatus': {'origin': 'learned', 'weight': -0.17295794814902476}, 'Medu': {'origin': 'learned', 'weight': -8.376171747006237e-05}, 'Fedu': {'origin': 'learned', 'weight': -5.875240692181356e-06}, 'traveltime': {'origin': 'learned', 'weight': 5.681875851702312e-07}, 'studytime': {'origin': 'learned', 'weight': 2.2938931309765494e-06}, 'failures': {'origin': 'learned', 'weight': 0.007199670534529419}, 'schoolsup': {'origin': 'learned', 'weight': -0.07969030328801704}, 'famsup': {'origin': 'learned', 'weight': 0.0016122619388671963}, 'paid': {'origin': 'learned', 'weight': -0.08662176398113904}, 'activities': {'origin': 'learned', 'weight': 0.020024417715390045}, 'nursery': {'origin': 'learned', 'weight': 0.20181916953441106}, 'higher': {'origin': 'learned', 'weight': 0.17370961720916422}, 'internet': {'origin': 'learned', 'weight': 0.08161029156084386}, 'romantic': {'origin': 'learned', 'weight': 0.0001242279611122574}, 'famrel': {'origin': 'learned', 'weight': 8.77451264318084e-07}, 'freetime': {'origin': 'learned', 'weight': 7.565108486278707e-06}, 'goout': {'origin': 'learned', 'weight': 2.860011965556905e-06}, 'Dalc': {'origin': 'learned', 'weight': 6.124775682118712e-07}, 'Walc': {'origin': 'learned', 'weight': 9.661335752092414e-07}, 'health': {'origin': 'learned', 'weight': 4.5809455483301075e-06}, 'absences': {'origin': 'learned', 'weight': 8.597580220229035e-07}, 'G1': {'origin': 'learned', 'weight': 4.231758239400621e-07}, 'G2': {'origin': 'learned', 'weight': 1.018204545261268e-06}, 'G3': {'origin': 'learned', 'weight': 3.6447543713365855e-06}}, 'Pstatus': {'address': {'origin': 'learned', 'weight': 0.027500652131841753}, 'famsize': {'origin': 'learned', 'weight': -5.39386360384519e-07}, 'Medu': {'origin': 'learned', 'weight': 7.664857242148944e-07}, 'Fedu': {'origin': 'learned', 'weight': 1.0862756113952355e-06}, 'traveltime': {'origin': 'learned', 'weight': 1.5254924959846107e-07}, 'studytime': {'origin': 'learned', 'weight': 4.5152482925329287e-07}, 'failures': {'origin': 'learned', 'weight': 3.7113144071898173e-07}, 'schoolsup': {'origin': 'learned', 'weight': 0.0031060892594583374}, 'famsup': {'origin': 'learned', 'weight': 0.08467752097138515}, 'paid': {'origin': 'learned', 'weight': 0.01940453653643334}, 'activities': {'origin': 'learned', 'weight': 0.1186650900039901}, 'nursery': {'origin': 'learned', 'weight': 0.18458724734437718}, 'higher': {'origin': 'learned', 'weight': 0.42470020866871444}, 'internet': {'origin': 'learned', 'weight': 0.20073374119007015}, 'romantic': {'origin': 'learned', 'weight': 0.03882760026404552}, 'famrel': {'origin': 'learned', 'weight': 1.846478796364456e-07}, 'freetime': {'origin': 'learned', 'weight': 9.210757723189831e-07}, 'goout': {'origin': 'learned', 'weight': 3.2360205696198744e-06}, 'Dalc': {'origin': 'learned', 'weight': 3.3480538042122376e-07}, 'Walc': {'origin': 'learned', 'weight': 4.580593050516383e-07}, 'health': {'origin': 'learned', 'weight': 9.494811331021372e-07}, 'absences': {'origin': 'learned', 'weight': 3.110979370027898e-08}, 'G1': {'origin': 'learned', 'weight': 1.2192523374411585e-07}, 'G2': {'origin': 'learned', 'weight': 4.0197743788316634e-07}, 'G3': {'origin': 'learned', 'weight': 1.2383169619592981e-06}}, 'Medu': {'address': {'origin': 'learned', 'weight': 0.4329609981782503}, 'famsize': {'origin': 'learned', 'weight': -0.0016220902698672792}, 'Pstatus': {'origin': 'learned', 'weight': 0.1384140623478854}, 'Fedu': {'origin': 'learned', 'weight': 1.3815353478780808e-06}, 'traveltime': {'origin': 'learned', 'weight': -0.05682679496770537}, 'studytime': {'origin': 'learned', 'weight': 1.0099464281901412e-05}, 'failures': {'origin': 'learned', 'weight': -0.05554902196378678}, 'schoolsup': {'origin': 'learned', 'weight': -0.14973724028142785}, 'famsup': {'origin': 'learned', 'weight': 0.2712033095860632}, 'paid': {'origin': 'learned', 'weight': 0.45092087317544877}, 'activities': {'origin': 'learned', 'weight': 0.24111978808014004}, 'nursery': {'origin': 'learned', 'weight': 0.5239103813400171}, 'higher': {'origin': 'learned', 'weight': 0.9842407795725915}, 'internet': {'origin': 'learned', 'weight': 0.6875462651121823}, 'romantic': {'origin': 'learned', 'weight': 0.057553976531306665}, 'famrel': {'origin': 'learned', 'weight': 1.966155554661421e-05}, 'freetime': {'origin': 'learned', 'weight': 5.3045604346644666e-05}, 'goout': {'origin': 'learned', 'weight': 0.00013893787430084464}, 'Dalc': {'origin': 'learned', 'weight': 1.8941343308167783e-05}, 'Walc': {'origin': 'learned', 'weight': 1.0234019307479275e-05}, 'health': {'origin': 'learned', 'weight': 5.323859031710839e-05}, 'absences': {'origin': 'learned', 'weight': 3.818433288195618e-06}, 'G1': {'origin': 'learned', 'weight': 3.524468719738307e-06}, 'G2': {'origin': 'learned', 'weight': 9.147904181797066e-06}, 'G3': {'origin': 'learned', 'weight': 2.7181742380645266e-05}}, 'Fedu': {'address': {'origin': 'learned', 'weight': 0.10940724573937048}, 'famsize': {'origin': 'learned', 'weight': -0.024651044459558742}, 'Pstatus': {'origin': 'learned', 'weight': 0.14975863405325376}, 'Medu': {'origin': 'learned', 'weight': 0.6253625161000721}, 'traveltime': {'origin': 'learned', 'weight': 0.04369105682484006}, 'studytime': {'origin': 'learned', 'weight': -0.000495670140147531}, 'failures': {'origin': 'learned', 'weight': -0.03634104972539488}, 'schoolsup': {'origin': 'learned', 'weight': 0.111206285588392}, 'famsup': {'origin': 'learned', 'weight': 0.14573161333959725}, 'paid': {'origin': 'learned', 'weight': 0.07819729062203296}, 'activities': {'origin': 'learned', 'weight': 0.022242975459254674}, 'nursery': {'origin': 'learned', 'weight': 0.0576652012939855}, 'higher': {'origin': 'learned', 'weight': 0.28719837310478313}, 'internet': {'origin': 'learned', 'weight': 0.06454075511391491}, 'romantic': {'origin': 'learned', 'weight': -0.038502546594630475}, 'famrel': {'origin': 'learned', 'weight': 5.614649983118622e-06}, 'freetime': {'origin': 'learned', 'weight': 1.0989037361421973e-05}, 'goout': {'origin': 'learned', 'weight': 3.500255190181704e-05}, 'Dalc': {'origin': 'learned', 'weight': 6.684651844691612e-06}, 'Walc': {'origin': 'learned', 'weight': 5.230869729896622e-06}, 'health': {'origin': 'learned', 'weight': 8.728697764773375e-06}, 'absences': {'origin': 'learned', 'weight': 1.8252677120908404e-06}, 'G1': {'origin': 'learned', 'weight': 2.655572153653365e-06}, 'G2': {'origin': 'learned', 'weight': 6.073498805912339e-06}, 'G3': {'origin': 'learned', 'weight': 1.7927492482726562e-05}}, 'traveltime': {'address': {'origin': 'learned', 'weight': -0.3080468648891065}, 'famsize': {'origin': 'learned', 'weight': 0.25181986913147913}, 'Pstatus': {'origin': 'learned', 'weight': 0.714734047306784}, 'Medu': {'origin': 'learned', 'weight': -1.4976973044455327e-05}, 'Fedu': {'origin': 'learned', 'weight': 2.3458092007222387e-06}, 'studytime': {'origin': 'learned', 'weight': 2.7298276113987395e-06}, 'failures': {'origin': 'learned', 'weight': 0.28893299557926194}, 'schoolsup': {'origin': 'learned', 'weight': -0.05461326354951528}, 'famsup': {'origin': 'learned', 'weight': 0.09728374298715864}, 'paid': {'origin': 'learned', 'weight': -0.1751929065462438}, 'activities': {'origin': 'learned', 'weight': 0.008463822567962324}, 'nursery': {'origin': 'learned', 'weight': 0.3359494704671782}, 'higher': {'origin': 'learned', 'weight': 0.6652075929820775}, 'internet': {'origin': 'learned', 'weight': -0.021094282505113388}, 'romantic': {'origin': 'learned', 'weight': 0.14329667201511975}, 'famrel': {'origin': 'learned', 'weight': 1.2821620220563868e-06}, 'freetime': {'origin': 'learned', 'weight': 5.4929092719122535e-06}, 'goout': {'origin': 'learned', 'weight': 7.206819224813103e-06}, 'Dalc': {'origin': 'learned', 'weight': 1.6720888589429364e-06}, 'Walc': {'origin': 'learned', 'weight': 3.823707461640614e-06}, 'health': {'origin': 'learned', 'weight': 1.0242635060847743e-05}, 'absences': {'origin': 'learned', 'weight': 2.2660262196440774e-06}, 'G1': {'origin': 'learned', 'weight': 1.6493706472793821e-06}, 'G2': {'origin': 'learned', 'weight': 4.277353370007445e-06}, 'G3': {'origin': 'learned', 'weight': 8.956896659868888e-06}}, 'studytime': {'address': {'origin': 'learned', 'weight': 0.22858517407180592}, 'famsize': {'origin': 'learned', 'weight': 0.07404468489673609}, 'Pstatus': {'origin': 'learned', 'weight': 0.29230404950042704}, 'Medu': {'origin': 'learned', 'weight': 0.07663461056844137}, 'Fedu': {'origin': 'learned', 'weight': -0.002267727436488319}, 'traveltime': {'origin': 'learned', 'weight': 0.14665592285551024}, 'failures': {'origin': 'learned', 'weight': -0.036925581153895784}, 'schoolsup': {'origin': 'learned', 'weight': 0.2323474711325423}, 'famsup': {'origin': 'learned', 'weight': 0.266362204840018}, 'paid': {'origin': 'learned', 'weight': -0.06792582697060526}, 'activities': {'origin': 'learned', 'weight': 0.12516307931862}, 'nursery': {'origin': 'learned', 'weight': 0.18535635699631886}, 'higher': {'origin': 'learned', 'weight': 0.6614250646852067}, 'internet': {'origin': 'learned', 'weight': 0.09306481319152346}, 'romantic': {'origin': 'learned', 'weight': 0.15562427843420687}, 'famrel': {'origin': 'learned', 'weight': 2.7325071082731085e-06}, 'freetime': {'origin': 'learned', 'weight': 5.999391678181635e-06}, 'goout': {'origin': 'learned', 'weight': 5.392816587318543e-06}, 'Dalc': {'origin': 'learned', 'weight': -0.04079588249535337}, 'Walc': {'origin': 'learned', 'weight': -3.7312092819954272e-06}, 'health': {'origin': 'learned', 'weight': 8.714528708551217e-06}, 'absences': {'origin': 'learned', 'weight': -1.6241967207249302e-06}, 'G1': {'origin': 'learned', 'weight': 5.880507684560454e-07}, 'G2': {'origin': 'learned', 'weight': 1.4113913670578505e-06}, 'G3': {'origin': 'learned', 'weight': 5.052203280123686e-06}}, 'failures': {'address': {'origin': 'learned', 'weight': 0.06633709792506814}, 'famsize': {'origin': 'learned', 'weight': -0.00011631802985936184}, 'Pstatus': {'origin': 'learned', 'weight': 0.27245193062493933}, 'Medu': {'origin': 'learned', 'weight': -8.47848862991425e-06}, 'Fedu': {'origin': 'learned', 'weight': -4.4896874864671566e-06}, 'traveltime': {'origin': 'learned', 'weight': 8.390113681439373e-07}, 'studytime': {'origin': 'learned', 'weight': -4.52614007711886e-07}, 'schoolsup': {'origin': 'learned', 'weight': 0.05344254788762017}, 'famsup': {'origin': 'learned', 'weight': 0.08031678051890989}, 'paid': {'origin': 'learned', 'weight': 0.19488310269441256}, 'activities': {'origin': 'learned', 'weight': 0.045406510982519854}, 'nursery': {'origin': 'learned', 'weight': 0.0750746154121407}, 'higher': {'origin': 'learned', 'weight': -0.30470801802731773}, 'internet': {'origin': 'learned', 'weight': -0.015305344026746737}, 'romantic': {'origin': 'learned', 'weight': 0.10425856564537055}, 'famrel': {'origin': 'learned', 'weight': 1.8774318511130135e-06}, 'freetime': {'origin': 'learned', 'weight': 1.454765326837019e-06}, 'goout': {'origin': 'learned', 'weight': 1.2758953810800162e-05}, 'Dalc': {'origin': 'learned', 'weight': 1.5180401053457686e-06}, 'Walc': {'origin': 'learned', 'weight': 3.1858816041837672e-06}, 'health': {'origin': 'learned', 'weight': 2.806745787568456e-06}, 'absences': {'origin': 'learned', 'weight': 3.1040475703698455e-07}, 'G1': {'origin': 'learned', 'weight': -1.7871574230049647e-07}, 'G2': {'origin': 'learned', 'weight': -5.18613014617815e-07}, 'G3': {'origin': 'learned', 'weight': -1.621351356540549e-06}}, 'schoolsup': {'address': {'origin': 'learned', 'weight': 2.265558640319601e-06}, 'famsize': {'origin': 'learned', 'weight': 7.582265421368856e-07}, 'Pstatus': {'origin': 'learned', 'weight': 6.161919403615951e-06}, 'Medu': {'origin': 'learned', 'weight': 1.4871605630041722e-06}, 'Fedu': {'origin': 'learned', 'weight': 3.5966507196187998e-06}, 'traveltime': {'origin': 'learned', 'weight': 3.572657993912356e-06}, 'studytime': {'origin': 'learned', 'weight': 1.3187597528677218e-06}, 'failures': {'origin': 'learned', 'weight': 1.2442168943478484e-06}, 'famsup': {'origin': 'learned', 'weight': 1.633685547630518e-07}, 'paid': {'origin': 'learned', 'weight': 0.10971256665441963}, 'activities': {'origin': 'learned', 'weight': 0.07942221196339495}, 'nursery': {'origin': 'learned', 'weight': 4.4501014882221276e-07}, 'higher': {'origin': 'learned', 'weight': 1.2479890798999761e-06}, 'internet': {'origin': 'learned', 'weight': 1.7593655699762522e-06}, 'romantic': {'origin': 'learned', 'weight': 0.014368894340047815}, 'famrel': {'origin': 'learned', 'weight': 7.748541219982958e-06}, 'freetime': {'origin': 'learned', 'weight': 1.083118372234952e-05}, 'goout': {'origin': 'learned', 'weight': 9.292721765645084e-06}, 'Dalc': {'origin': 'learned', 'weight': 2.6577884822509986e-05}, 'Walc': {'origin': 'learned', 'weight': 6.602704056446805e-07}, 'health': {'origin': 'learned', 'weight': 3.8134498853512872e-06}, 'absences': {'origin': 'learned', 'weight': 3.2795583819598026e-07}, 'G1': {'origin': 'learned', 'weight': 4.865957647916266e-07}, 'G2': {'origin': 'learned', 'weight': 1.3800602422165208e-06}, 'G3': {'origin': 'learned', 'weight': 3.7300833122935385e-06}}, 'famsup': {'address': {'origin': 'learned', 'weight': 4.164128335492464e-06}, 'famsize': {'origin': 'learned', 'weight': 8.083571741711851e-06}, 'Pstatus': {'origin': 'learned', 'weight': 8.134891913687072e-06}, 'Medu': {'origin': 'learned', 'weight': 2.768426487726607e-06}, 'Fedu': {'origin': 'learned', 'weight': 8.380912481855755e-06}, 'traveltime': {'origin': 'learned', 'weight': 6.7280883915310845e-06}, 'studytime': {'origin': 'learned', 'weight': 3.733353224457675e-06}, 'failures': {'origin': 'learned', 'weight': 2.7970697872618514e-06}, 'schoolsup': {'origin': 'learned', 'weight': 0.43115271308130015}, 'paid': {'origin': 'learned', 'weight': 0.3711694184171664}, 'activities': {'origin': 'learned', 'weight': 0.40747787530276136}, 'nursery': {'origin': 'learned', 'weight': 5.245322452922104e-07}, 'higher': {'origin': 'learned', 'weight': 2.9132190513716887e-06}, 'internet': {'origin': 'learned', 'weight': 1.2448178984658832e-06}, 'romantic': {'origin': 'learned', 'weight': 0.3147106400752427}, 'famrel': {'origin': 'learned', 'weight': 1.0392942107720905e-05}, 'freetime': {'origin': 'learned', 'weight': 2.9264384487782554e-05}, 'goout': {'origin': 'learned', 'weight': 3.142034075725276e-05}, 'Dalc': {'origin': 'learned', 'weight': 3.898305342873185e-05}, 'Walc': {'origin': 'learned', 'weight': 2.462099835786531e-05}, 'health': {'origin': 'learned', 'weight': 2.320637753493311e-05}, 'absences': {'origin': 'learned', 'weight': 1.2319092982466107e-06}, 'G1': {'origin': 'learned', 'weight': 7.719161908753132e-06}, 'G2': {'origin': 'learned', 'weight': 3.0220831125406032e-05}, 'G3': {'origin': 'learned', 'weight': 6.9595740834268e-05}}, 'paid': {'address': {'origin': 'learned', 'weight': 2.6188325902813357e-06}, 'famsize': {'origin': 'learned', 'weight': 5.982031984826393e-07}, 'Pstatus': {'origin': 'learned', 'weight': 7.550818083392646e-06}, 'Medu': {'origin': 'learned', 'weight': 4.306941634359122e-07}, 'Fedu': {'origin': 'learned', 'weight': 1.5972940923620563e-06}, 'traveltime': {'origin': 'learned', 'weight': 1.1047233320614985e-06}, 'studytime': {'origin': 'learned', 'weight': 3.7336184729781297e-06}, 'failures': {'origin': 'learned', 'weight': 3.2799055993158386e-07}, 'schoolsup': {'origin': 'learned', 'weight': 4.393230469914194e-07}, 'famsup': {'origin': 'learned', 'weight': 1.7014085331477617e-07}, 'activities': {'origin': 'learned', 'weight': 1.0579930515164717e-07}, 'nursery': {'origin': 'learned', 'weight': 5.830128592885166e-07}, 'higher': {'origin': 'learned', 'weight': 2.7674708199764802e-06}, 'internet': {'origin': 'learned', 'weight': 1.4622746367588082e-06}, 'romantic': {'origin': 'learned', 'weight': 0.04724004434882376}, 'famrel': {'origin': 'learned', 'weight': 6.725986004009021e-06}, 'freetime': {'origin': 'learned', 'weight': 4.7266131590172746e-07}, 'goout': {'origin': 'learned', 'weight': 6.015041527997529e-06}, 'Dalc': {'origin': 'learned', 'weight': 1.3187861051116028e-06}, 'Walc': {'origin': 'learned', 'weight': 4.096182615608204e-06}, 'health': {'origin': 'learned', 'weight': 1.3045542586857709e-06}, 'absences': {'origin': 'learned', 'weight': 6.232694334298974e-08}, 'G1': {'origin': 'learned', 'weight': 4.879860760979429e-07}, 'G2': {'origin': 'learned', 'weight': 1.1816940754479807e-06}, 'G3': {'origin': 'learned', 'weight': 2.618791872592911e-06}}, 'activities': {'address': {'origin': 'learned', 'weight': 8.921883360997223e-06}, 'famsize': {'origin': 'learned', 'weight': 1.1369901568939202e-05}, 'Pstatus': {'origin': 'learned', 'weight': 9.167216054392334e-06}, 'Medu': {'origin': 'learned', 'weight': 4.839327739872298e-06}, 'Fedu': {'origin': 'learned', 'weight': 2.2202292453444777e-05}, 'traveltime': {'origin': 'learned', 'weight': 1.5182162182595177e-05}, 'studytime': {'origin': 'learned', 'weight': 1.1962348457785248e-05}, 'failures': {'origin': 'learned', 'weight': 5.462903893005342e-06}, 'schoolsup': {'origin': 'learned', 'weight': 3.3289576319408384e-06}, 'famsup': {'origin': 'learned', 'weight': 7.251013741149529e-07}, 'paid': {'origin': 'learned', 'weight': 0.42980667486373997}, 'nursery': {'origin': 'learned', 'weight': 8.75089591986338e-07}, 'higher': {'origin': 'learned', 'weight': 7.063695630694698e-06}, 'internet': {'origin': 'learned', 'weight': 2.270135281570907e-06}, 'romantic': {'origin': 'learned', 'weight': 0.4895721690598813}, 'famrel': {'origin': 'learned', 'weight': 1.7103940193342104e-05}, 'freetime': {'origin': 'learned', 'weight': 7.199372883872205e-06}, 'goout': {'origin': 'learned', 'weight': 4.984497634306652e-05}, 'Dalc': {'origin': 'learned', 'weight': 4.86850586028225e-05}, 'Walc': {'origin': 'learned', 'weight': 4.679631804837704e-05}, 'health': {'origin': 'learned', 'weight': 5.101290264386016e-05}, 'absences': {'origin': 'learned', 'weight': 6.813282419837235e-06}, 'G1': {'origin': 'learned', 'weight': 1.573168543985265e-05}, 'G2': {'origin': 'learned', 'weight': 5.669885412547309e-05}, 'G3': {'origin': 'learned', 'weight': 0.00019957011213946537}}, 'nursery': {'address': {'origin': 'learned', 'weight': 1.0431757754516237e-06}, 'famsize': {'origin': 'learned', 'weight': 1.3604190036451818e-06}, 'Pstatus': {'origin': 'learned', 'weight': 2.2293990599005983e-06}, 'Medu': {'origin': 'learned', 'weight': 9.859417699637172e-07}, 'Fedu': {'origin': 'learned', 'weight': 3.836377734813915e-06}, 'traveltime': {'origin': 'learned', 'weight': 1.4616510424530478e-06}, 'studytime': {'origin': 'learned', 'weight': 3.5500670023818374e-06}, 'failures': {'origin': 'learned', 'weight': 1.115736579162668e-06}, 'schoolsup': {'origin': 'learned', 'weight': 0.21898204604390092}, 'famsup': {'origin': 'learned', 'weight': 0.49493689368622484}, 'paid': {'origin': 'learned', 'weight': 0.10713624144249709}, 'activities': {'origin': 'learned', 'weight': 0.3870752878517111}, 'higher': {'origin': 'learned', 'weight': 9.369537748463454e-07}, 'internet': {'origin': 'learned', 'weight': 4.823286857399146e-07}, 'romantic': {'origin': 'learned', 'weight': 0.2448302568893097}, 'famrel': {'origin': 'learned', 'weight': 1.8503775845644034e-06}, 'freetime': {'origin': 'learned', 'weight': 7.151725171424487e-06}, 'goout': {'origin': 'learned', 'weight': 1.0622247426374497e-05}, 'Dalc': {'origin': 'learned', 'weight': 9.098998339948322e-06}, 'Walc': {'origin': 'learned', 'weight': 1.4819511531044937e-05}, 'health': {'origin': 'learned', 'weight': 7.240116351111648e-06}, 'absences': {'origin': 'learned', 'weight': 1.783222076390664e-06}, 'G1': {'origin': 'learned', 'weight': 2.2310985066482208e-06}, 'G2': {'origin': 'learned', 'weight': 7.608200291011169e-06}, 'G3': {'origin': 'learned', 'weight': 2.8136654487595504e-05}}, 'higher': {'address': {'origin': 'learned', 'weight': 0.2175470691398659}, 'famsize': {'origin': 'learned', 'weight': 3.4544721166046257e-07}, 'Pstatus': {'origin': 'learned', 'weight': 2.567768712230681e-07}, 'Medu': {'origin': 'learned', 'weight': 1.2090653015743418e-07}, 'Fedu': {'origin': 'learned', 'weight': 4.6588574867353284e-07}, 'traveltime': {'origin': 'learned', 'weight': 2.1338297753062791e-07}, 'studytime': {'origin': 'learned', 'weight': 2.3561892859955156e-07}, 'failures': {'origin': 'learned', 'weight': -1.583102592694493e-07}, 'schoolsup': {'origin': 'learned', 'weight': 0.15113701551678627}, 'famsup': {'origin': 'learned', 'weight': 0.17814403224742134}, 'paid': {'origin': 'learned', 'weight': 0.0651615011059292}, 'activities': {'origin': 'learned', 'weight': 0.10140915280647488}, 'nursery': {'origin': 'learned', 'weight': 0.33856473446106944}, 'internet': {'origin': 'learned', 'weight': 0.27561946030947526}, 'romantic': {'origin': 'learned', 'weight': 0.013855780556472706}, 'famrel': {'origin': 'learned', 'weight': 3.11903271403777e-07}, 'freetime': {'origin': 'learned', 'weight': 2.4368058171397756e-06}, 'goout': {'origin': 'learned', 'weight': 6.733122212252568e-06}, 'Dalc': {'origin': 'learned', 'weight': 1.3772195017901158e-06}, 'Walc': {'origin': 'learned', 'weight': 1.0224844526732827e-06}, 'health': {'origin': 'learned', 'weight': 6.676523819363924e-07}, 'absences': {'origin': 'learned', 'weight': 5.590376239583715e-08}, 'G1': {'origin': 'learned', 'weight': 1.1238345971304325e-07}, 'G2': {'origin': 'learned', 'weight': 1.9509765374517475e-07}, 'G3': {'origin': 'learned', 'weight': 7.976562142570407e-07}}, 'internet': {'address': {'origin': 'learned', 'weight': 4.631899217412905e-07}, 'famsize': {'origin': 'learned', 'weight': 1.985563914894138e-06}, 'Pstatus': {'origin': 'learned', 'weight': 1.2495739741261968e-06}, 'Medu': {'origin': 'learned', 'weight': 3.826610819737762e-07}, 'Fedu': {'origin': 'learned', 'weight': 1.6062126461530145e-06}, 'traveltime': {'origin': 'learned', 'weight': 1.6460904743183209e-06}, 'studytime': {'origin': 'learned', 'weight': 2.96354399751265e-06}, 'failures': {'origin': 'learned', 'weight': -4.150375359058897e-08}, 'schoolsup': {'origin': 'learned', 'weight': 0.04153209516996423}, 'famsup': {'origin': 'learned', 'weight': 0.27715008710483463}, 'paid': {'origin': 'learned', 'weight': 0.06155932087550792}, 'activities': {'origin': 'learned', 'weight': 0.22115620514055448}, 'nursery': {'origin': 'learned', 'weight': 0.4242928819958667}, 'higher': {'origin': 'learned', 'weight': 7.463964327612281e-07}, 'romantic': {'origin': 'learned', 'weight': 0.14405028246426685}, 'famrel': {'origin': 'learned', 'weight': 1.1560838230536603e-06}, 'freetime': {'origin': 'learned', 'weight': 3.6712820497747034e-06}, 'goout': {'origin': 'learned', 'weight': 6.996845346414707e-06}, 'Dalc': {'origin': 'learned', 'weight': 1.9892730666634255e-06}, 'Walc': {'origin': 'learned', 'weight': 3.2089637875986894e-06}, 'health': {'origin': 'learned', 'weight': 4.782931502866295e-06}, 'absences': {'origin': 'learned', 'weight': 3.687447609686423e-07}, 'G1': {'origin': 'learned', 'weight': 1.1594765224713857e-06}, 'G2': {'origin': 'learned', 'weight': 3.3812595236012536e-06}, 'G3': {'origin': 'learned', 'weight': 1.1023378253076663e-05}}, 'romantic': {'address': {'origin': 'learned', 'weight': 2.1163994047249527e-05}, 'famsize': {'origin': 'learned', 'weight': 2.9757663553056567e-05}, 'Pstatus': {'origin': 'learned', 'weight': 3.606586324263287e-05}, 'Medu': {'origin': 'learned', 'weight': 1.7041739225182675e-05}, 'Fedu': {'origin': 'learned', 'weight': 6.776538544245963e-05}, 'traveltime': {'origin': 'learned', 'weight': 1.3548531245438947e-05}, 'studytime': {'origin': 'learned', 'weight': 1.3775916562081774e-05}, 'failures': {'origin': 'learned', 'weight': 5.644847741993733e-06}, 'schoolsup': {'origin': 'learned', 'weight': 1.741729645205567e-05}, 'famsup': {'origin': 'learned', 'weight': 1.212623696766134e-06}, 'paid': {'origin': 'learned', 'weight': 6.219147593514768e-06}, 'activities': {'origin': 'learned', 'weight': 5.062885962223394e-07}, 'nursery': {'origin': 'learned', 'weight': 2.139012622741077e-06}, 'higher': {'origin': 'learned', 'weight': 2.268046145982143e-05}, 'internet': {'origin': 'learned', 'weight': 5.241075220842723e-06}, 'famrel': {'origin': 'learned', 'weight': 3.644736374916043e-05}, 'freetime': {'origin': 'learned', 'weight': 2.6581035887039415e-05}, 'goout': {'origin': 'learned', 'weight': 0.00014000699129624396}, 'Dalc': {'origin': 'learned', 'weight': 1.1085710188018912e-05}, 'Walc': {'origin': 'learned', 'weight': 2.529025287342515e-05}, 'health': {'origin': 'learned', 'weight': 6.18192581736639e-05}, 'absences': {'origin': 'learned', 'weight': 1.6291233178806432e-06}, 'G1': {'origin': 'learned', 'weight': 4.5568396125773596e-05}, 'G2': {'origin': 'learned', 'weight': 0.000163890714845625}, 'G3': {'origin': 'learned', 'weight': 0.0005007381639334503}}, 'famrel': {'address': {'origin': 'learned', 'weight': 0.2713375883408355}, 'famsize': {'origin': 'learned', 'weight': 0.23128615865426996}, 'Pstatus': {'origin': 'learned', 'weight': 0.8402877660070628}, 'Medu': {'origin': 'learned', 'weight': 0.06395750625321515}, 'Fedu': {'origin': 'learned', 'weight': 0.09036740104688158}, 'traveltime': {'origin': 'learned', 'weight': 0.3652619258538022}, 'studytime': {'origin': 'learned', 'weight': 0.15816240290931505}, 'failures': {'origin': 'learned', 'weight': 0.1668232709293059}, 'schoolsup': {'origin': 'learned', 'weight': 0.013400176227771085}, 'famsup': {'origin': 'learned', 'weight': 0.09564586270588174}, 'paid': {'origin': 'learned', 'weight': 0.07276395951434235}, 'activities': {'origin': 'learned', 'weight': 0.1060097717426425}, 'nursery': {'origin': 'learned', 'weight': 0.432569121650298}, 'higher': {'origin': 'learned', 'weight': 0.749421075800239}, 'internet': {'origin': 'learned', 'weight': 0.40830632335954425}, 'romantic': {'origin': 'learned', 'weight': 0.09273389200751765}, 'freetime': {'origin': 'learned', 'weight': 2.6864503278375758e-06}, 'goout': {'origin': 'learned', 'weight': 8.279250568554317e-06}, 'Dalc': {'origin': 'learned', 'weight': 0.061860074406191755}, 'Walc': {'origin': 'learned', 'weight': -2.572005415955528e-05}, 'health': {'origin': 'learned', 'weight': 2.7931909257193434e-06}, 'absences': {'origin': 'learned', 'weight': 6.761395164008487e-06}, 'G1': {'origin': 'learned', 'weight': 2.1548227065399565e-06}, 'G2': {'origin': 'learned', 'weight': 4.421633581782909e-06}, 'G3': {'origin': 'learned', 'weight': 1.2436281655857373e-05}}, 'freetime': {'address': {'origin': 'learned', 'weight': 0.11768720419459214}, 'famsize': {'origin': 'learned', 'weight': 0.023554521782170514}, 'Pstatus': {'origin': 'learned', 'weight': 0.3076339104564842}, 'Medu': {'origin': 'learned', 'weight': 0.005298006953244488}, 'Fedu': {'origin': 'learned', 'weight': 0.07269279661945031}, 'traveltime': {'origin': 'learned', 'weight': 0.1386601673406505}, 'studytime': {'origin': 'learned', 'weight': 0.061672808424480724}, 'failures': {'origin': 'learned', 'weight': 0.2757287584822249}, 'schoolsup': {'origin': 'learned', 'weight': 0.08146892483723561}, 'famsup': {'origin': 'learned', 'weight': 0.08487609151687552}, 'paid': {'origin': 'learned', 'weight': -0.397084583455957}, 'activities': {'origin': 'learned', 'weight': 0.29025194859764786}, 'nursery': {'origin': 'learned', 'weight': 0.18200415195307637}, 'higher': {'origin': 'learned', 'weight': 0.05992191532028243}, 'internet': {'origin': 'learned', 'weight': 0.19475274397573786}, 'romantic': {'origin': 'learned', 'weight': 0.12148123441125036}, 'famrel': {'origin': 'learned', 'weight': 0.31156532861814135}, 'goout': {'origin': 'learned', 'weight': 2.2300812352732997e-06}, 'Dalc': {'origin': 'learned', 'weight': 0.08959510517136154}, 'Walc': {'origin': 'learned', 'weight': 0.1213001152355078}, 'health': {'origin': 'learned', 'weight': 2.8779314964966107e-06}, 'absences': {'origin': 'learned', 'weight': -2.8147000352287287e-06}, 'G1': {'origin': 'learned', 'weight': 5.557825534741226e-06}, 'G2': {'origin': 'learned', 'weight': 9.63198572344712e-06}, 'G3': {'origin': 'learned', 'weight': 1.4630621123820853e-05}}, 'goout': {'address': {'origin': 'learned', 'weight': 0.16392393831724242}, 'famsize': {'origin': 'learned', 'weight': -0.089444259197238}, 'Pstatus': {'origin': 'learned', 'weight': -0.006601878891263519}, 'Medu': {'origin': 'learned', 'weight': 0.017833992490542724}, 'Fedu': {'origin': 'learned', 'weight': 0.001521336398273317}, 'traveltime': {'origin': 'learned', 'weight': 0.14543707996940677}, 'studytime': {'origin': 'learned', 'weight': 0.050063594468249706}, 'failures': {'origin': 'learned', 'weight': -0.00253721944936783}, 'schoolsup': {'origin': 'learned', 'weight': -0.054048281147243506}, 'famsup': {'origin': 'learned', 'weight': 0.09664059894202708}, 'paid': {'origin': 'learned', 'weight': -0.05554731045279839}, 'activities': {'origin': 'learned', 'weight': 0.053016213518201454}, 'nursery': {'origin': 'learned', 'weight': 0.17017617661645093}, 'higher': {'origin': 'learned', 'weight': -0.02944249552655697}, 'internet': {'origin': 'learned', 'weight': 0.1408710805149382}, 'romantic': {'origin': 'learned', 'weight': 0.011833625417886233}, 'famrel': {'origin': 'learned', 'weight': 0.13688329678438912}, 'freetime': {'origin': 'learned', 'weight': 0.3402337019417903}, 'Dalc': {'origin': 'learned', 'weight': -0.0024505554268309045}, 'Walc': {'origin': 'learned', 'weight': 0.3524600102352628}, 'health': {'origin': 'learned', 'weight': -5.738929894237622e-06}, 'absences': {'origin': 'learned', 'weight': 2.98875965846704e-06}, 'G1': {'origin': 'learned', 'weight': 9.449183937356098e-06}, 'G2': {'origin': 'learned', 'weight': 2.416742610715618e-05}, 'G3': {'origin': 'learned', 'weight': 8.885235654394119e-05}}, 'Dalc': {'address': {'origin': 'learned', 'weight': 0.11663243893798651}, 'famsize': {'origin': 'learned', 'weight': 0.272822548840043}, 'Pstatus': {'origin': 'learned', 'weight': 0.451312158903729}, 'Medu': {'origin': 'learned', 'weight': 0.05639212133201029}, 'Fedu': {'origin': 'learned', 'weight': 0.06540063043992946}, 'traveltime': {'origin': 'learned', 'weight': 0.2640464432914783}, 'studytime': {'origin': 'learned', 'weight': -1.7407881648513562e-05}, 'failures': {'origin': 'learned', 'weight': 0.19852244938589078}, 'schoolsup': {'origin': 'learned', 'weight': 0.030431446056897765}, 'famsup': {'origin': 'learned', 'weight': 0.01911615512884646}, 'paid': {'origin': 'learned', 'weight': 0.18947644768941185}, 'activities': {'origin': 'learned', 'weight': 0.03508084451564856}, 'nursery': {'origin': 'learned', 'weight': -0.05664828517064359}, 'higher': {'origin': 'learned', 'weight': -0.06561934921537634}, 'internet': {'origin': 'learned', 'weight': 0.2086038568514957}, 'romantic': {'origin': 'learned', 'weight': 0.17526816121879552}, 'famrel': {'origin': 'learned', 'weight': 8.974158916716448e-06}, 'freetime': {'origin': 'learned', 'weight': 9.033290147904766e-06}, 'goout': {'origin': 'learned', 'weight': 4.8560363036115805e-06}, 'Walc': {'origin': 'learned', 'weight': 6.927723939556109e-07}, 'health': {'origin': 'learned', 'weight': 6.5806594432733315e-06}, 'absences': {'origin': 'learned', 'weight': 1.2537933032705393e-06}, 'G1': {'origin': 'learned', 'weight': -1.5501567349024007e-06}, 'G2': {'origin': 'learned', 'weight': -4.049949010417597e-06}, 'G3': {'origin': 'learned', 'weight': -1.519052520577944e-05}}, 'Walc': {'address': {'origin': 'learned', 'weight': 0.16559963300289912}, 'famsize': {'origin': 'learned', 'weight': 0.21200668687560334}, 'Pstatus': {'origin': 'learned', 'weight': 0.4005429332616751}, 'Medu': {'origin': 'learned', 'weight': -0.05655177993703371}, 'Fedu': {'origin': 'learned', 'weight': 0.12603842388100064}, 'traveltime': {'origin': 'learned', 'weight': 0.1054311976437596}, 'studytime': {'origin': 'learned', 'weight': -0.13225283210928684}, 'failures': {'origin': 'learned', 'weight': 0.1110213039605426}, 'schoolsup': {'origin': 'learned', 'weight': -0.28625533228773004}, 'famsup': {'origin': 'learned', 'weight': -0.08227553368062841}, 'paid': {'origin': 'learned', 'weight': 0.03286301430594966}, 'activities': {'origin': 'learned', 'weight': 0.05822411086046015}, 'nursery': {'origin': 'learned', 'weight': 0.017727713239038333}, 'higher': {'origin': 'learned', 'weight': 0.2709113403707566}, 'internet': {'origin': 'learned', 'weight': 0.1663542314573771}, 'romantic': {'origin': 'learned', 'weight': -0.08849224803371417}, 'famrel': {'origin': 'learned', 'weight': 0.012488501523243383}, 'freetime': {'origin': 'learned', 'weight': 5.723497269328464e-06}, 'goout': {'origin': 'learned', 'weight': 2.1472173559096028e-06}, 'Dalc': {'origin': 'learned', 'weight': 0.8623769618608512}, 'health': {'origin': 'learned', 'weight': 2.5242442268968173e-06}, 'absences': {'origin': 'learned', 'weight': 2.9049481240489784e-06}, 'G1': {'origin': 'learned', 'weight': 5.0681509628027555e-05}, 'G2': {'origin': 'learned', 'weight': 4.391655782041878e-06}, 'G3': {'origin': 'learned', 'weight': -5.154448682834879e-06}}, 'health': {'address': {'origin': 'learned', 'weight': 0.20294893185551394}, 'famsize': {'origin': 'learned', 'weight': 0.07702410821801904}, 'Pstatus': {'origin': 'learned', 'weight': 0.2873495054103081}, 'Medu': {'origin': 'learned', 'weight': -0.0017836759484594275}, 'Fedu': {'origin': 'learned', 'weight': 0.09655752353619704}, 'traveltime': {'origin': 'learned', 'weight': 0.05946039269548516}, 'studytime': {'origin': 'learned', 'weight': 0.044435607273602996}, 'failures': {'origin': 'learned', 'weight': 0.17934136094011674}, 'schoolsup': {'origin': 'learned', 'weight': 0.16814364990171213}, 'famsup': {'origin': 'learned', 'weight': 0.1009039626224132}, 'paid': {'origin': 'learned', 'weight': 0.2884379850406954}, 'activities': {'origin': 'learned', 'weight': -0.04472072932931432}, 'nursery': {'origin': 'learned', 'weight': 0.1833351895084601}, 'higher': {'origin': 'learned', 'weight': 0.460475844352154}, 'internet': {'origin': 'learned', 'weight': -0.12331190291514839}, 'romantic': {'origin': 'learned', 'weight': 0.09235839989213118}, 'famrel': {'origin': 'learned', 'weight': 0.32535235552165176}, 'freetime': {'origin': 'learned', 'weight': 0.20359128011716196}, 'goout': {'origin': 'learned', 'weight': -0.12015368066308832}, 'Dalc': {'origin': 'learned', 'weight': 0.0062315200782290985}, 'Walc': {'origin': 'learned', 'weight': 0.22910017223115414}, 'absences': {'origin': 'learned', 'weight': -2.3873787462029974e-05}, 'G1': {'origin': 'learned', 'weight': 1.4456180749546806e-05}, 'G2': {'origin': 'learned', 'weight': 3.863184393270905e-06}, 'G3': {'origin': 'learned', 'weight': -8.85746266481034e-07}}, 'absences': {'address': {'origin': 'learned', 'weight': 1.0400949529066366}, 'famsize': {'origin': 'learned', 'weight': -0.1488343695903593}, 'Pstatus': {'origin': 'learned', 'weight': -1.0538754156321408}, 'Medu': {'origin': 'learned', 'weight': -0.10963221670789629}, 'Fedu': {'origin': 'learned', 'weight': 0.34662147120177766}, 'traveltime': {'origin': 'learned', 'weight': 0.31742677251596246}, 'studytime': {'origin': 'learned', 'weight': -0.24449913460462702}, 'failures': {'origin': 'learned', 'weight': 0.9395791571697139}, 'schoolsup': {'origin': 'learned', 'weight': -0.44169320558277186}, 'famsup': {'origin': 'learned', 'weight': 0.6753957856896687}, 'paid': {'origin': 'learned', 'weight': -1.0534625350951718}, 'activities': {'origin': 'learned', 'weight': -0.011557604864954631}, 'nursery': {'origin': 'learned', 'weight': 0.19424952439476387}, 'higher': {'origin': 'learned', 'weight': -0.4644399619110806}, 'internet': {'origin': 'learned', 'weight': 0.8369080746968736}, 'romantic': {'origin': 'learned', 'weight': 0.7593034494873926}, 'famrel': {'origin': 'learned', 'weight': 0.029534730152577033}, 'freetime': {'origin': 'learned', 'weight': -0.13258912399887035}, 'goout': {'origin': 'learned', 'weight': 0.22748994743278778}, 'Dalc': {'origin': 'learned', 'weight': 0.6285293747934196}, 'Walc': {'origin': 'learned', 'weight': 0.28212912867979606}, 'health': {'origin': 'learned', 'weight': 0.013270440047704299}, 'G1': {'origin': 'learned', 'weight': -0.16519243826107544}, 'G2': {'origin': 'learned', 'weight': -0.12083364187284075}, 'G3': {'origin': 'learned', 'weight': 0.2799693506960016}}, 'G1': {'address': {'origin': 'learned', 'weight': 1.006295091882122}, 'famsize': {'origin': 'learned', 'weight': 0.5361350969644317}, 'Pstatus': {'origin': 'learned', 'weight': 1.261362346111696}, 'Medu': {'origin': 'learned', 'weight': 0.3731879464225919}, 'Fedu': {'origin': 'learned', 'weight': 0.2457622670411357}, 'traveltime': {'origin': 'learned', 'weight': 0.4258522757563797}, 'studytime': {'origin': 'learned', 'weight': 0.8636139137063454}, 'failures': {'origin': 'learned', 'weight': -0.7734093106877317}, 'schoolsup': {'origin': 'learned', 'weight': -0.8015184747758134}, 'famsup': {'origin': 'learned', 'weight': 0.013792402912843525}, 'paid': {'origin': 'learned', 'weight': -0.7476665468841639}, 'activities': {'origin': 'learned', 'weight': 0.13356290095617598}, 'nursery': {'origin': 'learned', 'weight': 0.26458992819928057}, 'higher': {'origin': 'learned', 'weight': 2.6906165356962597}, 'internet': {'origin': 'learned', 'weight': 0.4693377785294991}, 'romantic': {'origin': 'learned', 'weight': 0.04875311772928067}, 'famrel': {'origin': 'learned', 'weight': 0.46833609431305073}, 'freetime': {'origin': 'learned', 'weight': 0.15893694608957573}, 'goout': {'origin': 'learned', 'weight': 0.0725254040091578}, 'Dalc': {'origin': 'learned', 'weight': -0.1679903202090344}, 'Walc': {'origin': 'learned', 'weight': 0.01628754240663206}, 'health': {'origin': 'learned', 'weight': 0.09831680087724673}, 'absences': {'origin': 'learned', 'weight': -1.5031127212036804e-06}, 'G2': {'origin': 'learned', 'weight': 4.852215936739337e-06}, 'G3': {'origin': 'learned', 'weight': 1.2269310076312509e-05}}, 'G2': {'address': {'origin': 'learned', 'weight': 0.15007496882413057}, 'famsize': {'origin': 'learned', 'weight': 0.032840481295506055}, 'Pstatus': {'origin': 'learned', 'weight': 0.18088756091335226}, 'Medu': {'origin': 'learned', 'weight': 0.048587816372934696}, 'Fedu': {'origin': 'learned', 'weight': 0.06740156244799099}, 'traveltime': {'origin': 'learned', 'weight': 0.0452125282264167}, 'studytime': {'origin': 'learned', 'weight': 0.05362052988133593}, 'failures': {'origin': 'learned', 'weight': -0.17877938791798662}, 'schoolsup': {'origin': 'learned', 'weight': 0.01756848085425741}, 'famsup': {'origin': 'learned', 'weight': -0.008335288023269384}, 'paid': {'origin': 'learned', 'weight': 0.215077113364691}, 'activities': {'origin': 'learned', 'weight': -0.02719253860768766}, 'nursery': {'origin': 'learned', 'weight': 0.07008782622305502}, 'higher': {'origin': 'learned', 'weight': 0.21293172852077402}, 'internet': {'origin': 'learned', 'weight': 0.10416797222379809}, 'romantic': {'origin': 'learned', 'weight': -0.039529109530973716}, 'famrel': {'origin': 'learned', 'weight': 0.20116104297386833}, 'freetime': {'origin': 'learned', 'weight': -0.021466939129440744}, 'goout': {'origin': 'learned', 'weight': -0.008887013971329476}, 'Dalc': {'origin': 'learned', 'weight': 0.01828514198351367}, 'Walc': {'origin': 'learned', 'weight': -0.028336314998879123}, 'health': {'origin': 'learned', 'weight': -0.0655360822154847}, 'absences': {'origin': 'learned', 'weight': 3.886996614933009e-06}, 'G1': {'origin': 'learned', 'weight': 0.8893123602483163}, 'G3': {'origin': 'learned', 'weight': 1.6073761334772817e-06}}, 'G3': {'address': {'origin': 'learned', 'weight': 0.223096391377955}, 'famsize': {'origin': 'learned', 'weight': 0.03510912683115285}, 'Pstatus': {'origin': 'learned', 'weight': -0.08860028396266117}, 'Medu': {'origin': 'learned', 'weight': -0.04977786757469074}, 'Fedu': {'origin': 'learned', 'weight': 0.04209668187865408}, 'traveltime': {'origin': 'learned', 'weight': 0.1472529805083419}, 'studytime': {'origin': 'learned', 'weight': 0.07325427221999745}, 'failures': {'origin': 'learned', 'weight': -0.15972379098765793}, 'schoolsup': {'origin': 'learned', 'weight': -0.16017431148807354}, 'famsup': {'origin': 'learned', 'weight': 0.11012660720124419}, 'paid': {'origin': 'learned', 'weight': -0.19159897136433737}, 'activities': {'origin': 'learned', 'weight': 0.008521962648982792}, 'nursery': {'origin': 'learned', 'weight': -0.04178769441684207}, 'higher': {'origin': 'learned', 'weight': 0.161696919211617}, 'internet': {'origin': 'learned', 'weight': 0.12476082994216223}, 'romantic': {'origin': 'learned', 'weight': -0.0005487024932422538}, 'famrel': {'origin': 'learned', 'weight': -0.024238569511162412}, 'freetime': {'origin': 'learned', 'weight': -0.035291910715639876}, 'goout': {'origin': 'learned', 'weight': -0.005467748034587408}, 'Dalc': {'origin': 'learned', 'weight': -0.06069763850187142}, 'Walc': {'origin': 'learned', 'weight': -0.017052027248871705}, 'health': {'origin': 'learned', 'weight': -0.03549672945498936}, 'absences': {'origin': 'learned', 'weight': 3.987948656636059e-06}, 'G1': {'origin': 'learned', 'weight': 0.1314622702860853}, 'G2': {'origin': 'learned', 'weight': 0.884705682463779}}})




```python
# Adjacency object holding predecessors of each node
structureModelPruned.pred
```




    AdjacencyView({'address': {}, 'famsize': {}, 'Pstatus': {}, 'Medu': {'higher': {'origin': 'learned', 'weight': 0.9842407795725915}}, 'Fedu': {}, 'traveltime': {}, 'studytime': {}, 'failures': {}, 'schoolsup': {}, 'famsup': {}, 'paid': {}, 'activities': {}, 'nursery': {}, 'higher': {}, 'internet': {}, 'romantic': {}, 'famrel': {'Pstatus': {'origin': 'learned', 'weight': 0.8402877660070628}}, 'freetime': {}, 'goout': {}, 'Dalc': {}, 'Walc': {'Dalc': {'origin': 'learned', 'weight': 0.8623769618608512}}, 'health': {}, 'absences': {'address': {'origin': 'learned', 'weight': 1.0400949529066366}, 'Pstatus': {'origin': 'learned', 'weight': -1.0538754156321408}, 'failures': {'origin': 'learned', 'weight': 0.9395791571697139}, 'paid': {'origin': 'learned', 'weight': -1.0534625350951718}, 'internet': {'origin': 'learned', 'weight': 0.8369080746968736}}, 'G1': {'address': {'origin': 'learned', 'weight': 1.006295091882122}, 'Pstatus': {'origin': 'learned', 'weight': 1.261362346111696}, 'studytime': {'origin': 'learned', 'weight': 0.8636139137063454}, 'schoolsup': {'origin': 'learned', 'weight': -0.8015184747758134}, 'higher': {'origin': 'learned', 'weight': 2.6906165356962597}}, 'G2': {'G1': {'origin': 'learned', 'weight': 0.8893123602483163}}, 'G3': {'G2': {'origin': 'learned', 'weight': 0.884705682463779}}})




```python
# Adjacency object holding the successors of each node
structureModelLearned.succ
```




    AdjacencyView({'address': {'famsize': {'origin': 'learned', 'weight': 0.07172400411745194}, 'Pstatus': {'origin': 'learned', 'weight': 0.027500652131841753}, 'Medu': {'origin': 'learned', 'weight': 0.4329609981782503}, 'Fedu': {'origin': 'learned', 'weight': 0.10940724573937048}, 'traveltime': {'origin': 'learned', 'weight': -0.3080468648891065}, 'studytime': {'origin': 'learned', 'weight': 0.22858517407180592}, 'failures': {'origin': 'learned', 'weight': 0.06633709792506814}, 'schoolsup': {'origin': 'learned', 'weight': 2.265558640319601e-06}, 'famsup': {'origin': 'learned', 'weight': 4.164128335492464e-06}, 'paid': {'origin': 'learned', 'weight': 2.6188325902813357e-06}, 'activities': {'origin': 'learned', 'weight': 8.921883360997223e-06}, 'nursery': {'origin': 'learned', 'weight': 1.0431757754516237e-06}, 'higher': {'origin': 'learned', 'weight': 0.2175470691398659}, 'internet': {'origin': 'learned', 'weight': 4.631899217412905e-07}, 'romantic': {'origin': 'learned', 'weight': 2.1163994047249527e-05}, 'famrel': {'origin': 'learned', 'weight': 0.2713375883408355}, 'freetime': {'origin': 'learned', 'weight': 0.11768720419459214}, 'goout': {'origin': 'learned', 'weight': 0.16392393831724242}, 'Dalc': {'origin': 'learned', 'weight': 0.11663243893798651}, 'Walc': {'origin': 'learned', 'weight': 0.16559963300289912}, 'health': {'origin': 'learned', 'weight': 0.20294893185551394}, 'absences': {'origin': 'learned', 'weight': 1.0400949529066366}, 'G1': {'origin': 'learned', 'weight': 1.006295091882122}, 'G2': {'origin': 'learned', 'weight': 0.15007496882413057}, 'G3': {'origin': 'learned', 'weight': 0.223096391377955}}, 'famsize': {'address': {'origin': 'learned', 'weight': 2.57364988344861e-06}, 'Pstatus': {'origin': 'learned', 'weight': -5.39386360384519e-07}, 'Medu': {'origin': 'learned', 'weight': -0.0016220902698672792}, 'Fedu': {'origin': 'learned', 'weight': -0.024651044459558742}, 'traveltime': {'origin': 'learned', 'weight': 0.25181986913147913}, 'studytime': {'origin': 'learned', 'weight': 0.07404468489673609}, 'failures': {'origin': 'learned', 'weight': -0.00011631802985936184}, 'schoolsup': {'origin': 'learned', 'weight': 7.582265421368856e-07}, 'famsup': {'origin': 'learned', 'weight': 8.083571741711851e-06}, 'paid': {'origin': 'learned', 'weight': 5.982031984826393e-07}, 'activities': {'origin': 'learned', 'weight': 1.1369901568939202e-05}, 'nursery': {'origin': 'learned', 'weight': 1.3604190036451818e-06}, 'higher': {'origin': 'learned', 'weight': 3.4544721166046257e-07}, 'internet': {'origin': 'learned', 'weight': 1.985563914894138e-06}, 'romantic': {'origin': 'learned', 'weight': 2.9757663553056567e-05}, 'famrel': {'origin': 'learned', 'weight': 0.23128615865426996}, 'freetime': {'origin': 'learned', 'weight': 0.023554521782170514}, 'goout': {'origin': 'learned', 'weight': -0.089444259197238}, 'Dalc': {'origin': 'learned', 'weight': 0.272822548840043}, 'Walc': {'origin': 'learned', 'weight': 0.21200668687560334}, 'health': {'origin': 'learned', 'weight': 0.07702410821801904}, 'absences': {'origin': 'learned', 'weight': -0.1488343695903593}, 'G1': {'origin': 'learned', 'weight': 0.5361350969644317}, 'G2': {'origin': 'learned', 'weight': 0.032840481295506055}, 'G3': {'origin': 'learned', 'weight': 0.03510912683115285}}, 'Pstatus': {'address': {'origin': 'learned', 'weight': 4.034341252476512e-06}, 'famsize': {'origin': 'learned', 'weight': -0.17295794814902476}, 'Medu': {'origin': 'learned', 'weight': 0.1384140623478854}, 'Fedu': {'origin': 'learned', 'weight': 0.14975863405325376}, 'traveltime': {'origin': 'learned', 'weight': 0.714734047306784}, 'studytime': {'origin': 'learned', 'weight': 0.29230404950042704}, 'failures': {'origin': 'learned', 'weight': 0.27245193062493933}, 'schoolsup': {'origin': 'learned', 'weight': 6.161919403615951e-06}, 'famsup': {'origin': 'learned', 'weight': 8.134891913687072e-06}, 'paid': {'origin': 'learned', 'weight': 7.550818083392646e-06}, 'activities': {'origin': 'learned', 'weight': 9.167216054392334e-06}, 'nursery': {'origin': 'learned', 'weight': 2.2293990599005983e-06}, 'higher': {'origin': 'learned', 'weight': 2.567768712230681e-07}, 'internet': {'origin': 'learned', 'weight': 1.2495739741261968e-06}, 'romantic': {'origin': 'learned', 'weight': 3.606586324263287e-05}, 'famrel': {'origin': 'learned', 'weight': 0.8402877660070628}, 'freetime': {'origin': 'learned', 'weight': 0.3076339104564842}, 'goout': {'origin': 'learned', 'weight': -0.006601878891263519}, 'Dalc': {'origin': 'learned', 'weight': 0.451312158903729}, 'Walc': {'origin': 'learned', 'weight': 0.4005429332616751}, 'health': {'origin': 'learned', 'weight': 0.2873495054103081}, 'absences': {'origin': 'learned', 'weight': -1.0538754156321408}, 'G1': {'origin': 'learned', 'weight': 1.261362346111696}, 'G2': {'origin': 'learned', 'weight': 0.18088756091335226}, 'G3': {'origin': 'learned', 'weight': -0.08860028396266117}}, 'Medu': {'address': {'origin': 'learned', 'weight': 5.282843496249485e-07}, 'famsize': {'origin': 'learned', 'weight': -8.376171747006237e-05}, 'Pstatus': {'origin': 'learned', 'weight': 7.664857242148944e-07}, 'Fedu': {'origin': 'learned', 'weight': 0.6253625161000721}, 'traveltime': {'origin': 'learned', 'weight': -1.4976973044455327e-05}, 'studytime': {'origin': 'learned', 'weight': 0.07663461056844137}, 'failures': {'origin': 'learned', 'weight': -8.47848862991425e-06}, 'schoolsup': {'origin': 'learned', 'weight': 1.4871605630041722e-06}, 'famsup': {'origin': 'learned', 'weight': 2.768426487726607e-06}, 'paid': {'origin': 'learned', 'weight': 4.306941634359122e-07}, 'activities': {'origin': 'learned', 'weight': 4.839327739872298e-06}, 'nursery': {'origin': 'learned', 'weight': 9.859417699637172e-07}, 'higher': {'origin': 'learned', 'weight': 1.2090653015743418e-07}, 'internet': {'origin': 'learned', 'weight': 3.826610819737762e-07}, 'romantic': {'origin': 'learned', 'weight': 1.7041739225182675e-05}, 'famrel': {'origin': 'learned', 'weight': 0.06395750625321515}, 'freetime': {'origin': 'learned', 'weight': 0.005298006953244488}, 'goout': {'origin': 'learned', 'weight': 0.017833992490542724}, 'Dalc': {'origin': 'learned', 'weight': 0.05639212133201029}, 'Walc': {'origin': 'learned', 'weight': -0.05655177993703371}, 'health': {'origin': 'learned', 'weight': -0.0017836759484594275}, 'absences': {'origin': 'learned', 'weight': -0.10963221670789629}, 'G1': {'origin': 'learned', 'weight': 0.3731879464225919}, 'G2': {'origin': 'learned', 'weight': 0.048587816372934696}, 'G3': {'origin': 'learned', 'weight': -0.04977786757469074}}, 'Fedu': {'address': {'origin': 'learned', 'weight': 1.815837863695999e-06}, 'famsize': {'origin': 'learned', 'weight': -5.875240692181356e-06}, 'Pstatus': {'origin': 'learned', 'weight': 1.0862756113952355e-06}, 'Medu': {'origin': 'learned', 'weight': 1.3815353478780808e-06}, 'traveltime': {'origin': 'learned', 'weight': 2.3458092007222387e-06}, 'studytime': {'origin': 'learned', 'weight': -0.002267727436488319}, 'failures': {'origin': 'learned', 'weight': -4.4896874864671566e-06}, 'schoolsup': {'origin': 'learned', 'weight': 3.5966507196187998e-06}, 'famsup': {'origin': 'learned', 'weight': 8.380912481855755e-06}, 'paid': {'origin': 'learned', 'weight': 1.5972940923620563e-06}, 'activities': {'origin': 'learned', 'weight': 2.2202292453444777e-05}, 'nursery': {'origin': 'learned', 'weight': 3.836377734813915e-06}, 'higher': {'origin': 'learned', 'weight': 4.6588574867353284e-07}, 'internet': {'origin': 'learned', 'weight': 1.6062126461530145e-06}, 'romantic': {'origin': 'learned', 'weight': 6.776538544245963e-05}, 'famrel': {'origin': 'learned', 'weight': 0.09036740104688158}, 'freetime': {'origin': 'learned', 'weight': 0.07269279661945031}, 'goout': {'origin': 'learned', 'weight': 0.001521336398273317}, 'Dalc': {'origin': 'learned', 'weight': 0.06540063043992946}, 'Walc': {'origin': 'learned', 'weight': 0.12603842388100064}, 'health': {'origin': 'learned', 'weight': 0.09655752353619704}, 'absences': {'origin': 'learned', 'weight': 0.34662147120177766}, 'G1': {'origin': 'learned', 'weight': 0.2457622670411357}, 'G2': {'origin': 'learned', 'weight': 0.06740156244799099}, 'G3': {'origin': 'learned', 'weight': 0.04209668187865408}}, 'traveltime': {'address': {'origin': 'learned', 'weight': -3.2083752911421134e-08}, 'famsize': {'origin': 'learned', 'weight': 5.681875851702312e-07}, 'Pstatus': {'origin': 'learned', 'weight': 1.5254924959846107e-07}, 'Medu': {'origin': 'learned', 'weight': -0.05682679496770537}, 'Fedu': {'origin': 'learned', 'weight': 0.04369105682484006}, 'studytime': {'origin': 'learned', 'weight': 0.14665592285551024}, 'failures': {'origin': 'learned', 'weight': 8.390113681439373e-07}, 'schoolsup': {'origin': 'learned', 'weight': 3.572657993912356e-06}, 'famsup': {'origin': 'learned', 'weight': 6.7280883915310845e-06}, 'paid': {'origin': 'learned', 'weight': 1.1047233320614985e-06}, 'activities': {'origin': 'learned', 'weight': 1.5182162182595177e-05}, 'nursery': {'origin': 'learned', 'weight': 1.4616510424530478e-06}, 'higher': {'origin': 'learned', 'weight': 2.1338297753062791e-07}, 'internet': {'origin': 'learned', 'weight': 1.6460904743183209e-06}, 'romantic': {'origin': 'learned', 'weight': 1.3548531245438947e-05}, 'famrel': {'origin': 'learned', 'weight': 0.3652619258538022}, 'freetime': {'origin': 'learned', 'weight': 0.1386601673406505}, 'goout': {'origin': 'learned', 'weight': 0.14543707996940677}, 'Dalc': {'origin': 'learned', 'weight': 0.2640464432914783}, 'Walc': {'origin': 'learned', 'weight': 0.1054311976437596}, 'health': {'origin': 'learned', 'weight': 0.05946039269548516}, 'absences': {'origin': 'learned', 'weight': 0.31742677251596246}, 'G1': {'origin': 'learned', 'weight': 0.4258522757563797}, 'G2': {'origin': 'learned', 'weight': 0.0452125282264167}, 'G3': {'origin': 'learned', 'weight': 0.1472529805083419}}, 'studytime': {'address': {'origin': 'learned', 'weight': 1.2094798742837836e-06}, 'famsize': {'origin': 'learned', 'weight': 2.2938931309765494e-06}, 'Pstatus': {'origin': 'learned', 'weight': 4.5152482925329287e-07}, 'Medu': {'origin': 'learned', 'weight': 1.0099464281901412e-05}, 'Fedu': {'origin': 'learned', 'weight': -0.000495670140147531}, 'traveltime': {'origin': 'learned', 'weight': 2.7298276113987395e-06}, 'failures': {'origin': 'learned', 'weight': -4.52614007711886e-07}, 'schoolsup': {'origin': 'learned', 'weight': 1.3187597528677218e-06}, 'famsup': {'origin': 'learned', 'weight': 3.733353224457675e-06}, 'paid': {'origin': 'learned', 'weight': 3.7336184729781297e-06}, 'activities': {'origin': 'learned', 'weight': 1.1962348457785248e-05}, 'nursery': {'origin': 'learned', 'weight': 3.5500670023818374e-06}, 'higher': {'origin': 'learned', 'weight': 2.3561892859955156e-07}, 'internet': {'origin': 'learned', 'weight': 2.96354399751265e-06}, 'romantic': {'origin': 'learned', 'weight': 1.3775916562081774e-05}, 'famrel': {'origin': 'learned', 'weight': 0.15816240290931505}, 'freetime': {'origin': 'learned', 'weight': 0.061672808424480724}, 'goout': {'origin': 'learned', 'weight': 0.050063594468249706}, 'Dalc': {'origin': 'learned', 'weight': -1.7407881648513562e-05}, 'Walc': {'origin': 'learned', 'weight': -0.13225283210928684}, 'health': {'origin': 'learned', 'weight': 0.044435607273602996}, 'absences': {'origin': 'learned', 'weight': -0.24449913460462702}, 'G1': {'origin': 'learned', 'weight': 0.8636139137063454}, 'G2': {'origin': 'learned', 'weight': 0.05362052988133593}, 'G3': {'origin': 'learned', 'weight': 0.07325427221999745}}, 'failures': {'address': {'origin': 'learned', 'weight': 1.0270730806788747e-06}, 'famsize': {'origin': 'learned', 'weight': 0.007199670534529419}, 'Pstatus': {'origin': 'learned', 'weight': 3.7113144071898173e-07}, 'Medu': {'origin': 'learned', 'weight': -0.05554902196378678}, 'Fedu': {'origin': 'learned', 'weight': -0.03634104972539488}, 'traveltime': {'origin': 'learned', 'weight': 0.28893299557926194}, 'studytime': {'origin': 'learned', 'weight': -0.036925581153895784}, 'schoolsup': {'origin': 'learned', 'weight': 1.2442168943478484e-06}, 'famsup': {'origin': 'learned', 'weight': 2.7970697872618514e-06}, 'paid': {'origin': 'learned', 'weight': 3.2799055993158386e-07}, 'activities': {'origin': 'learned', 'weight': 5.462903893005342e-06}, 'nursery': {'origin': 'learned', 'weight': 1.115736579162668e-06}, 'higher': {'origin': 'learned', 'weight': -1.583102592694493e-07}, 'internet': {'origin': 'learned', 'weight': -4.150375359058897e-08}, 'romantic': {'origin': 'learned', 'weight': 5.644847741993733e-06}, 'famrel': {'origin': 'learned', 'weight': 0.1668232709293059}, 'freetime': {'origin': 'learned', 'weight': 0.2757287584822249}, 'goout': {'origin': 'learned', 'weight': -0.00253721944936783}, 'Dalc': {'origin': 'learned', 'weight': 0.19852244938589078}, 'Walc': {'origin': 'learned', 'weight': 0.1110213039605426}, 'health': {'origin': 'learned', 'weight': 0.17934136094011674}, 'absences': {'origin': 'learned', 'weight': 0.9395791571697139}, 'G1': {'origin': 'learned', 'weight': -0.7734093106877317}, 'G2': {'origin': 'learned', 'weight': -0.17877938791798662}, 'G3': {'origin': 'learned', 'weight': -0.15972379098765793}}, 'schoolsup': {'address': {'origin': 'learned', 'weight': 0.09016610695015827}, 'famsize': {'origin': 'learned', 'weight': -0.07969030328801704}, 'Pstatus': {'origin': 'learned', 'weight': 0.0031060892594583374}, 'Medu': {'origin': 'learned', 'weight': -0.14973724028142785}, 'Fedu': {'origin': 'learned', 'weight': 0.111206285588392}, 'traveltime': {'origin': 'learned', 'weight': -0.05461326354951528}, 'studytime': {'origin': 'learned', 'weight': 0.2323474711325423}, 'failures': {'origin': 'learned', 'weight': 0.05344254788762017}, 'famsup': {'origin': 'learned', 'weight': 0.43115271308130015}, 'paid': {'origin': 'learned', 'weight': 4.393230469914194e-07}, 'activities': {'origin': 'learned', 'weight': 3.3289576319408384e-06}, 'nursery': {'origin': 'learned', 'weight': 0.21898204604390092}, 'higher': {'origin': 'learned', 'weight': 0.15113701551678627}, 'internet': {'origin': 'learned', 'weight': 0.04153209516996423}, 'romantic': {'origin': 'learned', 'weight': 1.741729645205567e-05}, 'famrel': {'origin': 'learned', 'weight': 0.013400176227771085}, 'freetime': {'origin': 'learned', 'weight': 0.08146892483723561}, 'goout': {'origin': 'learned', 'weight': -0.054048281147243506}, 'Dalc': {'origin': 'learned', 'weight': 0.030431446056897765}, 'Walc': {'origin': 'learned', 'weight': -0.28625533228773004}, 'health': {'origin': 'learned', 'weight': 0.16814364990171213}, 'absences': {'origin': 'learned', 'weight': -0.44169320558277186}, 'G1': {'origin': 'learned', 'weight': -0.8015184747758134}, 'G2': {'origin': 'learned', 'weight': 0.01756848085425741}, 'G3': {'origin': 'learned', 'weight': -0.16017431148807354}}, 'famsup': {'address': {'origin': 'learned', 'weight': 0.10427386381413724}, 'famsize': {'origin': 'learned', 'weight': 0.0016122619388671963}, 'Pstatus': {'origin': 'learned', 'weight': 0.08467752097138515}, 'Medu': {'origin': 'learned', 'weight': 0.2712033095860632}, 'Fedu': {'origin': 'learned', 'weight': 0.14573161333959725}, 'traveltime': {'origin': 'learned', 'weight': 0.09728374298715864}, 'studytime': {'origin': 'learned', 'weight': 0.266362204840018}, 'failures': {'origin': 'learned', 'weight': 0.08031678051890989}, 'schoolsup': {'origin': 'learned', 'weight': 1.633685547630518e-07}, 'paid': {'origin': 'learned', 'weight': 1.7014085331477617e-07}, 'activities': {'origin': 'learned', 'weight': 7.251013741149529e-07}, 'nursery': {'origin': 'learned', 'weight': 0.49493689368622484}, 'higher': {'origin': 'learned', 'weight': 0.17814403224742134}, 'internet': {'origin': 'learned', 'weight': 0.27715008710483463}, 'romantic': {'origin': 'learned', 'weight': 1.212623696766134e-06}, 'famrel': {'origin': 'learned', 'weight': 0.09564586270588174}, 'freetime': {'origin': 'learned', 'weight': 0.08487609151687552}, 'goout': {'origin': 'learned', 'weight': 0.09664059894202708}, 'Dalc': {'origin': 'learned', 'weight': 0.01911615512884646}, 'Walc': {'origin': 'learned', 'weight': -0.08227553368062841}, 'health': {'origin': 'learned', 'weight': 0.1009039626224132}, 'absences': {'origin': 'learned', 'weight': 0.6753957856896687}, 'G1': {'origin': 'learned', 'weight': 0.013792402912843525}, 'G2': {'origin': 'learned', 'weight': -0.008335288023269384}, 'G3': {'origin': 'learned', 'weight': 0.11012660720124419}}, 'paid': {'address': {'origin': 'learned', 'weight': -0.06226780216318523}, 'famsize': {'origin': 'learned', 'weight': -0.08662176398113904}, 'Pstatus': {'origin': 'learned', 'weight': 0.01940453653643334}, 'Medu': {'origin': 'learned', 'weight': 0.45092087317544877}, 'Fedu': {'origin': 'learned', 'weight': 0.07819729062203296}, 'traveltime': {'origin': 'learned', 'weight': -0.1751929065462438}, 'studytime': {'origin': 'learned', 'weight': -0.06792582697060526}, 'failures': {'origin': 'learned', 'weight': 0.19488310269441256}, 'schoolsup': {'origin': 'learned', 'weight': 0.10971256665441963}, 'famsup': {'origin': 'learned', 'weight': 0.3711694184171664}, 'activities': {'origin': 'learned', 'weight': 0.42980667486373997}, 'nursery': {'origin': 'learned', 'weight': 0.10713624144249709}, 'higher': {'origin': 'learned', 'weight': 0.0651615011059292}, 'internet': {'origin': 'learned', 'weight': 0.06155932087550792}, 'romantic': {'origin': 'learned', 'weight': 6.219147593514768e-06}, 'famrel': {'origin': 'learned', 'weight': 0.07276395951434235}, 'freetime': {'origin': 'learned', 'weight': -0.397084583455957}, 'goout': {'origin': 'learned', 'weight': -0.05554731045279839}, 'Dalc': {'origin': 'learned', 'weight': 0.18947644768941185}, 'Walc': {'origin': 'learned', 'weight': 0.03286301430594966}, 'health': {'origin': 'learned', 'weight': 0.2884379850406954}, 'absences': {'origin': 'learned', 'weight': -1.0534625350951718}, 'G1': {'origin': 'learned', 'weight': -0.7476665468841639}, 'G2': {'origin': 'learned', 'weight': 0.215077113364691}, 'G3': {'origin': 'learned', 'weight': -0.19159897136433737}}, 'activities': {'address': {'origin': 'learned', 'weight': 0.05553758017558176}, 'famsize': {'origin': 'learned', 'weight': 0.020024417715390045}, 'Pstatus': {'origin': 'learned', 'weight': 0.1186650900039901}, 'Medu': {'origin': 'learned', 'weight': 0.24111978808014004}, 'Fedu': {'origin': 'learned', 'weight': 0.022242975459254674}, 'traveltime': {'origin': 'learned', 'weight': 0.008463822567962324}, 'studytime': {'origin': 'learned', 'weight': 0.12516307931862}, 'failures': {'origin': 'learned', 'weight': 0.045406510982519854}, 'schoolsup': {'origin': 'learned', 'weight': 0.07942221196339495}, 'famsup': {'origin': 'learned', 'weight': 0.40747787530276136}, 'paid': {'origin': 'learned', 'weight': 1.0579930515164717e-07}, 'nursery': {'origin': 'learned', 'weight': 0.3870752878517111}, 'higher': {'origin': 'learned', 'weight': 0.10140915280647488}, 'internet': {'origin': 'learned', 'weight': 0.22115620514055448}, 'romantic': {'origin': 'learned', 'weight': 5.062885962223394e-07}, 'famrel': {'origin': 'learned', 'weight': 0.1060097717426425}, 'freetime': {'origin': 'learned', 'weight': 0.29025194859764786}, 'goout': {'origin': 'learned', 'weight': 0.053016213518201454}, 'Dalc': {'origin': 'learned', 'weight': 0.03508084451564856}, 'Walc': {'origin': 'learned', 'weight': 0.05822411086046015}, 'health': {'origin': 'learned', 'weight': -0.04472072932931432}, 'absences': {'origin': 'learned', 'weight': -0.011557604864954631}, 'G1': {'origin': 'learned', 'weight': 0.13356290095617598}, 'G2': {'origin': 'learned', 'weight': -0.02719253860768766}, 'G3': {'origin': 'learned', 'weight': 0.008521962648982792}}, 'nursery': {'address': {'origin': 'learned', 'weight': 0.2776178205344719}, 'famsize': {'origin': 'learned', 'weight': 0.20181916953441106}, 'Pstatus': {'origin': 'learned', 'weight': 0.18458724734437718}, 'Medu': {'origin': 'learned', 'weight': 0.5239103813400171}, 'Fedu': {'origin': 'learned', 'weight': 0.0576652012939855}, 'traveltime': {'origin': 'learned', 'weight': 0.3359494704671782}, 'studytime': {'origin': 'learned', 'weight': 0.18535635699631886}, 'failures': {'origin': 'learned', 'weight': 0.0750746154121407}, 'schoolsup': {'origin': 'learned', 'weight': 4.4501014882221276e-07}, 'famsup': {'origin': 'learned', 'weight': 5.245322452922104e-07}, 'paid': {'origin': 'learned', 'weight': 5.830128592885166e-07}, 'activities': {'origin': 'learned', 'weight': 8.75089591986338e-07}, 'higher': {'origin': 'learned', 'weight': 0.33856473446106944}, 'internet': {'origin': 'learned', 'weight': 0.4242928819958667}, 'romantic': {'origin': 'learned', 'weight': 2.139012622741077e-06}, 'famrel': {'origin': 'learned', 'weight': 0.432569121650298}, 'freetime': {'origin': 'learned', 'weight': 0.18200415195307637}, 'goout': {'origin': 'learned', 'weight': 0.17017617661645093}, 'Dalc': {'origin': 'learned', 'weight': -0.05664828517064359}, 'Walc': {'origin': 'learned', 'weight': 0.017727713239038333}, 'health': {'origin': 'learned', 'weight': 0.1833351895084601}, 'absences': {'origin': 'learned', 'weight': 0.19424952439476387}, 'G1': {'origin': 'learned', 'weight': 0.26458992819928057}, 'G2': {'origin': 'learned', 'weight': 0.07008782622305502}, 'G3': {'origin': 'learned', 'weight': -0.04178769441684207}}, 'higher': {'address': {'origin': 'learned', 'weight': 7.851783367975633e-07}, 'famsize': {'origin': 'learned', 'weight': 0.17370961720916422}, 'Pstatus': {'origin': 'learned', 'weight': 0.42470020866871444}, 'Medu': {'origin': 'learned', 'weight': 0.9842407795725915}, 'Fedu': {'origin': 'learned', 'weight': 0.28719837310478313}, 'traveltime': {'origin': 'learned', 'weight': 0.6652075929820775}, 'studytime': {'origin': 'learned', 'weight': 0.6614250646852067}, 'failures': {'origin': 'learned', 'weight': -0.30470801802731773}, 'schoolsup': {'origin': 'learned', 'weight': 1.2479890798999761e-06}, 'famsup': {'origin': 'learned', 'weight': 2.9132190513716887e-06}, 'paid': {'origin': 'learned', 'weight': 2.7674708199764802e-06}, 'activities': {'origin': 'learned', 'weight': 7.063695630694698e-06}, 'nursery': {'origin': 'learned', 'weight': 9.369537748463454e-07}, 'internet': {'origin': 'learned', 'weight': 7.463964327612281e-07}, 'romantic': {'origin': 'learned', 'weight': 2.268046145982143e-05}, 'famrel': {'origin': 'learned', 'weight': 0.749421075800239}, 'freetime': {'origin': 'learned', 'weight': 0.05992191532028243}, 'goout': {'origin': 'learned', 'weight': -0.02944249552655697}, 'Dalc': {'origin': 'learned', 'weight': -0.06561934921537634}, 'Walc': {'origin': 'learned', 'weight': 0.2709113403707566}, 'health': {'origin': 'learned', 'weight': 0.460475844352154}, 'absences': {'origin': 'learned', 'weight': -0.4644399619110806}, 'G1': {'origin': 'learned', 'weight': 2.6906165356962597}, 'G2': {'origin': 'learned', 'weight': 0.21293172852077402}, 'G3': {'origin': 'learned', 'weight': 0.161696919211617}}, 'internet': {'address': {'origin': 'learned', 'weight': 0.40328532019811464}, 'famsize': {'origin': 'learned', 'weight': 0.08161029156084386}, 'Pstatus': {'origin': 'learned', 'weight': 0.20073374119007015}, 'Medu': {'origin': 'learned', 'weight': 0.6875462651121823}, 'Fedu': {'origin': 'learned', 'weight': 0.06454075511391491}, 'traveltime': {'origin': 'learned', 'weight': -0.021094282505113388}, 'studytime': {'origin': 'learned', 'weight': 0.09306481319152346}, 'failures': {'origin': 'learned', 'weight': -0.015305344026746737}, 'schoolsup': {'origin': 'learned', 'weight': 1.7593655699762522e-06}, 'famsup': {'origin': 'learned', 'weight': 1.2448178984658832e-06}, 'paid': {'origin': 'learned', 'weight': 1.4622746367588082e-06}, 'activities': {'origin': 'learned', 'weight': 2.270135281570907e-06}, 'nursery': {'origin': 'learned', 'weight': 4.823286857399146e-07}, 'higher': {'origin': 'learned', 'weight': 0.27561946030947526}, 'romantic': {'origin': 'learned', 'weight': 5.241075220842723e-06}, 'famrel': {'origin': 'learned', 'weight': 0.40830632335954425}, 'freetime': {'origin': 'learned', 'weight': 0.19475274397573786}, 'goout': {'origin': 'learned', 'weight': 0.1408710805149382}, 'Dalc': {'origin': 'learned', 'weight': 0.2086038568514957}, 'Walc': {'origin': 'learned', 'weight': 0.1663542314573771}, 'health': {'origin': 'learned', 'weight': -0.12331190291514839}, 'absences': {'origin': 'learned', 'weight': 0.8369080746968736}, 'G1': {'origin': 'learned', 'weight': 0.4693377785294991}, 'G2': {'origin': 'learned', 'weight': 0.10416797222379809}, 'G3': {'origin': 'learned', 'weight': 0.12476082994216223}}, 'romantic': {'address': {'origin': 'learned', 'weight': 0.03449641423060724}, 'famsize': {'origin': 'learned', 'weight': 0.0001242279611122574}, 'Pstatus': {'origin': 'learned', 'weight': 0.03882760026404552}, 'Medu': {'origin': 'learned', 'weight': 0.057553976531306665}, 'Fedu': {'origin': 'learned', 'weight': -0.038502546594630475}, 'traveltime': {'origin': 'learned', 'weight': 0.14329667201511975}, 'studytime': {'origin': 'learned', 'weight': 0.15562427843420687}, 'failures': {'origin': 'learned', 'weight': 0.10425856564537055}, 'schoolsup': {'origin': 'learned', 'weight': 0.014368894340047815}, 'famsup': {'origin': 'learned', 'weight': 0.3147106400752427}, 'paid': {'origin': 'learned', 'weight': 0.04724004434882376}, 'activities': {'origin': 'learned', 'weight': 0.4895721690598813}, 'nursery': {'origin': 'learned', 'weight': 0.2448302568893097}, 'higher': {'origin': 'learned', 'weight': 0.013855780556472706}, 'internet': {'origin': 'learned', 'weight': 0.14405028246426685}, 'famrel': {'origin': 'learned', 'weight': 0.09273389200751765}, 'freetime': {'origin': 'learned', 'weight': 0.12148123441125036}, 'goout': {'origin': 'learned', 'weight': 0.011833625417886233}, 'Dalc': {'origin': 'learned', 'weight': 0.17526816121879552}, 'Walc': {'origin': 'learned', 'weight': -0.08849224803371417}, 'health': {'origin': 'learned', 'weight': 0.09235839989213118}, 'absences': {'origin': 'learned', 'weight': 0.7593034494873926}, 'G1': {'origin': 'learned', 'weight': 0.04875311772928067}, 'G2': {'origin': 'learned', 'weight': -0.039529109530973716}, 'G3': {'origin': 'learned', 'weight': -0.0005487024932422538}}, 'famrel': {'address': {'origin': 'learned', 'weight': 1.320897881340788e-06}, 'famsize': {'origin': 'learned', 'weight': 8.77451264318084e-07}, 'Pstatus': {'origin': 'learned', 'weight': 1.846478796364456e-07}, 'Medu': {'origin': 'learned', 'weight': 1.966155554661421e-05}, 'Fedu': {'origin': 'learned', 'weight': 5.614649983118622e-06}, 'traveltime': {'origin': 'learned', 'weight': 1.2821620220563868e-06}, 'studytime': {'origin': 'learned', 'weight': 2.7325071082731085e-06}, 'failures': {'origin': 'learned', 'weight': 1.8774318511130135e-06}, 'schoolsup': {'origin': 'learned', 'weight': 7.748541219982958e-06}, 'famsup': {'origin': 'learned', 'weight': 1.0392942107720905e-05}, 'paid': {'origin': 'learned', 'weight': 6.725986004009021e-06}, 'activities': {'origin': 'learned', 'weight': 1.7103940193342104e-05}, 'nursery': {'origin': 'learned', 'weight': 1.8503775845644034e-06}, 'higher': {'origin': 'learned', 'weight': 3.11903271403777e-07}, 'internet': {'origin': 'learned', 'weight': 1.1560838230536603e-06}, 'romantic': {'origin': 'learned', 'weight': 3.644736374916043e-05}, 'freetime': {'origin': 'learned', 'weight': 0.31156532861814135}, 'goout': {'origin': 'learned', 'weight': 0.13688329678438912}, 'Dalc': {'origin': 'learned', 'weight': 8.974158916716448e-06}, 'Walc': {'origin': 'learned', 'weight': 0.012488501523243383}, 'health': {'origin': 'learned', 'weight': 0.32535235552165176}, 'absences': {'origin': 'learned', 'weight': 0.029534730152577033}, 'G1': {'origin': 'learned', 'weight': 0.46833609431305073}, 'G2': {'origin': 'learned', 'weight': 0.20116104297386833}, 'G3': {'origin': 'learned', 'weight': -0.024238569511162412}}, 'freetime': {'address': {'origin': 'learned', 'weight': 4.999315254151007e-06}, 'famsize': {'origin': 'learned', 'weight': 7.565108486278707e-06}, 'Pstatus': {'origin': 'learned', 'weight': 9.210757723189831e-07}, 'Medu': {'origin': 'learned', 'weight': 5.3045604346644666e-05}, 'Fedu': {'origin': 'learned', 'weight': 1.0989037361421973e-05}, 'traveltime': {'origin': 'learned', 'weight': 5.4929092719122535e-06}, 'studytime': {'origin': 'learned', 'weight': 5.999391678181635e-06}, 'failures': {'origin': 'learned', 'weight': 1.454765326837019e-06}, 'schoolsup': {'origin': 'learned', 'weight': 1.083118372234952e-05}, 'famsup': {'origin': 'learned', 'weight': 2.9264384487782554e-05}, 'paid': {'origin': 'learned', 'weight': 4.7266131590172746e-07}, 'activities': {'origin': 'learned', 'weight': 7.199372883872205e-06}, 'nursery': {'origin': 'learned', 'weight': 7.151725171424487e-06}, 'higher': {'origin': 'learned', 'weight': 2.4368058171397756e-06}, 'internet': {'origin': 'learned', 'weight': 3.6712820497747034e-06}, 'romantic': {'origin': 'learned', 'weight': 2.6581035887039415e-05}, 'famrel': {'origin': 'learned', 'weight': 2.6864503278375758e-06}, 'goout': {'origin': 'learned', 'weight': 0.3402337019417903}, 'Dalc': {'origin': 'learned', 'weight': 9.033290147904766e-06}, 'Walc': {'origin': 'learned', 'weight': 5.723497269328464e-06}, 'health': {'origin': 'learned', 'weight': 0.20359128011716196}, 'absences': {'origin': 'learned', 'weight': -0.13258912399887035}, 'G1': {'origin': 'learned', 'weight': 0.15893694608957573}, 'G2': {'origin': 'learned', 'weight': -0.021466939129440744}, 'G3': {'origin': 'learned', 'weight': -0.035291910715639876}}, 'goout': {'address': {'origin': 'learned', 'weight': 3.2035805298097187e-06}, 'famsize': {'origin': 'learned', 'weight': 2.860011965556905e-06}, 'Pstatus': {'origin': 'learned', 'weight': 3.2360205696198744e-06}, 'Medu': {'origin': 'learned', 'weight': 0.00013893787430084464}, 'Fedu': {'origin': 'learned', 'weight': 3.500255190181704e-05}, 'traveltime': {'origin': 'learned', 'weight': 7.206819224813103e-06}, 'studytime': {'origin': 'learned', 'weight': 5.392816587318543e-06}, 'failures': {'origin': 'learned', 'weight': 1.2758953810800162e-05}, 'schoolsup': {'origin': 'learned', 'weight': 9.292721765645084e-06}, 'famsup': {'origin': 'learned', 'weight': 3.142034075725276e-05}, 'paid': {'origin': 'learned', 'weight': 6.015041527997529e-06}, 'activities': {'origin': 'learned', 'weight': 4.984497634306652e-05}, 'nursery': {'origin': 'learned', 'weight': 1.0622247426374497e-05}, 'higher': {'origin': 'learned', 'weight': 6.733122212252568e-06}, 'internet': {'origin': 'learned', 'weight': 6.996845346414707e-06}, 'romantic': {'origin': 'learned', 'weight': 0.00014000699129624396}, 'famrel': {'origin': 'learned', 'weight': 8.279250568554317e-06}, 'freetime': {'origin': 'learned', 'weight': 2.2300812352732997e-06}, 'Dalc': {'origin': 'learned', 'weight': 4.8560363036115805e-06}, 'Walc': {'origin': 'learned', 'weight': 2.1472173559096028e-06}, 'health': {'origin': 'learned', 'weight': -0.12015368066308832}, 'absences': {'origin': 'learned', 'weight': 0.22748994743278778}, 'G1': {'origin': 'learned', 'weight': 0.0725254040091578}, 'G2': {'origin': 'learned', 'weight': -0.008887013971329476}, 'G3': {'origin': 'learned', 'weight': -0.005467748034587408}}, 'Dalc': {'address': {'origin': 'learned', 'weight': 2.443914771173288e-06}, 'famsize': {'origin': 'learned', 'weight': 6.124775682118712e-07}, 'Pstatus': {'origin': 'learned', 'weight': 3.3480538042122376e-07}, 'Medu': {'origin': 'learned', 'weight': 1.8941343308167783e-05}, 'Fedu': {'origin': 'learned', 'weight': 6.684651844691612e-06}, 'traveltime': {'origin': 'learned', 'weight': 1.6720888589429364e-06}, 'studytime': {'origin': 'learned', 'weight': -0.04079588249535337}, 'failures': {'origin': 'learned', 'weight': 1.5180401053457686e-06}, 'schoolsup': {'origin': 'learned', 'weight': 2.6577884822509986e-05}, 'famsup': {'origin': 'learned', 'weight': 3.898305342873185e-05}, 'paid': {'origin': 'learned', 'weight': 1.3187861051116028e-06}, 'activities': {'origin': 'learned', 'weight': 4.86850586028225e-05}, 'nursery': {'origin': 'learned', 'weight': 9.098998339948322e-06}, 'higher': {'origin': 'learned', 'weight': 1.3772195017901158e-06}, 'internet': {'origin': 'learned', 'weight': 1.9892730666634255e-06}, 'romantic': {'origin': 'learned', 'weight': 1.1085710188018912e-05}, 'famrel': {'origin': 'learned', 'weight': 0.061860074406191755}, 'freetime': {'origin': 'learned', 'weight': 0.08959510517136154}, 'goout': {'origin': 'learned', 'weight': -0.0024505554268309045}, 'Walc': {'origin': 'learned', 'weight': 0.8623769618608512}, 'health': {'origin': 'learned', 'weight': 0.0062315200782290985}, 'absences': {'origin': 'learned', 'weight': 0.6285293747934196}, 'G1': {'origin': 'learned', 'weight': -0.1679903202090344}, 'G2': {'origin': 'learned', 'weight': 0.01828514198351367}, 'G3': {'origin': 'learned', 'weight': -0.06069763850187142}}, 'Walc': {'address': {'origin': 'learned', 'weight': 2.3235931090372038e-06}, 'famsize': {'origin': 'learned', 'weight': 9.661335752092414e-07}, 'Pstatus': {'origin': 'learned', 'weight': 4.580593050516383e-07}, 'Medu': {'origin': 'learned', 'weight': 1.0234019307479275e-05}, 'Fedu': {'origin': 'learned', 'weight': 5.230869729896622e-06}, 'traveltime': {'origin': 'learned', 'weight': 3.823707461640614e-06}, 'studytime': {'origin': 'learned', 'weight': -3.7312092819954272e-06}, 'failures': {'origin': 'learned', 'weight': 3.1858816041837672e-06}, 'schoolsup': {'origin': 'learned', 'weight': 6.602704056446805e-07}, 'famsup': {'origin': 'learned', 'weight': 2.462099835786531e-05}, 'paid': {'origin': 'learned', 'weight': 4.096182615608204e-06}, 'activities': {'origin': 'learned', 'weight': 4.679631804837704e-05}, 'nursery': {'origin': 'learned', 'weight': 1.4819511531044937e-05}, 'higher': {'origin': 'learned', 'weight': 1.0224844526732827e-06}, 'internet': {'origin': 'learned', 'weight': 3.2089637875986894e-06}, 'romantic': {'origin': 'learned', 'weight': 2.529025287342515e-05}, 'famrel': {'origin': 'learned', 'weight': -2.572005415955528e-05}, 'freetime': {'origin': 'learned', 'weight': 0.1213001152355078}, 'goout': {'origin': 'learned', 'weight': 0.3524600102352628}, 'Dalc': {'origin': 'learned', 'weight': 6.927723939556109e-07}, 'health': {'origin': 'learned', 'weight': 0.22910017223115414}, 'absences': {'origin': 'learned', 'weight': 0.28212912867979606}, 'G1': {'origin': 'learned', 'weight': 0.01628754240663206}, 'G2': {'origin': 'learned', 'weight': -0.028336314998879123}, 'G3': {'origin': 'learned', 'weight': -0.017052027248871705}}, 'health': {'address': {'origin': 'learned', 'weight': 2.495006069707716e-06}, 'famsize': {'origin': 'learned', 'weight': 4.5809455483301075e-06}, 'Pstatus': {'origin': 'learned', 'weight': 9.494811331021372e-07}, 'Medu': {'origin': 'learned', 'weight': 5.323859031710839e-05}, 'Fedu': {'origin': 'learned', 'weight': 8.728697764773375e-06}, 'traveltime': {'origin': 'learned', 'weight': 1.0242635060847743e-05}, 'studytime': {'origin': 'learned', 'weight': 8.714528708551217e-06}, 'failures': {'origin': 'learned', 'weight': 2.806745787568456e-06}, 'schoolsup': {'origin': 'learned', 'weight': 3.8134498853512872e-06}, 'famsup': {'origin': 'learned', 'weight': 2.320637753493311e-05}, 'paid': {'origin': 'learned', 'weight': 1.3045542586857709e-06}, 'activities': {'origin': 'learned', 'weight': 5.101290264386016e-05}, 'nursery': {'origin': 'learned', 'weight': 7.240116351111648e-06}, 'higher': {'origin': 'learned', 'weight': 6.676523819363924e-07}, 'internet': {'origin': 'learned', 'weight': 4.782931502866295e-06}, 'romantic': {'origin': 'learned', 'weight': 6.18192581736639e-05}, 'famrel': {'origin': 'learned', 'weight': 2.7931909257193434e-06}, 'freetime': {'origin': 'learned', 'weight': 2.8779314964966107e-06}, 'goout': {'origin': 'learned', 'weight': -5.738929894237622e-06}, 'Dalc': {'origin': 'learned', 'weight': 6.5806594432733315e-06}, 'Walc': {'origin': 'learned', 'weight': 2.5242442268968173e-06}, 'absences': {'origin': 'learned', 'weight': 0.013270440047704299}, 'G1': {'origin': 'learned', 'weight': 0.09831680087724673}, 'G2': {'origin': 'learned', 'weight': -0.0655360822154847}, 'G3': {'origin': 'learned', 'weight': -0.03549672945498936}}, 'absences': {'address': {'origin': 'learned', 'weight': 2.1954756979199574e-07}, 'famsize': {'origin': 'learned', 'weight': 8.597580220229035e-07}, 'Pstatus': {'origin': 'learned', 'weight': 3.110979370027898e-08}, 'Medu': {'origin': 'learned', 'weight': 3.818433288195618e-06}, 'Fedu': {'origin': 'learned', 'weight': 1.8252677120908404e-06}, 'traveltime': {'origin': 'learned', 'weight': 2.2660262196440774e-06}, 'studytime': {'origin': 'learned', 'weight': -1.6241967207249302e-06}, 'failures': {'origin': 'learned', 'weight': 3.1040475703698455e-07}, 'schoolsup': {'origin': 'learned', 'weight': 3.2795583819598026e-07}, 'famsup': {'origin': 'learned', 'weight': 1.2319092982466107e-06}, 'paid': {'origin': 'learned', 'weight': 6.232694334298974e-08}, 'activities': {'origin': 'learned', 'weight': 6.813282419837235e-06}, 'nursery': {'origin': 'learned', 'weight': 1.783222076390664e-06}, 'higher': {'origin': 'learned', 'weight': 5.590376239583715e-08}, 'internet': {'origin': 'learned', 'weight': 3.687447609686423e-07}, 'romantic': {'origin': 'learned', 'weight': 1.6291233178806432e-06}, 'famrel': {'origin': 'learned', 'weight': 6.761395164008487e-06}, 'freetime': {'origin': 'learned', 'weight': -2.8147000352287287e-06}, 'goout': {'origin': 'learned', 'weight': 2.98875965846704e-06}, 'Dalc': {'origin': 'learned', 'weight': 1.2537933032705393e-06}, 'Walc': {'origin': 'learned', 'weight': 2.9049481240489784e-06}, 'health': {'origin': 'learned', 'weight': -2.3873787462029974e-05}, 'G1': {'origin': 'learned', 'weight': -1.5031127212036804e-06}, 'G2': {'origin': 'learned', 'weight': 3.886996614933009e-06}, 'G3': {'origin': 'learned', 'weight': 3.987948656636059e-06}}, 'G1': {'address': {'origin': 'learned', 'weight': 4.145635565322556e-07}, 'famsize': {'origin': 'learned', 'weight': 4.231758239400621e-07}, 'Pstatus': {'origin': 'learned', 'weight': 1.2192523374411585e-07}, 'Medu': {'origin': 'learned', 'weight': 3.524468719738307e-06}, 'Fedu': {'origin': 'learned', 'weight': 2.655572153653365e-06}, 'traveltime': {'origin': 'learned', 'weight': 1.6493706472793821e-06}, 'studytime': {'origin': 'learned', 'weight': 5.880507684560454e-07}, 'failures': {'origin': 'learned', 'weight': -1.7871574230049647e-07}, 'schoolsup': {'origin': 'learned', 'weight': 4.865957647916266e-07}, 'famsup': {'origin': 'learned', 'weight': 7.719161908753132e-06}, 'paid': {'origin': 'learned', 'weight': 4.879860760979429e-07}, 'activities': {'origin': 'learned', 'weight': 1.573168543985265e-05}, 'nursery': {'origin': 'learned', 'weight': 2.2310985066482208e-06}, 'higher': {'origin': 'learned', 'weight': 1.1238345971304325e-07}, 'internet': {'origin': 'learned', 'weight': 1.1594765224713857e-06}, 'romantic': {'origin': 'learned', 'weight': 4.5568396125773596e-05}, 'famrel': {'origin': 'learned', 'weight': 2.1548227065399565e-06}, 'freetime': {'origin': 'learned', 'weight': 5.557825534741226e-06}, 'goout': {'origin': 'learned', 'weight': 9.449183937356098e-06}, 'Dalc': {'origin': 'learned', 'weight': -1.5501567349024007e-06}, 'Walc': {'origin': 'learned', 'weight': 5.0681509628027555e-05}, 'health': {'origin': 'learned', 'weight': 1.4456180749546806e-05}, 'absences': {'origin': 'learned', 'weight': -0.16519243826107544}, 'G2': {'origin': 'learned', 'weight': 0.8893123602483163}, 'G3': {'origin': 'learned', 'weight': 0.1314622702860853}}, 'G2': {'address': {'origin': 'learned', 'weight': 1.0808731900149392e-06}, 'famsize': {'origin': 'learned', 'weight': 1.018204545261268e-06}, 'Pstatus': {'origin': 'learned', 'weight': 4.0197743788316634e-07}, 'Medu': {'origin': 'learned', 'weight': 9.147904181797066e-06}, 'Fedu': {'origin': 'learned', 'weight': 6.073498805912339e-06}, 'traveltime': {'origin': 'learned', 'weight': 4.277353370007445e-06}, 'studytime': {'origin': 'learned', 'weight': 1.4113913670578505e-06}, 'failures': {'origin': 'learned', 'weight': -5.18613014617815e-07}, 'schoolsup': {'origin': 'learned', 'weight': 1.3800602422165208e-06}, 'famsup': {'origin': 'learned', 'weight': 3.0220831125406032e-05}, 'paid': {'origin': 'learned', 'weight': 1.1816940754479807e-06}, 'activities': {'origin': 'learned', 'weight': 5.669885412547309e-05}, 'nursery': {'origin': 'learned', 'weight': 7.608200291011169e-06}, 'higher': {'origin': 'learned', 'weight': 1.9509765374517475e-07}, 'internet': {'origin': 'learned', 'weight': 3.3812595236012536e-06}, 'romantic': {'origin': 'learned', 'weight': 0.000163890714845625}, 'famrel': {'origin': 'learned', 'weight': 4.421633581782909e-06}, 'freetime': {'origin': 'learned', 'weight': 9.63198572344712e-06}, 'goout': {'origin': 'learned', 'weight': 2.416742610715618e-05}, 'Dalc': {'origin': 'learned', 'weight': -4.049949010417597e-06}, 'Walc': {'origin': 'learned', 'weight': 4.391655782041878e-06}, 'health': {'origin': 'learned', 'weight': 3.863184393270905e-06}, 'absences': {'origin': 'learned', 'weight': -0.12083364187284075}, 'G1': {'origin': 'learned', 'weight': 4.852215936739337e-06}, 'G3': {'origin': 'learned', 'weight': 0.884705682463779}}, 'G3': {'address': {'origin': 'learned', 'weight': 2.8997294244065144e-06}, 'famsize': {'origin': 'learned', 'weight': 3.6447543713365855e-06}, 'Pstatus': {'origin': 'learned', 'weight': 1.2383169619592981e-06}, 'Medu': {'origin': 'learned', 'weight': 2.7181742380645266e-05}, 'Fedu': {'origin': 'learned', 'weight': 1.7927492482726562e-05}, 'traveltime': {'origin': 'learned', 'weight': 8.956896659868888e-06}, 'studytime': {'origin': 'learned', 'weight': 5.052203280123686e-06}, 'failures': {'origin': 'learned', 'weight': -1.621351356540549e-06}, 'schoolsup': {'origin': 'learned', 'weight': 3.7300833122935385e-06}, 'famsup': {'origin': 'learned', 'weight': 6.9595740834268e-05}, 'paid': {'origin': 'learned', 'weight': 2.618791872592911e-06}, 'activities': {'origin': 'learned', 'weight': 0.00019957011213946537}, 'nursery': {'origin': 'learned', 'weight': 2.8136654487595504e-05}, 'higher': {'origin': 'learned', 'weight': 7.976562142570407e-07}, 'internet': {'origin': 'learned', 'weight': 1.1023378253076663e-05}, 'romantic': {'origin': 'learned', 'weight': 0.0005007381639334503}, 'famrel': {'origin': 'learned', 'weight': 1.2436281655857373e-05}, 'freetime': {'origin': 'learned', 'weight': 1.4630621123820853e-05}, 'goout': {'origin': 'learned', 'weight': 8.885235654394119e-05}, 'Dalc': {'origin': 'learned', 'weight': -1.519052520577944e-05}, 'Walc': {'origin': 'learned', 'weight': -5.154448682834879e-06}, 'health': {'origin': 'learned', 'weight': -8.85746266481034e-07}, 'absences': {'origin': 'learned', 'weight': 0.2799693506960016}, 'G1': {'origin': 'learned', 'weight': 1.2269310076312509e-05}, 'G2': {'origin': 'learned', 'weight': 1.6073761334772817e-06}}})




```python
# Adjacency object holding the successors of each node
structureModelPruned.succ
```




    AdjacencyView({'address': {'absences': {'origin': 'learned', 'weight': 1.0400949529066366}, 'G1': {'origin': 'learned', 'weight': 1.006295091882122}}, 'famsize': {}, 'Pstatus': {'famrel': {'origin': 'learned', 'weight': 0.8402877660070628}, 'absences': {'origin': 'learned', 'weight': -1.0538754156321408}, 'G1': {'origin': 'learned', 'weight': 1.261362346111696}}, 'Medu': {}, 'Fedu': {}, 'traveltime': {}, 'studytime': {'G1': {'origin': 'learned', 'weight': 0.8636139137063454}}, 'failures': {'absences': {'origin': 'learned', 'weight': 0.9395791571697139}}, 'schoolsup': {'G1': {'origin': 'learned', 'weight': -0.8015184747758134}}, 'famsup': {}, 'paid': {'absences': {'origin': 'learned', 'weight': -1.0534625350951718}}, 'activities': {}, 'nursery': {}, 'higher': {'Medu': {'origin': 'learned', 'weight': 0.9842407795725915}, 'G1': {'origin': 'learned', 'weight': 2.6906165356962597}}, 'internet': {'absences': {'origin': 'learned', 'weight': 0.8369080746968736}}, 'romantic': {}, 'famrel': {}, 'freetime': {}, 'goout': {}, 'Dalc': {'Walc': {'origin': 'learned', 'weight': 0.8623769618608512}}, 'Walc': {}, 'health': {}, 'absences': {}, 'G1': {'G2': {'origin': 'learned', 'weight': 0.8893123602483163}}, 'G2': {'G3': {'origin': 'learned', 'weight': 0.884705682463779}}, 'G3': {}})




```python
structureModelLearned.has_edge(u = 'Fedu', v= 'famsup')
```




    True




```python
structureModelPruned.has_edge(u = 'Fedu', v= 'famsup')
```




    False




```python
structureModelLearned.has_edge(u = 'address', v= 'absences')
```




    True




```python
structureModelPruned.has_edge(u = 'address', v= 'absences')
```




    True




```python
structureModelLearned.get_edge_data(u = 'address', v= 'absences')
```




    {'origin': 'learned', 'weight': 1.0400949529066366}




```python
# NOTE: after pruning the weight doesn't change
structureModelPruned.get_edge_data(u = 'address', v= 'absences')
```




    {'origin': 'learned', 'weight': 1.0400949529066366}




```python
list(structureModelLearned.neighbors(n = 'address'))
```




    ['famsize',
     'Pstatus',
     'Medu',
     'Fedu',
     'traveltime',
     'studytime',
     'failures',
     'schoolsup',
     'famsup',
     'paid',
     'activities',
     'nursery',
     'higher',
     'internet',
     'romantic',
     'famrel',
     'freetime',
     'goout',
     'Dalc',
     'Walc',
     'health',
     'absences',
     'G1',
     'G2',
     'G3']




```python
list(structureModelPruned.neighbors(n = 'address'))
```




    ['absences', 'G1']




```python
# TODO: what does negative weight mean?
# TODO: why are weights not probabilities?
list(structureModelLearned.adjacency())[:2]
```




    [('address',
      {'famsize': {'origin': 'learned', 'weight': 0.07172400411745194},
       'Pstatus': {'origin': 'learned', 'weight': 0.027500652131841753},
       'Medu': {'origin': 'learned', 'weight': 0.4329609981782503},
       'Fedu': {'origin': 'learned', 'weight': 0.10940724573937048},
       'traveltime': {'origin': 'learned', 'weight': -0.3080468648891065},
       'studytime': {'origin': 'learned', 'weight': 0.22858517407180592},
       'failures': {'origin': 'learned', 'weight': 0.06633709792506814},
       'schoolsup': {'origin': 'learned', 'weight': 2.265558640319601e-06},
       'famsup': {'origin': 'learned', 'weight': 4.164128335492464e-06},
       'paid': {'origin': 'learned', 'weight': 2.6188325902813357e-06},
       'activities': {'origin': 'learned', 'weight': 8.921883360997223e-06},
       'nursery': {'origin': 'learned', 'weight': 1.0431757754516237e-06},
       'higher': {'origin': 'learned', 'weight': 0.2175470691398659},
       'internet': {'origin': 'learned', 'weight': 4.631899217412905e-07},
       'romantic': {'origin': 'learned', 'weight': 2.1163994047249527e-05},
       'famrel': {'origin': 'learned', 'weight': 0.2713375883408355},
       'freetime': {'origin': 'learned', 'weight': 0.11768720419459214},
       'goout': {'origin': 'learned', 'weight': 0.16392393831724242},
       'Dalc': {'origin': 'learned', 'weight': 0.11663243893798651},
       'Walc': {'origin': 'learned', 'weight': 0.16559963300289912},
       'health': {'origin': 'learned', 'weight': 0.20294893185551394},
       'absences': {'origin': 'learned', 'weight': 1.0400949529066366},
       'G1': {'origin': 'learned', 'weight': 1.006295091882122},
       'G2': {'origin': 'learned', 'weight': 0.15007496882413057},
       'G3': {'origin': 'learned', 'weight': 0.223096391377955}}),
     ('famsize',
      {'address': {'origin': 'learned', 'weight': 2.57364988344861e-06},
       'Pstatus': {'origin': 'learned', 'weight': -5.39386360384519e-07},
       'Medu': {'origin': 'learned', 'weight': -0.0016220902698672792},
       'Fedu': {'origin': 'learned', 'weight': -0.024651044459558742},
       'traveltime': {'origin': 'learned', 'weight': 0.25181986913147913},
       'studytime': {'origin': 'learned', 'weight': 0.07404468489673609},
       'failures': {'origin': 'learned', 'weight': -0.00011631802985936184},
       'schoolsup': {'origin': 'learned', 'weight': 7.582265421368856e-07},
       'famsup': {'origin': 'learned', 'weight': 8.083571741711851e-06},
       'paid': {'origin': 'learned', 'weight': 5.982031984826393e-07},
       'activities': {'origin': 'learned', 'weight': 1.1369901568939202e-05},
       'nursery': {'origin': 'learned', 'weight': 1.3604190036451818e-06},
       'higher': {'origin': 'learned', 'weight': 3.4544721166046257e-07},
       'internet': {'origin': 'learned', 'weight': 1.985563914894138e-06},
       'romantic': {'origin': 'learned', 'weight': 2.9757663553056567e-05},
       'famrel': {'origin': 'learned', 'weight': 0.23128615865426996},
       'freetime': {'origin': 'learned', 'weight': 0.023554521782170514},
       'goout': {'origin': 'learned', 'weight': -0.089444259197238},
       'Dalc': {'origin': 'learned', 'weight': 0.272822548840043},
       'Walc': {'origin': 'learned', 'weight': 0.21200668687560334},
       'health': {'origin': 'learned', 'weight': 0.07702410821801904},
       'absences': {'origin': 'learned', 'weight': -0.1488343695903593},
       'G1': {'origin': 'learned', 'weight': 0.5361350969644317},
       'G2': {'origin': 'learned', 'weight': 0.032840481295506055},
       'G3': {'origin': 'learned', 'weight': 0.03510912683115285}})]




```python
# TODO: what does negative weight mean?
# TODO: why are weights not probabilities?
list(structureModelPruned.adjacency())
```




    [('address',
      {'absences': {'origin': 'learned', 'weight': 1.0400949529066366},
       'G1': {'origin': 'learned', 'weight': 1.006295091882122}}),
     ('famsize', {}),
     ('Pstatus',
      {'famrel': {'origin': 'learned', 'weight': 0.8402877660070628},
       'absences': {'origin': 'learned', 'weight': -1.0538754156321408},
       'G1': {'origin': 'learned', 'weight': 1.261362346111696}}),
     ('Medu', {}),
     ('Fedu', {}),
     ('traveltime', {}),
     ('studytime', {'G1': {'origin': 'learned', 'weight': 0.8636139137063454}}),
     ('failures',
      {'absences': {'origin': 'learned', 'weight': 0.9395791571697139}}),
     ('schoolsup', {'G1': {'origin': 'learned', 'weight': -0.8015184747758134}}),
     ('famsup', {}),
     ('paid', {'absences': {'origin': 'learned', 'weight': -1.0534625350951718}}),
     ('activities', {}),
     ('nursery', {}),
     ('higher',
      {'Medu': {'origin': 'learned', 'weight': 0.9842407795725915},
       'G1': {'origin': 'learned', 'weight': 2.6906165356962597}}),
     ('internet',
      {'absences': {'origin': 'learned', 'weight': 0.8369080746968736}}),
     ('romantic', {}),
     ('famrel', {}),
     ('freetime', {}),
     ('goout', {}),
     ('Dalc', {'Walc': {'origin': 'learned', 'weight': 0.8623769618608512}}),
     ('Walc', {}),
     ('health', {}),
     ('absences', {}),
     ('G1', {'G2': {'origin': 'learned', 'weight': 0.8893123602483163}}),
     ('G2', {'G3': {'origin': 'learned', 'weight': 0.884705682463779}}),
     ('G3', {})]




```python
structureModelLearned.get_edge_data(u = 'address', v = 'G1') # something!
```




    {'origin': 'learned', 'weight': 1.006295091882122}




```python
structureModelPruned.get_edge_data(u = 'address', v = 'G1') # something!
```




    {'origin': 'learned', 'weight': 1.006295091882122}




```python
structureModelLearned.get_edge_data(u = 'Feduromantic', v = 'absences') # nothing!
```


```python
structureModelPruned.get_edge_data(u = 'Feduromantic', v = 'absences') # nothing!
```


```python
list(structureModelLearned.get_target_subgraph(node = 'absences').adjacency())[:2]
```




    [('address',
      {'famsize': {'origin': 'learned', 'weight': 0.07172400411745194},
       'Pstatus': {'origin': 'learned', 'weight': 0.027500652131841753},
       'Medu': {'origin': 'learned', 'weight': 0.4329609981782503},
       'Fedu': {'origin': 'learned', 'weight': 0.10940724573937048},
       'traveltime': {'origin': 'learned', 'weight': -0.3080468648891065},
       'studytime': {'origin': 'learned', 'weight': 0.22858517407180592},
       'failures': {'origin': 'learned', 'weight': 0.06633709792506814},
       'schoolsup': {'origin': 'learned', 'weight': 2.265558640319601e-06},
       'famsup': {'origin': 'learned', 'weight': 4.164128335492464e-06},
       'paid': {'origin': 'learned', 'weight': 2.6188325902813357e-06},
       'activities': {'origin': 'learned', 'weight': 8.921883360997223e-06},
       'nursery': {'origin': 'learned', 'weight': 1.0431757754516237e-06},
       'higher': {'origin': 'learned', 'weight': 0.2175470691398659},
       'internet': {'origin': 'learned', 'weight': 4.631899217412905e-07},
       'romantic': {'origin': 'learned', 'weight': 2.1163994047249527e-05},
       'famrel': {'origin': 'learned', 'weight': 0.2713375883408355},
       'freetime': {'origin': 'learned', 'weight': 0.11768720419459214},
       'goout': {'origin': 'learned', 'weight': 0.16392393831724242},
       'Dalc': {'origin': 'learned', 'weight': 0.11663243893798651},
       'Walc': {'origin': 'learned', 'weight': 0.16559963300289912},
       'health': {'origin': 'learned', 'weight': 0.20294893185551394},
       'absences': {'origin': 'learned', 'weight': 1.0400949529066366},
       'G1': {'origin': 'learned', 'weight': 1.006295091882122},
       'G2': {'origin': 'learned', 'weight': 0.15007496882413057},
       'G3': {'origin': 'learned', 'weight': 0.223096391377955}}),
     ('famsize',
      {'address': {'origin': 'learned', 'weight': 2.57364988344861e-06},
       'Pstatus': {'origin': 'learned', 'weight': -5.39386360384519e-07},
       'Medu': {'origin': 'learned', 'weight': -0.0016220902698672792},
       'Fedu': {'origin': 'learned', 'weight': -0.024651044459558742},
       'traveltime': {'origin': 'learned', 'weight': 0.25181986913147913},
       'studytime': {'origin': 'learned', 'weight': 0.07404468489673609},
       'failures': {'origin': 'learned', 'weight': -0.00011631802985936184},
       'schoolsup': {'origin': 'learned', 'weight': 7.582265421368856e-07},
       'famsup': {'origin': 'learned', 'weight': 8.083571741711851e-06},
       'paid': {'origin': 'learned', 'weight': 5.982031984826393e-07},
       'activities': {'origin': 'learned', 'weight': 1.1369901568939202e-05},
       'nursery': {'origin': 'learned', 'weight': 1.3604190036451818e-06},
       'higher': {'origin': 'learned', 'weight': 3.4544721166046257e-07},
       'internet': {'origin': 'learned', 'weight': 1.985563914894138e-06},
       'romantic': {'origin': 'learned', 'weight': 2.9757663553056567e-05},
       'famrel': {'origin': 'learned', 'weight': 0.23128615865426996},
       'freetime': {'origin': 'learned', 'weight': 0.023554521782170514},
       'goout': {'origin': 'learned', 'weight': -0.089444259197238},
       'Dalc': {'origin': 'learned', 'weight': 0.272822548840043},
       'Walc': {'origin': 'learned', 'weight': 0.21200668687560334},
       'health': {'origin': 'learned', 'weight': 0.07702410821801904},
       'absences': {'origin': 'learned', 'weight': -0.1488343695903593},
       'G1': {'origin': 'learned', 'weight': 0.5361350969644317},
       'G2': {'origin': 'learned', 'weight': 0.032840481295506055},
       'G3': {'origin': 'learned', 'weight': 0.03510912683115285}})]




```python
list(structureModelPruned.get_target_subgraph(node = 'absences').adjacency())



```




    [('address',
      {'absences': {'origin': 'learned', 'weight': 1.0400949529066366},
       'G1': {'origin': 'learned', 'weight': 1.006295091882122}}),
     ('Pstatus',
      {'famrel': {'origin': 'learned', 'weight': 0.8402877660070628},
       'absences': {'origin': 'learned', 'weight': -1.0538754156321408},
       'G1': {'origin': 'learned', 'weight': 1.261362346111696}}),
     ('Medu', {}),
     ('studytime', {'G1': {'origin': 'learned', 'weight': 0.8636139137063454}}),
     ('failures',
      {'absences': {'origin': 'learned', 'weight': 0.9395791571697139}}),
     ('schoolsup', {'G1': {'origin': 'learned', 'weight': -0.8015184747758134}}),
     ('paid', {'absences': {'origin': 'learned', 'weight': -1.0534625350951718}}),
     ('higher',
      {'Medu': {'origin': 'learned', 'weight': 0.9842407795725915},
       'G1': {'origin': 'learned', 'weight': 2.6906165356962597}}),
     ('internet',
      {'absences': {'origin': 'learned', 'weight': 0.8369080746968736}}),
     ('famrel', {}),
     ('absences', {}),
     ('G1', {'G2': {'origin': 'learned', 'weight': 0.8893123602483163}}),
     ('G2', {'G3': {'origin': 'learned', 'weight': 0.884705682463779}}),
     ('G3', {})]



In the above structure some relations appear intuitively correct:
* `Pstatus` affects `famrel` - if parents live apart, the quality of family relationship may be poor as a result
* `internet` affects `absences` - the presence of internet at home may cause stduents to skip class.
* `studytime` affects `G1` - longer studytime should have a positive effect on a student's grade in semester 1 (`G1`).

However there are some relations that are certainly incorrect:
* `higher` affects `Medu` (Mother's education) - this relationship does not make sense as students who want to pursue higher education does not affect mother's education. It could be the OTHER WAY AROUND.

To avoid these erroneous relationships we can re-run the structure learning with some added constraints. Using the method `from_pandas` from `causalnex.structure.notears` to set the argument `tabu_edges`, with the edge (from --> to) which we do not want to include in the graph.


```python

# Reruns the analysis from the structure data, just not including this edge.
# NOT modifying the previous `structureModel`.
structureModel: StructureModel = from_pandas(structData, tabu_edges=[("higher", "Medu")], w_threshold=0.8)
```

Now the `higher --> Medu` relationship is **no longer** in the graph.


```python
# Now visualize it:
viz = plot_structure(
    structureModel,
    graph_attributes={"scale": "0.5"},
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK)
filename_noHigherMedu = curPath + "structure_model_learnedStructure_noHigherMedu.png"
viz.draw(filename_noHigherMedu)
Image(filename_noHigherMedu)
```




![png](FirstCausalNexTutorial_files/FirstCausalNexTutorial_87_0.png)



## Modifying the Structure (after structure learning)
To correct erroneous relationships, we can incorporate domain knowledge into the model after structure learning. We can modify the structure model through adding and deleting the edges. For example we can add and remove edges with the function `add_edge(u_of_edges, v_of_edges)` that adds a causal relationship from `u` to `v`, where
* `u_of_edge` = causal node
* `v_of_edge` = effect node

and if the relation doesn't exist it will be created.


```python
# NOTE the learning of the graph is different each time so these assertions may not be true all the time!
assert not structureModel.has_edge(u = 'higher', v = 'Medu')

# Adding causal relationship from health to paid (used to failures -> G1 ??)
structModeTestEdges = structureModel.copy()

# No edge, showing creation effect
assert not structModeTestEdges.has_edge(u ='health', v ='paid')
structModeTestEdges.add_edge(u_of_edge ='health', v_of_edge ='paid')
assert structModeTestEdges.has_edge(u ='health', v ='paid')
assert {'origin': 'unknown'} == structModeTestEdges.get_edge_data(u ='health', v ='paid')
```


```python
# Has edge, showing replacement effect
assert structModeTestEdges.has_edge(u ='higher', v ='G1')
prevEdge = structModeTestEdges.get_edge_data(u ='higher', v ='G1')
prevEdge
```




    {'origin': 'learned', 'weight': 2.7243556829495947}




```python
structModeTestEdges.add_edge(u_of_edge ='higher', v_of_edge ='G1')
assert structModeTestEdges.has_edge(u ='higher', v ='G1')
curEdge = structModeTestEdges.get_edge_data(u ='higher', v ='G1')
curEdge
assert prevEdge == curEdge
```


```python
# Has edge, showing removal effect
assert structModeTestEdges.has_edge(u ='higher', v ='famrel')
structModeTestEdges.get_edge_data(u ='higher', v ='famrel')
```




    {'origin': 'learned', 'weight': 0.8896329694730597}




```python
structModeTestEdges.remove_edge(u ='higher', v ='famrel')
assert not structModeTestEdges.has_edge(u ='higher', v ='famrel')
```

Can now visualize the updated structure:


```python
viz = plot_structure(
    structModeTestEdges,
    graph_attributes={"scale": "0.5"},
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK)
filename_testEdges = curPath + "structureModel_testedges.png"
viz.draw(filename_testEdges)
Image(filename_testEdges)
```




![png](FirstCausalNexTutorial_files/FirstCausalNexTutorial_95_0.png)




```python
# Previous one:
Image(curPath + "structure_model_learnedStructure_noHigherMedu.png")
```




![png](FirstCausalNexTutorial_files/FirstCausalNexTutorial_96_0.png)




```python
# Just doing same operations on the current graph, after tutorial:
structureModel.add_edge(u_of_edge = 'failures', v_of_edge = 'G1')
# structureModel.remove_edge(u = 'Pstatus', v = 'G1')
# structureModel.remove_edge(u = 'address', v='G1')

viz = plot_structure(
    structureModel,
    graph_attributes={"scale": "0.5"},
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK)
filename_updateEdge = curPath + "structureModel_updated.png"
viz.draw(filename_updateEdge)
Image(filename_updateEdge)
```




![png](FirstCausalNexTutorial_files/FirstCausalNexTutorial_97_0.png)



Can see there are two separate subgraphs in the above plot: `Dalc -> Walc` and the other big subgraph. We can retrieve the largest subgraph easily by calling `get_largest_subgraph()`:


```python
newStructModel: StructureModel = structureModel.get_largest_subgraph()
```


```python
# Now visualize:
viz = plot_structure(
    newStructModel,
    graph_attributes={"scale": "0.5"},
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK)
filename_finalStruct = curPath + "finalStruct.png"
viz.draw(filename_finalStruct)
Image(filename_finalStruct)
```

    /development/bin/python/conda3_ana/envs/pybayesian_env/lib/python3.7/site-packages/pygraphviz/agraph.py:1367: RuntimeWarning: Warning: node 'address', graph '%3' size too small for label
    Warning: node 'absences', graph '%3' size too small for label
    Warning: node 'G1', graph '%3' size too small for label
    Warning: node 'Pstatus', graph '%3' size too small for label
    Warning: node 'famrel', graph '%3' size too small for label
    Warning: node 'studytime', graph '%3' size too small for label
    Warning: node 'failures', graph '%3' size too small for label
    Warning: node 'schoolsup', graph '%3' size too small for label
    Warning: node 'paid', graph '%3' size too small for label
    Warning: node 'higher', graph '%3' size too small for label
    Warning: node 'internet', graph '%3' size too small for label
    Warning: node 'G2', graph '%3' size too small for label
    Warning: node 'G3', graph '%3' size too small for label
    
      warnings.warn(b"".join(errors).decode(self.encoding), RuntimeWarning)
    /development/bin/python/conda3_ana/envs/pybayesian_env/lib/python3.7/site-packages/pygraphviz/agraph.py:1367: RuntimeWarning: Warning: node 'address', graph '%3' size too small for label
    Warning: node 'absences', graph '%3' size too small for label
    Warning: node 'G1', graph '%3' size too small for label
    Warning: node 'G2', graph '%3' size too small for label
    Warning: node 'G3', graph '%3' size too small for label
    Warning: node 'Pstatus', graph '%3' size too small for label
    Warning: node 'famrel', graph '%3' size too small for label
    Warning: node 'studytime', graph '%3' size too small for label
    Warning: node 'failures', graph '%3' size too small for label
    Warning: node 'schoolsup', graph '%3' size too small for label
    Warning: node 'paid', graph '%3' size too small for label
    Warning: node 'higher', graph '%3' size too small for label
    Warning: node 'internet', graph '%3' size too small for label
    
      warnings.warn(b"".join(errors).decode(self.encoding), RuntimeWarning)





![png](FirstCausalNexTutorial_files/FirstCausalNexTutorial_100_1.png)




```python
# Showing that within the same subgraph, we can query by two different nodes and get the same subgraph:
assert newStructModel.get_target_subgraph(node = 'G1').adj == newStructModel.get_target_subgraph(node = 'absences').adj

# NOTE key way how to find all unique subgraphs: going by nodes, for each node, if the current subgraph adjacency equals any other adjacency in the list, scrap that subgraph.
```


```python

```

After deciding on how the final structure model should look, we can instantiate a `BayesianNetwork`:


```python
from causalnex.network import BayesianNetwork

bayesNet: BayesianNetwork = BayesianNetwork(structure = newStructModel)
bayesNet.cpds
```




    {}




```python
bayesNet.edges
#bayesNet.node_states
```




    [('address', 'absences'),
     ('address', 'G1'),
     ('G1', 'G2'),
     ('Pstatus', 'famrel'),
     ('Pstatus', 'absences'),
     ('Pstatus', 'G1'),
     ('studytime', 'G1'),
     ('failures', 'absences'),
     ('failures', 'G1'),
     ('schoolsup', 'G1'),
     ('paid', 'absences'),
     ('higher', 'famrel'),
     ('higher', 'G1'),
     ('internet', 'absences'),
     ('G2', 'G3')]




```python
assert set(bayesNet.nodes) == set(list(iter(newStructModel.node)))
bayesNet.nodes
```




    ['address',
     'absences',
     'G1',
     'Pstatus',
     'famrel',
     'studytime',
     'failures',
     'schoolsup',
     'paid',
     'higher',
     'internet',
     'G2',
     'G3']



Can now learn the conditional probability distribution of different features in this `BayesianNetwork`

# 2/ Fitting the Conditional Distribution of the Bayesian Network
## Preparing the Discretised Data
Any continuous features should be discretised prior to fitting the Bayesian Network, since CausalNex networks support only discrete distributions.

Should make numerical features categorical by discretisation then give the buckets meaningful labels.
## 1. Reducing Cardinality of Categorical Features
To reduce cardinality of categorical features (reduce number of values they take on), can define a map `{oldValue: newValue}` and use this to update the feature we will discretise. Example: for the `studytime` feature, if the studytime is more than $2$ then categorize it as `long-studytime` and the rest of the values are binned under `short_studytime`.


```python
discrData: DataFrame = data.copy()

# Getting unique values per variable
dataVals = {var: data[var].unique() for var in data.columns}
dataVals
```




    {'address': array(['U', 'R'], dtype=object),
     'famsize': array(['GT3', 'LE3'], dtype=object),
     'Pstatus': array(['A', 'T'], dtype=object),
     'Medu': array([4, 1, 3, 2, 0]),
     'Fedu': array([4, 1, 2, 3, 0]),
     'traveltime': array([2, 1, 3, 4]),
     'studytime': array([2, 3, 1, 4]),
     'failures': array([0, 3, 1, 2]),
     'schoolsup': array(['yes', 'no'], dtype=object),
     'famsup': array(['no', 'yes'], dtype=object),
     'paid': array(['no', 'yes'], dtype=object),
     'activities': array(['no', 'yes'], dtype=object),
     'nursery': array(['yes', 'no'], dtype=object),
     'higher': array(['yes', 'no'], dtype=object),
     'internet': array(['no', 'yes'], dtype=object),
     'romantic': array(['no', 'yes'], dtype=object),
     'famrel': array([4, 5, 3, 1, 2]),
     'freetime': array([3, 2, 4, 1, 5]),
     'goout': array([4, 3, 2, 1, 5]),
     'Dalc': array([1, 2, 5, 3, 4]),
     'Walc': array([1, 3, 2, 4, 5]),
     'health': array([3, 5, 1, 2, 4]),
     'absences': array([ 4,  2,  6,  0, 10,  8, 16, 14,  1, 12, 24, 22, 32, 30, 21, 15,  9,
            18, 26,  7, 11,  5, 13,  3]),
     'G1': array([ 0,  9, 12, 14, 11, 13, 10, 15, 17,  8, 16, 18,  7,  6,  5,  4, 19]),
     'G2': array([11, 13, 14, 12, 16, 17,  8, 10, 15,  9,  7,  6, 18, 19,  0,  5]),
     'G3': array([11, 12, 14, 13, 17, 15,  7, 10, 16,  9,  8, 18,  6,  0,  1,  5, 19])}




```python
failuresMap = {v: 'no_failure' if v == [0] else 'yes_failure'
               for v in dataVals['failures']} # 0, 1, 2, 3 (number of failures)
failuresMap
```




    {0: 'no_failure', 3: 'yes_failure', 1: 'yes_failure', 2: 'yes_failure'}




```python
studytimeMap = {v: 'short_studytime' if v in [1,2] else 'long_studytime'
                for v in dataVals['studytime']}
studytimeMap
```




    {2: 'short_studytime',
     3: 'long_studytime',
     1: 'short_studytime',
     4: 'long_studytime'}



Once we have defined the maps `{oldValue: newValue}` we can update each feature, applying the map transformation. The `map` function applies the given dictionary as a rule to the called dictionary.


```python
discrData['failures'] = discrData['failures'].map(failuresMap)
discrData['failures']
```




    0       no_failure
    1       no_failure
    2       no_failure
    3       no_failure
    4       no_failure
              ...     
    644    yes_failure
    645     no_failure
    646     no_failure
    647     no_failure
    648     no_failure
    Name: failures, Length: 649, dtype: object




```python
discrData['studytime'] = discrData['studytime'].map(studytimeMap)
discrData['studytime']
```




    0      short_studytime
    1      short_studytime
    2      short_studytime
    3       long_studytime
    4      short_studytime
                ...       
    644     long_studytime
    645    short_studytime
    646    short_studytime
    647    short_studytime
    648    short_studytime
    Name: studytime, Length: 649, dtype: object



## 3. Discretising Numeric Features
To make numeric features categorical, they must first by discretised. The `causalnex.discretiser.Discretiser` helper class supports several discretisation methods.
Here, the `fixed` method will be applied, providing static values that define the bucket boundaries. For instance, `absences` will be discretised into buckets `< 1`, `1 to 9`, and `>= 10`. Each bucket will be labelled as an integer, starting from zero.


```python
from causalnex.discretiser import Discretiser

# Many values in absences, G1, G2, G3
dataVals
```




    {'address': array(['U', 'R'], dtype=object),
     'famsize': array(['GT3', 'LE3'], dtype=object),
     'Pstatus': array(['A', 'T'], dtype=object),
     'Medu': array([4, 1, 3, 2, 0]),
     'Fedu': array([4, 1, 2, 3, 0]),
     'traveltime': array([2, 1, 3, 4]),
     'studytime': array([2, 3, 1, 4]),
     'failures': array([0, 3, 1, 2]),
     'schoolsup': array(['yes', 'no'], dtype=object),
     'famsup': array(['no', 'yes'], dtype=object),
     'paid': array(['no', 'yes'], dtype=object),
     'activities': array(['no', 'yes'], dtype=object),
     'nursery': array(['yes', 'no'], dtype=object),
     'higher': array(['yes', 'no'], dtype=object),
     'internet': array(['no', 'yes'], dtype=object),
     'romantic': array(['no', 'yes'], dtype=object),
     'famrel': array([4, 5, 3, 1, 2]),
     'freetime': array([3, 2, 4, 1, 5]),
     'goout': array([4, 3, 2, 1, 5]),
     'Dalc': array([1, 2, 5, 3, 4]),
     'Walc': array([1, 3, 2, 4, 5]),
     'health': array([3, 5, 1, 2, 4]),
     'absences': array([ 4,  2,  6,  0, 10,  8, 16, 14,  1, 12, 24, 22, 32, 30, 21, 15,  9,
            18, 26,  7, 11,  5, 13,  3]),
     'G1': array([ 0,  9, 12, 14, 11, 13, 10, 15, 17,  8, 16, 18,  7,  6,  5,  4, 19]),
     'G2': array([11, 13, 14, 12, 16, 17,  8, 10, 15,  9,  7,  6, 18, 19,  0,  5]),
     'G3': array([11, 12, 14, 13, 17, 15,  7, 10, 16,  9,  8, 18,  6,  0,  1,  5, 19])}




```python
discrData['absences'] = Discretiser(method = 'fixed', numeric_split_points = [1,10]).transform(data = data['absences'].values)

assert (np.unique(discrData['absences']) == np.array([0,1,2])).all()


discrData['G1'] = Discretiser(method = 'fixed', numeric_split_points = [10]).transform(data = data['G1'].values)
assert (np.unique(discrData['G1']) == np.array([0,1])).all()


discrData['G2'] = Discretiser(method = 'fixed', numeric_split_points = [10]).transform(data = data['G2'].values)
assert (np.unique(discrData['G2']) == np.array([0,1])).all()

discrData['G3'] = Discretiser(method = 'fixed', numeric_split_points = [10]).transform(data = data['G3'].values)
assert (np.unique(discrData['G3']) == np.array([0,1])).all()
```

## 4. Create Labels for Numeric Features
To make the discretised categories more readable, we can map the category labels onto something more meaningful in the same way we mapped category feature values.


```python

absencesMap = {0: "No-absence", 1:"Low-absence", 2:"High-absence"}

G1Map = {0: "Fail", 1: "Pass"}
G2Map = {0: "Fail", 1: "Pass"}
G3Map = {0: "Fail", 1: "Pass"}

discrData['absences'] = discrData['absences'].map(absencesMap)
discrData['absences']
```




    0      Low-absence
    1      Low-absence
    2      Low-absence
    3       No-absence
    4       No-absence
              ...     
    644    Low-absence
    645    Low-absence
    646    Low-absence
    647    Low-absence
    648    Low-absence
    Name: absences, Length: 649, dtype: object




```python
discrData['G1'] = discrData['G1'].map(G1Map)
discrData['G1']
```




    0      Fail
    1      Fail
    2      Pass
    3      Pass
    4      Pass
           ... 
    644    Pass
    645    Pass
    646    Pass
    647    Pass
    648    Pass
    Name: G1, Length: 649, dtype: object




```python
discrData['G2'] = discrData['G2'].map(G2Map)
discrData['G2']
```




    0      Pass
    1      Pass
    2      Pass
    3      Pass
    4      Pass
           ... 
    644    Pass
    645    Pass
    646    Pass
    647    Pass
    648    Pass
    Name: G2, Length: 649, dtype: object




```python
discrData['G3'] = discrData['G3'].map(G3Map)
discrData['G3']



```




    0      Pass
    1      Pass
    2      Pass
    3      Pass
    4      Pass
           ... 
    644    Pass
    645    Pass
    646    Fail
    647    Pass
    648    Pass
    Name: G3, Length: 649, dtype: object




```python
# Now for reference later get the discrete data values also:
discrDataVals = {var: discrData[var].unique() for var in discrData.columns}
discrDataVals
```




    {'address': array(['U', 'R'], dtype=object),
     'famsize': array(['GT3', 'LE3'], dtype=object),
     'Pstatus': array(['A', 'T'], dtype=object),
     'Medu': array([4, 1, 3, 2, 0]),
     'Fedu': array([4, 1, 2, 3, 0]),
     'traveltime': array([2, 1, 3, 4]),
     'studytime': array(['short_studytime', 'long_studytime'], dtype=object),
     'failures': array(['no_failure', 'yes_failure'], dtype=object),
     'schoolsup': array(['yes', 'no'], dtype=object),
     'famsup': array(['no', 'yes'], dtype=object),
     'paid': array(['no', 'yes'], dtype=object),
     'activities': array(['no', 'yes'], dtype=object),
     'nursery': array(['yes', 'no'], dtype=object),
     'higher': array(['yes', 'no'], dtype=object),
     'internet': array(['no', 'yes'], dtype=object),
     'romantic': array(['no', 'yes'], dtype=object),
     'famrel': array([4, 5, 3, 1, 2]),
     'freetime': array([3, 2, 4, 1, 5]),
     'goout': array([4, 3, 2, 1, 5]),
     'Dalc': array([1, 2, 5, 3, 4]),
     'Walc': array([1, 3, 2, 4, 5]),
     'health': array([3, 5, 1, 2, 4]),
     'absences': array(['Low-absence', 'No-absence', 'High-absence'], dtype=object),
     'G1': array(['Fail', 'Pass'], dtype=object),
     'G2': array(['Pass', 'Fail'], dtype=object),
     'G3': array(['Pass', 'Fail'], dtype=object)}



## 5. Train / Test Split
Must train and test split data to help validate findings.
Split 90% train and 10% test.


```python
from sklearn.model_selection import train_test_split

train, test = train_test_split(discrData,
                               train_size = 0.9, test_size = 0.10,
                               random_state = 7)
```

# 3/ Model Probability
With the learnt structure model and discretised data, we can now fit the probability distribution of the Bayesian Network.

**First Step:** The first step is to specify all the states that each node can take. Can be done from data or can provide dictionary of node values. Here, we use the full dataset to avoid cases where states in our test set do not exist in the training set. In the real world, those states would need to be provided using the dictionary method.


```python
import copy


# First 'copying' the object so previous state is preserved:
# SOURCE: https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/
bayesNetNodeStates = copy.deepcopy(bayesNet)
assert not bayesNetNodeStates == bayesNet, "Deepcopy bayesnet object must work"
# bayesNetNodeStates = BayesianNetwork(bayesNet.structure)

bayesNetNodeStates: BayesianNetwork = bayesNetNodeStates.fit_node_states(df = discrData)
bayesNetNodeStates.node_states
```




    {'address': {'R', 'U'},
     'famsize': {'GT3', 'LE3'},
     'Pstatus': {'A', 'T'},
     'Medu': {0, 1, 2, 3, 4},
     'Fedu': {0, 1, 2, 3, 4},
     'traveltime': {1, 2, 3, 4},
     'studytime': {'long_studytime', 'short_studytime'},
     'failures': {'no_failure', 'yes_failure'},
     'schoolsup': {'no', 'yes'},
     'famsup': {'no', 'yes'},
     'paid': {'no', 'yes'},
     'activities': {'no', 'yes'},
     'nursery': {'no', 'yes'},
     'higher': {'no', 'yes'},
     'internet': {'no', 'yes'},
     'romantic': {'no', 'yes'},
     'famrel': {1, 2, 3, 4, 5},
     'freetime': {1, 2, 3, 4, 5},
     'goout': {1, 2, 3, 4, 5},
     'Dalc': {1, 2, 3, 4, 5},
     'Walc': {1, 2, 3, 4, 5},
     'health': {1, 2, 3, 4, 5},
     'absences': {'High-absence', 'Low-absence', 'No-absence'},
     'G1': {'Fail', 'Pass'},
     'G2': {'Fail', 'Pass'},
     'G3': {'Fail', 'Pass'}}



## Fit Conditional Probability Distributions
The `fit_cpds` method of `BayesianNetwork` accepts a dataset to learn the conditional probability distributions (CPDs) of **each node** along with a method of how to do this fit.


```python
# Copying the object information
bayesNetCPD: BayesianNetwork = copy.deepcopy(bayesNetNodeStates)

# Fitting the CPDs
bayesNetCPD: BayesianNetwork = bayesNetCPD.fit_cpds(data = train,
                                                    method = "BayesianEstimator",
                                                    bayes_prior = "K2")
```

    /development/bin/python/conda3_ana/envs/pybayesian_env/lib/python3.7/site-packages/pandas/core/generic.py:5191: FutureWarning: Attribute 'is_copy' is deprecated and will be removed in a future version.
      object.__getattribute__(self, name)
    /development/bin/python/conda3_ana/envs/pybayesian_env/lib/python3.7/site-packages/pandas/core/generic.py:5192: FutureWarning: Attribute 'is_copy' is deprecated and will be removed in a future version.
      return object.__setattr__(self, name, value)
    /development/bin/python/conda3_ana/envs/pybayesian_env/lib/python3.7/site-packages/pgmpy/estimators/base.py:54: FutureWarning: 
    .ix is deprecated. Please use
    .loc for label based indexing or
    .iloc for positional indexing
    
    See the documentation here:
    http://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#ix-indexer-is-deprecated
      states = sorted(list(self.data.ix[:, variable].dropna().unique()))
    /development/bin/python/conda3_ana/envs/pybayesian_env/lib/python3.7/site-packages/pgmpy/estimators/base.py:111: FutureWarning: 
    .ix is deprecated. Please use
    .loc for label based indexing or
    .iloc for positional indexing
    
    See the documentation here:
    http://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#ix-indexer-is-deprecated
      state_count_data = data.ix[:, variable].value_counts()



```python
bayesNetCPD.cpds
```




    {'address':                  
     address          
     R        0.302048
     U        0.697952,
     'absences': Pstatus               A                                                       \
     address               R                                                        
     failures     no_failure                      yes_failure                       
     internet             no        yes                    no                 yes   
     paid                 no   yes   no       yes          no       yes        no   
     absences                                                                       
     High-absence        0.2  0.25  0.2  0.333333         0.2  0.333333  0.333333   
     Low-absence         0.4  0.50  0.4  0.333333         0.4  0.333333  0.333333   
     No-absence          0.4  0.25  0.4  0.333333         0.4  0.333333  0.333333   
     
     Pstatus                                      ...           T                  \
     address                         U            ...           R               U   
     failures               no_failure            ... yes_failure      no_failure   
     internet                       no            ...         yes              no   
     paid               yes         no       yes  ...          no  yes         no   
     absences                                     ...                               
     High-absence  0.333333   0.200000  0.333333  ...    0.148148  0.2   0.061224   
     Low-absence   0.333333   0.666667  0.333333  ...    0.518519  0.6   0.612245   
     No-absence    0.333333   0.133333  0.333333  ...    0.333333  0.2   0.326531   
     
     Pstatus                                                                       
     address                                                                       
     failures                               yes_failure                            
     internet                 yes                    no             yes            
     paid           yes        no       yes          no   yes        no       yes  
     absences                                                                      
     High-absence  0.25  0.109312  0.071429    0.142857  0.25  0.323529  0.222222  
     Low-absence   0.25  0.473684  0.714286    0.428571  0.25  0.470588  0.555556  
     No-absence    0.50  0.417004  0.214286    0.428571  0.50  0.205882  0.222222  
     
     [3 rows x 32 columns],
     'G1': Pstatus                A                                                 \
     address                R                                                  
     failures      no_failure                                                  
     higher                no                                                  
     schoolsup             no                            yes                   
     studytime long_studytime short_studytime long_studytime short_studytime   
     G1                                                                        
     Fail            0.666667        0.333333            0.5             0.5   
     Pass            0.333333        0.666667            0.5             0.5   
     
     Pstatus                                                                  \
     address                                                                   
     failures                                                                  
     higher               yes                                                  
     schoolsup             no                            yes                   
     studytime long_studytime short_studytime long_studytime short_studytime   
     G1                                                                        
     Fail            0.333333        0.222222            0.5             0.5   
     Pass            0.666667        0.777778            0.5             0.5   
     
     Pstatus                                   ...              T                  \
     address                                   ...              U                   
     failures     yes_failure                  ...     no_failure                   
     higher                no                  ...            yes                   
     schoolsup             no                  ...            yes                   
     studytime long_studytime short_studytime  ... long_studytime short_studytime   
     G1                                        ...                                  
     Fail            0.666667        0.666667  ...       0.222222        0.285714   
     Pass            0.333333        0.333333  ...       0.777778        0.714286   
     
     Pstatus                                                                  \
     address                                                                   
     failures     yes_failure                                                  
     higher                no                                                  
     schoolsup             no                            yes                   
     studytime long_studytime short_studytime long_studytime short_studytime   
     G1                                                                        
     Fail            0.666667        0.789474            0.5        0.666667   
     Pass            0.333333        0.210526            0.5        0.333333   
     
     Pstatus                                                                  
     address                                                                  
     failures                                                                 
     higher               yes                                                 
     schoolsup             no                            yes                  
     studytime long_studytime short_studytime long_studytime short_studytime  
     G1                                                                       
     Fail            0.571429        0.652174            0.5        0.666667  
     Pass            0.428571        0.347826            0.5        0.333333  
     
     [2 rows x 64 columns],
     'Pstatus':                  
     Pstatus          
     A        0.119454
     T        0.880546,
     'famrel': Pstatus         A                   T          
     higher         no       yes        no       yes
     famrel                                         
     1        0.142857  0.061538  0.064516  0.023758
     2        0.142857  0.092308  0.048387  0.045356
     3        0.285714  0.092308  0.161290  0.159827
     4        0.357143  0.461538  0.419355  0.503240
     5        0.071429  0.292308  0.306452  0.267819,
     'studytime':                          
     studytime                
     long_studytime   0.204778
     short_studytime  0.795222,
     'failures':                      
     failures             
     no_failure   0.837884
     yes_failure  0.162116,
     'schoolsup':                    
     schoolsup          
     no         0.887372
     yes        0.112628,
     'paid':               
     paid          
     no    0.938567
     yes   0.061433,
     'higher':                 
     higher          
     no      0.114334
     yes     0.885666,
     'internet':                   
     internet          
     no        0.230375
     yes       0.769625,
     'G2': G1   Fail Pass
     G2            
     Fail  0.5  0.5
     Pass  0.5  0.5,
     'G3': G2   Fail Pass
     G3            
     Fail  0.5  0.5
     Pass  0.5  0.5}




```python
# The size of the tables depends on how many connections a node has
Image(filename_finalStruct)
```




![png](FirstCausalNexTutorial_files/FirstCausalNexTutorial_130_0.png)




```python
# G1 has many connections so its table holds all the combinations of conditional probabilities.
bayesNetCPD.cpds['G1']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>Pstatus</th>
      <th colspan="10" halign="left">A</th>
      <th>...</th>
      <th colspan="10" halign="left">T</th>
    </tr>
    <tr>
      <th>address</th>
      <th colspan="10" halign="left">R</th>
      <th>...</th>
      <th colspan="10" halign="left">U</th>
    </tr>
    <tr>
      <th>failures</th>
      <th colspan="8" halign="left">no_failure</th>
      <th colspan="2" halign="left">yes_failure</th>
      <th>...</th>
      <th colspan="2" halign="left">no_failure</th>
      <th colspan="8" halign="left">yes_failure</th>
    </tr>
    <tr>
      <th>higher</th>
      <th colspan="4" halign="left">no</th>
      <th colspan="4" halign="left">yes</th>
      <th colspan="2" halign="left">no</th>
      <th>...</th>
      <th colspan="2" halign="left">yes</th>
      <th colspan="4" halign="left">no</th>
      <th colspan="4" halign="left">yes</th>
    </tr>
    <tr>
      <th>schoolsup</th>
      <th colspan="2" halign="left">no</th>
      <th colspan="2" halign="left">yes</th>
      <th colspan="2" halign="left">no</th>
      <th colspan="2" halign="left">yes</th>
      <th colspan="2" halign="left">no</th>
      <th>...</th>
      <th colspan="2" halign="left">yes</th>
      <th colspan="2" halign="left">no</th>
      <th colspan="2" halign="left">yes</th>
      <th colspan="2" halign="left">no</th>
      <th colspan="2" halign="left">yes</th>
    </tr>
    <tr>
      <th>studytime</th>
      <th>long_studytime</th>
      <th>short_studytime</th>
      <th>long_studytime</th>
      <th>short_studytime</th>
      <th>long_studytime</th>
      <th>short_studytime</th>
      <th>long_studytime</th>
      <th>short_studytime</th>
      <th>long_studytime</th>
      <th>short_studytime</th>
      <th>...</th>
      <th>long_studytime</th>
      <th>short_studytime</th>
      <th>long_studytime</th>
      <th>short_studytime</th>
      <th>long_studytime</th>
      <th>short_studytime</th>
      <th>long_studytime</th>
      <th>short_studytime</th>
      <th>long_studytime</th>
      <th>short_studytime</th>
    </tr>
    <tr>
      <th>G1</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Fail</th>
      <td>0.666667</td>
      <td>0.333333</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>0.333333</td>
      <td>0.222222</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>0.666667</td>
      <td>0.666667</td>
      <td>...</td>
      <td>0.222222</td>
      <td>0.285714</td>
      <td>0.666667</td>
      <td>0.789474</td>
      <td>0.5</td>
      <td>0.666667</td>
      <td>0.571429</td>
      <td>0.652174</td>
      <td>0.5</td>
      <td>0.666667</td>
    </tr>
    <tr>
      <th>Pass</th>
      <td>0.333333</td>
      <td>0.666667</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>0.666667</td>
      <td>0.777778</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>0.333333</td>
      <td>0.333333</td>
      <td>...</td>
      <td>0.777778</td>
      <td>0.714286</td>
      <td>0.333333</td>
      <td>0.210526</td>
      <td>0.5</td>
      <td>0.333333</td>
      <td>0.428571</td>
      <td>0.347826</td>
      <td>0.5</td>
      <td>0.333333</td>
    </tr>
  </tbody>
</table>
<p>2 rows × 64 columns</p>
</div>




```python
bayesNetCPD.cpds['absences']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>Pstatus</th>
      <th colspan="10" halign="left">A</th>
      <th>...</th>
      <th colspan="10" halign="left">T</th>
    </tr>
    <tr>
      <th>address</th>
      <th colspan="8" halign="left">R</th>
      <th colspan="2" halign="left">U</th>
      <th>...</th>
      <th colspan="2" halign="left">R</th>
      <th colspan="8" halign="left">U</th>
    </tr>
    <tr>
      <th>failures</th>
      <th colspan="4" halign="left">no_failure</th>
      <th colspan="4" halign="left">yes_failure</th>
      <th colspan="2" halign="left">no_failure</th>
      <th>...</th>
      <th colspan="2" halign="left">yes_failure</th>
      <th colspan="4" halign="left">no_failure</th>
      <th colspan="4" halign="left">yes_failure</th>
    </tr>
    <tr>
      <th>internet</th>
      <th colspan="2" halign="left">no</th>
      <th colspan="2" halign="left">yes</th>
      <th colspan="2" halign="left">no</th>
      <th colspan="2" halign="left">yes</th>
      <th colspan="2" halign="left">no</th>
      <th>...</th>
      <th colspan="2" halign="left">yes</th>
      <th colspan="2" halign="left">no</th>
      <th colspan="2" halign="left">yes</th>
      <th colspan="2" halign="left">no</th>
      <th colspan="2" halign="left">yes</th>
    </tr>
    <tr>
      <th>paid</th>
      <th>no</th>
      <th>yes</th>
      <th>no</th>
      <th>yes</th>
      <th>no</th>
      <th>yes</th>
      <th>no</th>
      <th>yes</th>
      <th>no</th>
      <th>yes</th>
      <th>...</th>
      <th>no</th>
      <th>yes</th>
      <th>no</th>
      <th>yes</th>
      <th>no</th>
      <th>yes</th>
      <th>no</th>
      <th>yes</th>
      <th>no</th>
      <th>yes</th>
    </tr>
    <tr>
      <th>absences</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>High-absence</th>
      <td>0.2</td>
      <td>0.25</td>
      <td>0.2</td>
      <td>0.333333</td>
      <td>0.2</td>
      <td>0.333333</td>
      <td>0.333333</td>
      <td>0.333333</td>
      <td>0.200000</td>
      <td>0.333333</td>
      <td>...</td>
      <td>0.148148</td>
      <td>0.2</td>
      <td>0.061224</td>
      <td>0.25</td>
      <td>0.109312</td>
      <td>0.071429</td>
      <td>0.142857</td>
      <td>0.25</td>
      <td>0.323529</td>
      <td>0.222222</td>
    </tr>
    <tr>
      <th>Low-absence</th>
      <td>0.4</td>
      <td>0.50</td>
      <td>0.4</td>
      <td>0.333333</td>
      <td>0.4</td>
      <td>0.333333</td>
      <td>0.333333</td>
      <td>0.333333</td>
      <td>0.666667</td>
      <td>0.333333</td>
      <td>...</td>
      <td>0.518519</td>
      <td>0.6</td>
      <td>0.612245</td>
      <td>0.25</td>
      <td>0.473684</td>
      <td>0.714286</td>
      <td>0.428571</td>
      <td>0.25</td>
      <td>0.470588</td>
      <td>0.555556</td>
    </tr>
    <tr>
      <th>No-absence</th>
      <td>0.4</td>
      <td>0.25</td>
      <td>0.4</td>
      <td>0.333333</td>
      <td>0.4</td>
      <td>0.333333</td>
      <td>0.333333</td>
      <td>0.333333</td>
      <td>0.133333</td>
      <td>0.333333</td>
      <td>...</td>
      <td>0.333333</td>
      <td>0.2</td>
      <td>0.326531</td>
      <td>0.50</td>
      <td>0.417004</td>
      <td>0.214286</td>
      <td>0.428571</td>
      <td>0.50</td>
      <td>0.205882</td>
      <td>0.222222</td>
    </tr>
  </tbody>
</table>
<p>3 rows × 32 columns</p>
</div>




```python
# Studytime variable is a singular ndoe so its table is small, no conditional probabilities here.
bayesNetCPD.cpds['studytime']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
    </tr>
    <tr>
      <th>studytime</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>long_studytime</th>
      <td>0.204778</td>
    </tr>
    <tr>
      <th>short_studytime</th>
      <td>0.795222</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Pstatus has only outgoing nodes, no incoming nodes so has no conditional probabilities.
bayesNetCPD.cpds['Pstatus']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
    </tr>
    <tr>
      <th>Pstatus</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>A</th>
      <td>0.119454</td>
    </tr>
    <tr>
      <th>T</th>
      <td>0.880546</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Famrel has two incoming nodes (PStatus and higher) so models their conditional probabilities.
bayesNetCPD.cpds['famrel']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>Pstatus</th>
      <th colspan="2" halign="left">A</th>
      <th colspan="2" halign="left">T</th>
    </tr>
    <tr>
      <th>higher</th>
      <th>no</th>
      <th>yes</th>
      <th>no</th>
      <th>yes</th>
    </tr>
    <tr>
      <th>famrel</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>0.142857</td>
      <td>0.061538</td>
      <td>0.064516</td>
      <td>0.023758</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.142857</td>
      <td>0.092308</td>
      <td>0.048387</td>
      <td>0.045356</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.285714</td>
      <td>0.092308</td>
      <td>0.161290</td>
      <td>0.159827</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.357143</td>
      <td>0.461538</td>
      <td>0.419355</td>
      <td>0.503240</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.071429</td>
      <td>0.292308</td>
      <td>0.306452</td>
      <td>0.267819</td>
    </tr>
  </tbody>
</table>
</div>




```python
bayesNetCPD.cpds['G2']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>G1</th>
      <th>Fail</th>
      <th>Pass</th>
    </tr>
    <tr>
      <th>G2</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Fail</th>
      <td>0.5</td>
      <td>0.5</td>
    </tr>
    <tr>
      <th>Pass</th>
      <td>0.5</td>
      <td>0.5</td>
    </tr>
  </tbody>
</table>
</div>




```python
bayesNetCPD.cpds['G3']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>G2</th>
      <th>Fail</th>
      <th>Pass</th>
    </tr>
    <tr>
      <th>G3</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Fail</th>
      <td>0.5</td>
      <td>0.5</td>
    </tr>
    <tr>
      <th>Pass</th>
      <td>0.5</td>
      <td>0.5</td>
    </tr>
  </tbody>
</table>
</div>



The CPD dictionaries are multiindexed so the `loc` functino can be a useful way to interact with them:


```python
# TODO: https://hyp.is/_95epIOuEeq_HdeYjzCPXQ/causalnex.readthedocs.io/en/latest/03_tutorial/03_tutorial.html
discrData.loc[1:5,['address', 'G1', 'paid', 'higher']]


```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>address</th>
      <th>G1</th>
      <th>paid</th>
      <th>higher</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>U</td>
      <td>Fail</td>
      <td>no</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>2</th>
      <td>U</td>
      <td>Pass</td>
      <td>no</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>3</th>
      <td>U</td>
      <td>Pass</td>
      <td>no</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>4</th>
      <td>U</td>
      <td>Pass</td>
      <td>no</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>5</th>
      <td>U</td>
      <td>Pass</td>
      <td>no</td>
      <td>yes</td>
    </tr>
  </tbody>
</table>
</div>



## Predict the State given the Input Data
The `predict` method of `BayesianNetwork` allos us to make predictions based on the data using the learnt network. For example we want to predict if a student passes of failes the exam based on the input data. Consider an incoming student data like this:


```python
# Row number 18
discrData.loc[18, discrData.columns != 'G1']
```




    address                     U
    famsize                   GT3
    Pstatus                     T
    Medu                        3
    Fedu                        2
    traveltime                  1
    studytime     short_studytime
    failures          yes_failure
    schoolsup                  no
    famsup                    yes
    paid                      yes
    activities                yes
    nursery                   yes
    higher                    yes
    internet                  yes
    romantic                   no
    famrel                      5
    freetime                    5
    goout                       5
    Dalc                        2
    Walc                        4
    health                      5
    absences          Low-absence
    G2                       Fail
    G3                       Fail
    Name: 18, dtype: object



Based on this data, want to predict if this particular student (in row 18) will succeed on their exam. Intuitively expect this student not to succeed because they spend shorter amount of study time and have failed in the past.

There are two kinds of prediction methods:
* [`predict_probability(data, node)`](https://causalnex.readthedocs.io/en/latest/source/api_docs/causalnex.network.BayesianNetwork.html#causalnex.network.BayesianNetwork.predict_probability): Predict the **probability of each possible state of a node**, based on some input data.
* [`predict(data, node)`](https://causalnex.readthedocs.io/en/latest/source/api_docs/causalnex.network.BayesianNetwork.html#causalnex.network.BayesianNetwork.predict): Predict the **state of a node ** based on some input data, using the Bayesian Network.


```python
predictionProbs = bayesNetCPD.predict_probability(data = discrData, node = 'G1')
predictionProbs
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>G1_Pass</th>
      <th>G1_Fail</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.777778</td>
      <td>0.222222</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.882051</td>
      <td>0.117949</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.714286</td>
      <td>0.285714</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.968254</td>
      <td>0.031746</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.882051</td>
      <td>0.117949</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>644</th>
      <td>0.600000</td>
      <td>0.400000</td>
    </tr>
    <tr>
      <th>645</th>
      <td>0.882051</td>
      <td>0.117949</td>
    </tr>
    <tr>
      <th>646</th>
      <td>0.882051</td>
      <td>0.117949</td>
    </tr>
    <tr>
      <th>647</th>
      <td>0.882051</td>
      <td>0.117949</td>
    </tr>
    <tr>
      <th>648</th>
      <td>0.750000</td>
      <td>0.250000</td>
    </tr>
  </tbody>
</table>
<p>649 rows × 2 columns</p>
</div>




```python
# Student 18 passes with probability 0.358, and fails with prob 0.64
predictionProbs.loc[18, :]
```




    G1_Pass    0.347826
    G1_Fail    0.652174
    Name: 18, dtype: float64




```python
# This function does predictions for ALL observations (all students)
predictions = bayesNetCPD.predict(data = discrData, node = 'G1')
predictions
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>G1_prediction</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Pass</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Pass</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Pass</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Pass</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Pass</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>644</th>
      <td>Pass</td>
    </tr>
    <tr>
      <th>645</th>
      <td>Pass</td>
    </tr>
    <tr>
      <th>646</th>
      <td>Pass</td>
    </tr>
    <tr>
      <th>647</th>
      <td>Pass</td>
    </tr>
    <tr>
      <th>648</th>
      <td>Pass</td>
    </tr>
  </tbody>
</table>
<p>649 rows × 1 columns</p>
</div>




```python
predictions.loc[18, :]
```




    G1_prediction    Fail
    Name: 18, dtype: object



Compare this prediction to the ground truth:


```python
print(f"Student 18 is predicted to {predictions.loc[18, 'G1_prediction']}")
print(f"Ground truth for student 18 is {discrData.loc[18, 'G1']}")
```

    Student 18 is predicted to Fail
    Ground truth for student 18 is Fail


# 4/ Model Quality
To evaluate the quality of the model that has been learned, CausalNex supports two main approaches: Classification Report and Reciever Operating Characteristics (ROC) / Area Under the ROC Curve (AUC).
## Measure 1: Classification Report
To obtain a classification report using a BN, we need to provide a test set and the node we are trying to classify. The classification report predicts the target node for all rows (observations) in the test set and evaluate how well those predictions are made, via the model.


```python
from causalnex.evaluation import classification_report

classification_report(bn = bayesNetCPD, data = test, node = 'G1')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>precision</th>
      <th>recall</th>
      <th>f1-score</th>
      <th>support</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>G1_Fail</th>
      <td>0.777778</td>
      <td>0.583333</td>
      <td>0.666667</td>
      <td>12</td>
    </tr>
    <tr>
      <th>G1_Pass</th>
      <td>0.910714</td>
      <td>0.962264</td>
      <td>0.935780</td>
      <td>53</td>
    </tr>
    <tr>
      <th>micro avg</th>
      <td>0.892308</td>
      <td>0.892308</td>
      <td>0.892308</td>
      <td>65</td>
    </tr>
    <tr>
      <th>macro avg</th>
      <td>0.844246</td>
      <td>0.772799</td>
      <td>0.801223</td>
      <td>65</td>
    </tr>
    <tr>
      <th>weighted avg</th>
      <td>0.886172</td>
      <td>0.892308</td>
      <td>0.886097</td>
      <td>65</td>
    </tr>
  </tbody>
</table>
</div>



**Interpret Results of classification report:** this report shows that the model can classify reasonably well whether a student passs the exam. For predictions where the student fails, the precision is adequate but recall is bad. This implies that we can rely on predictions for `G1_Fail` but we are likely to miss some of the predictions we should have made. Perhaps these missing predictions are a result of something missing in our structure
* ALERT - explore graph structure when the recall is bad


## ROC / AUC
The ROC and AUC can be obtained with `roc_auc` method within CausalNex metrics module.
ROC curve is computed by micro-averaging predictions made across all states (classes) of the target node.


```python
from causalnex.evaluation import roc_auc

roc, auc = roc_auc(bn = bayesNetCPD, data = test, node = 'G1')

print(f"ROC = \n{roc}\n")
print(f"AUC = {auc}")
```

    ROC = 
    [(0.0, 0.0), (0.0, 0.1076923076923077), (0.0, 0.16923076923076924), (0.046153846153846156, 0.5076923076923077), (0.046153846153846156, 0.5692307692307692), (0.046153846153846156, 0.6), (0.06153846153846154, 0.6153846153846154), (0.09230769230769231, 0.7692307692307693), (0.09230769230769231, 0.8), (0.1076923076923077, 0.8), (0.1076923076923077, 0.8461538461538461), (0.15384615384615385, 0.8923076923076924), (0.2, 0.8923076923076924), (0.2, 0.9076923076923077), (0.23076923076923078, 0.9076923076923077), (0.38461538461538464, 0.9384615384615385), (0.4, 0.9538461538461539), (0.4307692307692308, 0.9538461538461539), (0.49230769230769234, 0.9538461538461539), (0.8307692307692308, 1.0), (0.8923076923076924, 1.0), (1.0, 1.0)]
    
    AUC = 0.9123076923076924


High value of AUC gives confidence in model performance



# 5/ Querying Marginals
After iterating over our model structure, CPDs, and validating our model quality, we can **query our model under different observations** to gain insights.

## Baseline Marginals
To query the model for baseline marginals that reflect the population as a whole, a `query` method can be used.

**First:** update the model using the complete dataset since the one we currently have is built only from training data.


```python
# Copy object:
bayesNetFull = copy.deepcopy(bayesNetCPD)

# Fitting CPDs with full data
bayesNetFull: BayesianNetwork = bayesNetFull.fit_cpds(data = discrData,
                                                     method = "BayesianEstimator",
                                                     bayes_prior = "K2")
```

    WARNING:root:Replacing existing CPD for address
    WARNING:root:Replacing existing CPD for absences
    WARNING:root:Replacing existing CPD for G1
    WARNING:root:Replacing existing CPD for Pstatus
    WARNING:root:Replacing existing CPD for famrel
    WARNING:root:Replacing existing CPD for studytime
    WARNING:root:Replacing existing CPD for failures
    WARNING:root:Replacing existing CPD for schoolsup
    WARNING:root:Replacing existing CPD for paid
    WARNING:root:Replacing existing CPD for higher
    WARNING:root:Replacing existing CPD for internet
    WARNING:root:Replacing existing CPD for G2
    WARNING:root:Replacing existing CPD for G3


Get warnings, showing we are replacing the previously existing CPDs

**Second**: For inference, must create a new `InferenceEngine` from our `BayesianNetwork`, which lets us query the model. The query method will compute the marginal likelihood of all states for all nodes. Query lets us get the marginal distributions, marginalizing to get rid of the conditioning variable(s) for each node variable.


```python
from causalnex.inference import InferenceEngine


eng = InferenceEngine(bn = bayesNetFull)
eng
```




    <causalnex.inference.inference.InferenceEngine at 0x7f6cca0b69d0>



Query the baseline marginal distributions, which means querying marginals **as learned from data**:


```python
marginalDistLearned: Dict[str, Dict[str, float]] = eng.query()
marginalDistLearned
```




    {'address': {'R': 0.3041474654377881, 'U': 0.6958525345622117},
     'absences': {'High-absence': 0.1278149471852898,
      'Low-absence': 0.5034849294152204,
      'No-absence': 0.36870012339948993},
     'G1': {'Fail': 0.2614871976647877, 'Pass': 0.7385128023352121},
     'Pstatus': {'A': 0.12442396313364057, 'T': 0.8755760368663592},
     'famrel': {1: 0.03724247501855778,
      2: 0.04846203869543736,
      3: 0.15602529390568748,
      4: 0.4814761637760789,
      5: 0.2767940286042384},
     'studytime': {'long_studytime': 0.20430107526881724,
      'short_studytime': 0.7956989247311828},
     'failures': {'no_failure': 0.8448540706605223,
      'yes_failure': 0.1551459293394777},
     'schoolsup': {'no': 0.8940092165898619, 'yes': 0.10599078341013828},
     'paid': {'no': 0.9385560675883257, 'yes': 0.06144393241167435},
     'higher': {'no': 0.10752688172043012, 'yes': 0.8924731182795699},
     'internet': {'no': 0.2334869431643625, 'yes': 0.7665130568356374},
     'G2': {'Fail': 0.4999999999999999, 'Pass': 0.4999999999999999},
     'G3': {'Fail': 0.4999999999999999, 'Pass': 0.4999999999999999}}




```python
marginalDistLearned['address']
```




    {'R': 0.3041474654377881, 'U': 0.6958525345622117}




```python
marginalDistLearned['G1']
```




    {'Fail': 0.2614871976647877, 'Pass': 0.7385128023352121}



Output tells us that `P(G1=Fail) ~ 0.25` and `P(G1 = Pass) ~ 0.75`. As a quick sanity check can compute what proportion of our data are `Fail` and `Pass`, should give nearly the same result:


```python
import numpy as np

labels, counts = np.unique(discrData['G1'], return_counts = True)

print(list(zip(labels, counts)))
print('\nProportion failures = {}'.format(counts[0] / sum(counts)))
print('\nProportion passes = {}'.format(counts[1] / sum(counts)))
```

    [('Fail', 157), ('Pass', 492)]
    
    Proportion failures = 0.24191063174114022
    
    Proportion passes = 0.7580893682588598



```python


```

## Marginals After Observations
Can query the marginal likelihood of states in our network, **given observations**.

$\color{red}{\text{TODO}}$ is this using the Bayesian update rule?

These observations can be made anywhere in the network and their impact will be propagated through to the node of interest.


```python
# Reminding of the data types for each variable:
discrDataVals
```




    {'address': array(['U', 'R'], dtype=object),
     'famsize': array(['GT3', 'LE3'], dtype=object),
     'Pstatus': array(['A', 'T'], dtype=object),
     'Medu': array([4, 1, 3, 2, 0]),
     'Fedu': array([4, 1, 2, 3, 0]),
     'traveltime': array([2, 1, 3, 4]),
     'studytime': array(['short_studytime', 'long_studytime'], dtype=object),
     'failures': array(['no_failure', 'yes_failure'], dtype=object),
     'schoolsup': array(['yes', 'no'], dtype=object),
     'famsup': array(['no', 'yes'], dtype=object),
     'paid': array(['no', 'yes'], dtype=object),
     'activities': array(['no', 'yes'], dtype=object),
     'nursery': array(['yes', 'no'], dtype=object),
     'higher': array(['yes', 'no'], dtype=object),
     'internet': array(['no', 'yes'], dtype=object),
     'romantic': array(['no', 'yes'], dtype=object),
     'famrel': array([4, 5, 3, 1, 2]),
     'freetime': array([3, 2, 4, 1, 5]),
     'goout': array([4, 3, 2, 1, 5]),
     'Dalc': array([1, 2, 5, 3, 4]),
     'Walc': array([1, 3, 2, 4, 5]),
     'health': array([3, 5, 1, 2, 4]),
     'absences': array(['Low-absence', 'No-absence', 'High-absence'], dtype=object),
     'G1': array(['Fail', 'Pass'], dtype=object),
     'G2': array(['Pass', 'Fail'], dtype=object),
     'G3': array(['Pass', 'Fail'], dtype=object)}




```python
# Reminder of nodes you CAN query (for instance putting 'health' in the dictionary argument of 'query' will give us an error)
bayesNetFull.nodes
```




    ['address',
     'absences',
     'G1',
     'Pstatus',
     'famrel',
     'studytime',
     'failures',
     'schoolsup',
     'paid',
     'higher',
     'internet',
     'G2',
     'G3']




```python
marginalDistObs_biasPass: Dict[str, Dict[str, float]] = eng.query({'studytime': 'long_studytime', 'paid':'yes', 'higher':'yes', 'absences':'No-absence', 'failures':'no_failure'})

# Seeing if biasing in favor of failing will influence the observed marginals:
marginalDistObs_biasFail: Dict[str, Dict[str, float]] = eng.query({'studytime': 'short_studytime', 'paid':'no', 'higher':'no', 'absences':'High-absence', 'failures': 'yes_failure'})
```


```python
# Higher probability of passing when have the above observations, since they are another set of observations in favor of passing.
marginalDistLearned['G1']
```




    {'Fail': 0.2614871976647877, 'Pass': 0.7385128023352121}




```python
marginalDistObs_biasPass['G1']
```




    {'Fail': 0.07373430443712227, 'Pass': 0.9262656955628777}




```python
marginalDistObs_biasFail['G1']
```




    {'Fail': 0.7243863093775379, 'Pass': 0.27561369062246216}




```python
marginalDistLearned['G2']
```




    {'Fail': 0.4999999999999999, 'Pass': 0.4999999999999999}




```python
# G2 and G3 nodes don't show bias probability because they are not many conditionals on them.
marginalDistObs_biasPass['G2']
```




    {'Fail': 0.5, 'Pass': 0.5}




```python
marginalDistObs_biasFail['G2']
```




    {'Fail': 0.5, 'Pass': 0.5}




```python
marginalDistLearned['G3']
```




    {'Fail': 0.4999999999999999, 'Pass': 0.4999999999999999}




```python
marginalDistObs_biasPass['G3']
```




    {'Fail': 0.5, 'Pass': 0.5}




```python
marginalDistObs_biasFail['G3']
```




    {'Fail': 0.5, 'Pass': 0.5}



Looking at difference in likelihood of `G1` based on just `studytime`. See that students who study longer are more likely to pass on their exam:


```python
marginalDist_short = eng.query({'studytime':'short_studytime'})
marginalDist_long = eng.query({'studytime': 'long_studytime'})

print('Marginal G1 | Short Studytime', marginalDist_short['G1'])
print('Marginal G1 | Long Studytime', marginalDist_long['G1'])
```

    Marginal G1 | Short Studytime {'Fail': 0.2817997392562336, 'Pass': 0.7182002607437664}
    Marginal G1 | Long Studytime {'Fail': 0.18237519357178764, 'Pass': 0.8176248064282124}


## Interventions with Do Calculus
Do-Calculus, allows us to specify interventions.

### Updating a Node Distribution
Can apply an intervention to any node in our data, updating its distribution using a `do` operator, which means asking our mdoel "what if" something were different.

For example, can ask what would happen if 100% of students wanted to go on to do higher education.


```python
print("'higher' marginal distribution before DO: ", eng.query()['higher'])

# Make the intervention on the network
eng.do_intervention(node = 'higher', state = {'yes': 1.0, 'no': 0.0}) # all students yes

print("'higher' marginal distribution after DO: ", eng.query()['higher'])
```

    'higher' marginal distribution before DO:  {'no': 0.10752688172043012, 'yes': 0.8924731182795699}
    'higher' marginal distribution after DO:  {'no': 0.0, 'yes': 1.0000000000000002}


### Resetting a Node Distribution
We can reset any interventions that we make using `reset_intervention` method and providing the node we want to reset:


```python
eng.reset_do('higher')

eng.query()['higher'] # same as before
```




    {'no': 0.10752688172043012, 'yes': 0.8924731182795699}



### Effect of DO on Marginals
We can use `query` to find the effect that an intervention has on our marginal likelihoods of OTHER variables, not just on the INTERVENED variable.

**Example 1:** change 'higher' and check grade 'G1' (how the likelihood of achieving a pass changes if 100% of students wanted to do higher education)

Answer: if 100% of students wanted to do higher education (as opposed to 90% in our data population) , then we estimate the pass rate would increase from 74.7% to 79.3%.


```python
print('marginal G1', eng.query()['G1'])

eng.do_intervention(node = 'higher', state = {'yes':1.0, 'no': 0.0})
print('updated marginal G1', eng.query()['G1'])
```

    marginal G1 {'Fail': 0.2614871976647877, 'Pass': 0.7385128023352121}
    updated marginal G1 {'Fail': 0.22096538189680157, 'Pass': 0.7790346181031987}



```python
# This is how we know it is 90% of the population that does higher education:
eng.reset_do('higher')

eng.query()['higher']
```




    {'no': 0.10752688172043012, 'yes': 0.8924731182795699}




```python
# OR:
labels, counts = np.unique(discrData['higher'], return_counts = True)
counts / sum(counts)
```




    array([0.10631741, 0.89368259])



**Example 2:** change 'higher' and check grade 'G1' (how the likelihood of achieving a pass changes if 80% of students wanted to do higher education)


```python
eng.reset_do('higher')

print('marginal G1', eng.query()['G1'])

eng.do_intervention(node = 'higher', state = {'yes':0.8, 'no': 0.2})
print('updated marginal G1', eng.query()['G1']) # fail is actually higher!!!!
```

    marginal G1 {'Fail': 0.2614871976647877, 'Pass': 0.7385128023352121}
    updated marginal G1 {'Fail': 0.2963359592252558, 'Pass': 0.7036640407747445}
