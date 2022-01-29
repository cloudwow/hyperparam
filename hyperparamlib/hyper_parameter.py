from typing import Dict, List
from collections import defaultdict
import random
import numpy as np
class HVal:
  value: object
  found_errors: List[int]
  def __init__(self, value):
    self.value = value
    self.found_errors = []
    self.mean_error = None
  def add_error(self, error):
    self.found_errors.append(error)
    self.mean_error = sum(self.found_errors)/len(self.found_errors)
  def get_error(self):
    if len(self.found_errors)>0:
      return self.mean_error
    else:
      return 0.00000001
class HyperParameter:
  name: str
  h_values: Dict[object,HVal]
  values_list: List
  def __init__(self, name: str, values: List):
    self.name = name
    self.h_values = {v:HVal(v) for v in values}
    self.values_list = values
    
  def set_new_values(self, new_values: List):
    updated_h_values = {}
    updated_values_list = []
    for new_val in new_values:
      if new_val in self.h_values:
        updated_h_values[new_val] =  self.h_values[new_val]
      else:
        updated_h_values[new_val] =  HVal(new_val)
      updated_values_list.append(new_val) 
    self.h_values = updated_h_values
    self.values_list = updated_values_list

  def _calc_probs(self):

    num_choices = len(self.h_values)
    probs = np.empty([num_choices])
    counts = np.empty([num_choices])
    for index, v in enumerate(self.h_values.values()):
      if v.mean_error:
        probs[index]=1.0/v.get_error()
      else:
        probs[index]=10000
      counts[index] =max(1, len(v.found_errors))
    # higher counts mean more certainty
    probs = probs* np.sqrt(counts)
    probs = probs/probs.sum()
    return probs
  def get_likely_value(self):
    probs = self._calc_probs()
    
    choice = np.random.choice(a=len(self.h_values),p=probs)
    derp = list(self.h_values.values())
    return derp[choice].value
    

  def get_really_random_value(self):
    return random.choice(self.values_list)
    
    

  def set_error(self,value: str,error: float):
    self.h_values[value].add_error(error)

class HyperParameters:
  params: List[HyperParameter]
  params_by_name: Dict[str,HyperParameter]
  def __init__(self):
    self.params=[]
    self.params_by_name={}
  def add_param(self, name:str,values:list):
    if name in self.params_by_name:
      self.update_param(name, values)
    else:
      hp = HyperParameter(name,values)
      self.params.append(hp)
      self.params.sort(key= lambda v: v.name)
      self.params_by_name[name]= hp
  def update_param(self, name:str,new_values:list):
    self.params_by_name[name].set_new_values(new_values)
  def get_likely_values(self) ->Dict:
    result = {}
    for param in self.params:
      result[param.name]=param.get_likely_value()
    return result

  def set_error(self,scored_params: Dict,error: float):
    for name,value in scored_params.items():
      if name in self.params_by_name:
        self.params_by_name[name].set_error(value,error)
  def __str__(self):
    result = ""
    for param in self.params:
      probs = param._calc_probs()
      result=result+f"{param.name}:\n"
      for index,hv in enumerate(param.h_values.values()):
        result=result+f"\t{hv.value}:\t{hv.mean_error}\t{probs[index]}\n"
    return result
  def with_random_tweaks(self, params, how_many = 1):
    """makes a copy with one random change"""
    result = params.copy()
    for _ in range(how_many):
      tweak_target = random.choice(self.params)
      result[tweak_target.name]=tweak_target.get_really_random_value()
    return result